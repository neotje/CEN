import multiprocessing

from kivy.logger import Logger
_LOGGER = Logger


class UIUCoreWorker(multiprocessing.Process):
    def __init__(self, core):
        super().__init__()

        self.core = core

    def run(self):
        try:
            self.core.app.run()
        except KeyboardInterrupt:
            pass

        self.stop()

    def kill(self) -> None:
        self.core.app.stop()
        return super().kill()
