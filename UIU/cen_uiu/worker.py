import multiprocessing

from kivy.logger import Logger
_LOGGER = Logger


class UIUCoreWorker(multiprocessing.Process):
    def __init__(self, core):
        super().__init__()

        self.core = core

    def run(self):
        try:
            self.core.bl_audio.enable()
            self.core.app.run()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.core.bl_audio.disable()
        self.core.app.stop()

        self.kill()
