import signal

class GracefulKiller:
    """
    Callback hooks on signal interrupts.
    Based on http://stackoverflow.com/a/31464349/1910555
    """
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill_now = True
