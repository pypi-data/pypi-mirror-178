'''
==============================
Declassed Tor Circuits Manager
==============================

Maintain the specified number of circuits and attach streams to them in a round-robin manner.

How to use:

.. code:: python

    import dtcm

    config = {
        'tor': {
            'address': '127.0.0.1',
            'socks_port': 9100,
            'control_port': 9051,
            'password': '12345'
        },
        'circuits': {
        'hops': 2,  # Although this can be 1, exit-only circuits
                    # do not work, need a guard relay.
                    # So 2 is the minimum.
        'count': 100
            stable_only: False  # only use relays with Stable flag
            fast_only: False    # only use relays with Fast flag
        }
    }

    dtcm.init(config)
    # dtcm.logger.setLevel(logging.DEBUG)
    # your code here, a crawler, right?
    # or just a sleep call if this is a standalone process
    dtcm.fini()

:copyright: Copyright 2022 AXY axy@declassed.art
:license: BSD, see LICENSE for details.
'''

__version__ = '0.2.20'

import logging
import random
import threading
import time
import traceback

import stem
import stem.control
import stem.descriptor.remote

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)

_tcm = None

def init(config):
    global _tcm
    _tcm = TorCircuitsManager(config)
    logger.info('Starting circuit manager')
    _tcm.start()

def fini():
    global _tcm
    _tcm.close()
    _tcm = None


class TorCircuitsManager(threading.Thread):

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self._config = config
        self._controller = None

        self._circuit_ids = []
        self._circuit_index = 0
        self._circuit_paths = dict()
        self._circuits_awaiting_creation = set()
        self._circuits_lock = threading.RLock()

        self._exit_fingerprints = None
        self._middle_fingerprints = None
        self._guard_fingerprints = None

        self._fingerprints_in_use = set()
        self._fingerprints_last_updated = None

        self._shutdown_event = threading.Event()

        logger.info('Initializing tor controller')
        self._controller = stem.control.Controller.from_port(
            address = self._config['tor']['address'],
            port = self._config['tor']['control_port']
        )
        self._controller.authenticate(password=self._config['tor']['password'])

        self._update_fingerprints()

        hops_required = self._config['circuits']['hops']
        for circ in self._controller.get_circuits():
            if circ.status != 'BUILT':
                continue
            if circ.purpose != 'GENERAL':
                continue
            if len(circ.path) == hops_required:
                self._add_circuit_awaiting_creation(circ.id, circ.path)
                self._circuit_created(circ.id)
                logger.debug(f'Using existing circuit {circ.id}')
        if len(self._circuit_ids) == 0:
            self._create_circuits(3)

        # XXX event listeners eventually stop working, have no idea how to fix this
        self._controller.add_event_listener(self._handle_circuit, stem.control.EventType.CIRC)
        self._controller.add_event_listener(self._attach_stream, stem.control.EventType.STREAM)
        self._controller.set_conf('__LeaveStreamsUnattached', '1')  # leave stream management to us

        logger.info('Initialization complete')

    def close(self):
        logger.info('Deinitializing circuits manager')
        self._shutdown_event.set()
        self.join()
        logger.info('Removing event listeners')
        # Stop listening for attach stream events and stop controlling streams
        # XXX these calls may hang indifinitely for unknown reason
        self._controller.remove_event_listener(self._attach_stream)
        self._controller.remove_event_listener(self._handle_circuit)
        # reset_conf has bugs that cause an exception
        # self._controller.reset_conf('__LeaveStreamsUnattached')
        # instead, do this:
        logger.info('Restoring __LeaveStreamsUnattached')
        self._controller.set_conf('__LeaveStreamsUnattached', '0')
        logger.info('Closing tor controller')
        self._controller.close()
        logger.info('Deinitialized circuits manager')
        logger.info('Finalization complete')

    def _handle_circuit(self, circuit):
        try:
            if circuit.status == 'BUILT':
                num_hops = len(circuit.path)
                if num_hops != self._config['circuits']['hops']:
                    logger.debug(f'Rejecting created {num_hops}-hops circuit {circuit.id}')
                    self._forget_circuit(circuit.id)
                else:
                    logger.debug(f'Using created {num_hops}-hops circuit {circuit.id}')
                    self._circuit_created(circuit.id)
            elif circuit.status in ['CLOSED', 'FAILED']:
                if circuit.status == 'CLOSED':
                    logger.debug(f'Closed circuit {circuit.id}')
                elif circuit.status == 'FAILED':
                    logger.debug(f'Failed circuit {circuit.id}')
                self._forget_circuit(circuit.id)
        except Exception:
            traceback.print_exc()

    def _attach_stream(self, stream):
        try:
            if stream.status == 'NEW':
                # Don't stuck in here for too long, three attempts only.
                # Tor spec says: Tor will close unattached streams by itself,
                # roughly two minutes after they are born.
                for attempt in range(3):
                    try:
                        circuit_id = self._get_circuit_for_stream()
                        self._controller.attach_stream(stream.id, circuit_id)
                        logger.debug(f'Attached stream {stream.id} to circuit {circuit_id}')
                        return
                    except stem.InvalidRequest:
                        # 552 Unknown circuit. Try again.
                        continue
                    except stem.UnsatisfiableRequest:
                        # 555 Connection is not managed by controller.
                        # The stream isn't in an appropriate state to be attached (e.g. it's already open), so do nothing.
                        return
                    except stem.OperationFailed:
                        # 551 Can't attach stream to this one-hop circuit. Try again.
                        continue
        except Exception:
            traceback.print_exc()

    def _get_circuit_for_stream(self):
        # get a circuit for new stream, sequentially
        with self._circuits_lock:
            if self._circuit_index >= len(self._circuit_ids):
                self._circuit_index = 0
            circuit_id = self._circuit_ids[self._circuit_index]
            self._circuit_index = (self._circuit_index + 1) % len(self._circuit_ids)
        return circuit_id

    def _add_circuit_awaiting_creation(self, circuit_id, path):
        with self._circuits_lock:
            self._circuits_awaiting_creation.add(circuit_id)
            self._circuit_paths[circuit_id] = path
            for fingerprint in path:
                self._fingerprints_in_use.add(fingerprint)

    def _circuit_created(self, circuit_id):
        # move circuit from the set of circuits awaiting creation to the list of available circuits
        with self._circuits_lock:
            self._circuit_ids.append(circuit_id)
            if circuit_id in self._circuits_awaiting_creation:
                self._circuits_awaiting_creation.remove(circuit_id)

    def _forget_circuit(self, circuit_id):
        # remove circuit from all internal structures
        with self._circuits_lock:
            try:
                self._circuit_ids.remove(circuit_id)
            except ValueError:
                pass
            if circuit_id in self._circuits_awaiting_creation:
                self._circuits_awaiting_creation.remove(circuit_id)
            if circuit_id in self._circuit_paths:
                for fingerprint in self._circuit_paths[circuit_id]:
                    self._fingerprints_in_use.remove(fingerprint)
                del self._circuit_paths[circuit_id]

    def run(self):
        logger.info('Running circuit manager')
        while not self._shutdown_event.is_set():
            try:
                # maintain requisted number of circuits
                num_missing_circuits = self._config['circuits']['count'] - len(self._controller.get_circuits())
                if num_missing_circuits > 0:
                    logger.debug(f'Need {num_missing_circuits} more circuits')
                    self._create_circuits(num_missing_circuits)

                if time.monotonic() - self._fingerprints_last_updated > 3600:
                    self._update_fingerprints()
            except Exception:
                traceback.print_exc()
                pass

            self._shutdown_event.wait(10)
        logger.info('Stopped circuit manager')

    def _create_circuits(self, count):
        # XXX with await_build=True this does not create circuits as fast as necessary,
        # so create circuits in parallel but not too many at once
        parallel_creation_count = max(2, self._config['circuits']['count'] // 10)
        logger.debug(f'Creating up to {parallel_creation_count} circuits in parallel')
        for i in range(count):
            while len(self._circuits_awaiting_creation) >= parallel_creation_count:
                self._shutdown_event.wait(1)
                if self._shutdown_event.is_set():
                    break

            if self._shutdown_event.is_set():
                break
            while not self._shutdown_event.is_set():
                path = self._create_path()
                if path is None:
                    logger.debug('Will try again in 3 seconds')
                    self._shutdown_event.wait(3)
                    continue

                logger.debug(f'Creating new circuit {path}')
                try:
                    circuit_id = self._controller.new_circuit(path=path, await_build=False)
                    break
                except stem.InvalidRequest as e:
                    if e.code == '552':  # No such router
                        continue
                    else:
                        raise
                except stem.CircuitExtensionFailed:
                    continue

            self._add_circuit_awaiting_creation(circuit_id, path)

    def _create_path(self):
        # create path for new circuit
        # update self._fingerprints_in_use
        with self._circuits_lock:
            guard_fingerprints = self._guard_fingerprints
            middle_fingerprints = self._middle_fingerprints
            exit_fingerprints = self._exit_fingerprints
            fingerprints_in_use = self._fingerprints_in_use
        hops_required = self._config['circuits']['hops']
        path = []
        if hops_required > 1:
            guards = list(set(guard_fingerprints) - fingerprints_in_use)
            if len(guards) == 0:
                logger.info(f'All available {len(guard_fingerprints)} guard relays are in use')
                return None
            guard = random.choice(guards)
            path.append(guard)

        while len(path) < hops_required - 1:
            middles = list(set(middle_fingerprints) - fingerprints_in_use - set(path))
            if len(middles) == 0:
                logger.info(f'All available {len(middle_fingerprints)} middle relays are in use')
                return None
            middle = random.choice(middles)
            path.append(middle)

        exits = list(set(exit_fingerprints) - fingerprints_in_use - set(path))
        if len(exits) == 0:
            logger.info(f'All available {len(exit_fingerprints)} exit relays are in use')
            return None
        exit = random.choice(exits)
        path.append(exit)
        return path

    def _update_fingerprints(self):
        # update fingerprints of guard and exit relays
        new_guards = []
        new_middles = []
        new_exits = set()
        stable_only = self._config['circuits']['stable_only']
        fast_only = self._config['circuits']['fast_only']
        for desc in self._controller.get_network_statuses():
            if stable_only and 'Stable' not in desc.flags:
                continue
            if fast_only and 'Fast' not in desc.flags:
                continue
            # at first, collect exit nodes
            if 'Exit' in desc.flags:
                new_exits.add(desc.fingerprint)
                continue
            # there are a lot of guard nodes, and on the one hand the following approach has to be changed to choose less guards
            # but on the other hand that's not bad for short circuits that don't need anonymity
            if 'Guard' in desc.flags and desc.fingerprint not in new_exits:
                new_guards.append(desc.fingerprint)
            else:
                new_middles.append(desc.fingerprint)
        logger.info(f'{len(new_guards)} guard, {len(new_middles)} middle, {len(new_exits)} exit relays')
        with self._circuits_lock:
            self._guard_fingerprints = new_guards
            self._middle_fingerprints = new_middles
            self._exit_fingerprints = list(new_exits)
            self._fingerprints_last_updated = time.monotonic()
