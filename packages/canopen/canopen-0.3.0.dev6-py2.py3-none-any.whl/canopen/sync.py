import time
import threading


class SyncProducer(object):

    def __init__(self, network):
        self.network = network
        self.period = None
        self.transmit_thread = None
        self.stop_event = threading.Event()

    def transmit(self):
        self.network.send_message(0x80, [])

    def start(self, period=None):
        """Start periodic transmission of SYNC message in a background thread."""
        if period is not None:
            self.period = period

        if not self.period:
            raise ValueError("A valid transmission period has not been given")

        if not self.transmit_thread or not self.transmit_thread.is_alive():
            self.stop_event.clear()
            self.transmit_thread = threading.Thread(target=self._periodic_transmit)
            self.transmit_thread.daemon = True
            self.transmit_thread.start()

    def stop(self):
        self.stop_event.set()
        if self.transmit_thread:
            self.transmit_thread.join(2)
            self.transmit_thread = None

    def _periodic_transmit(self):
        while not self.stop_event.is_set():
            start = time.time()
            self.transmit()
            time.sleep(self.period - (time.time() - start))
