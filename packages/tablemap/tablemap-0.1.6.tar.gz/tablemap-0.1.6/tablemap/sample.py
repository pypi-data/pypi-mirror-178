from contextlib import contextmanager
import signal
import time


@contextmanager
def _delayed_keyboard_interrupts():
    signal_received = []

    def handler(sig, frame):
        nonlocal signal_received
        signal_received = (sig, frame)
    # Do nothing but recording something has happened.
    old_handler = signal.signal(signal.SIGINT, handler)

    try:
        yield
    finally:
        # signal handler back to the original one.
        signal.signal(signal.SIGINT, old_handler)
        if signal_received:
            # do the delayed work
            old_handler(*signal_received)

# time.sleep(10)
# print('helo') 

with _delayed_keyboard_interrupts():
    time.sleep(5)
    print('helo') 