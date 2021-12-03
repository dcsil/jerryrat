"""
This file has tasks for running periodically
"""

import time
from threading import Thread, Event

from myapp.datapipe.backbone import createBackBone


def train_model_periodically(backbone):
    time.sleep(backbone.period * 60)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("task start at", current_time)
    backbone.train_model_database_or_runtime(steps=50)

# borrow ideas from:
# Django background: https://www.youtube.com/watch?v=U5nuICIuAp0&t=530s
# How to stop a thread: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s03.html
class CreateTrainModelPeriodicallyThread(Thread):
    """
    start a new thread at background to
    periodically train the model
    """
    def __init__(self):
        Thread.__init__(self)
        self._stopevent = Event()
        self._sleepperiod = 1.0

    def run(self):
        self._stopevent.clear()
        backbone = createBackBone()
        try:
            print("Train thread start!")
            while not self._stopevent.is_set():
                train_model_periodically(backbone)
                self._stopevent.wait(self._sleepperiod)
        except Exception as e:
            print(e)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        Thread.join(self, timeout)
        print("This training cycle finished")


if __name__ == "__main__":
    backbone = createBackBone()
    train_model_periodically(backbone)
