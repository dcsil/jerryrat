"""
This file has tasks for running periodically
"""

import time
from threading import Thread, Event

from myapp.datapipe.backbone import createBackBone

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your tests here.


def train_model_periodically(backbone, savemodel, steps):
    time.sleep(backbone.period * 60)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("task start at", current_time)
    backbone.train_model_database_or_runtime(steps=steps, savemodel=savemodel)

# borrow ideas from:
# Django background: https://www.youtube.com/watch?v=U5nuICIuAp0&t=530s
# How to stop a thread: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s03.html
class CreateTrainModelPeriodicallyThread(Thread):
    """
    start a new thread at background to
    periodically train the model
    """
    def __init__(self, savemodel=True, steps=50):
        super(CreateTrainModelPeriodicallyThread, self).__init__()
        self._stopevent = Event()
        self._sleepperiod = 1.0
        self.savemodel = savemodel
        self.steps = steps

    def run(self):
        self._stopevent.clear()
        backbone = createBackBone()
        try:
            print("Train thread start!")
            while not self._stopevent.is_set():
                train_model_periodically(backbone, self.savemodel, self.steps)
                self._stopevent.wait(self._sleepperiod)
        except Exception as e:
            logger.error(e)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        print("Start ending the training cycle.")
        Thread.join(self, timeout)
        print("This training cycle finished")


if __name__ == "__main__":
    backbone = createBackBone()
    train_model_periodically(backbone, savemodel=False)
