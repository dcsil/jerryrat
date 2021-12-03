"""
This file has tasks for running periodically
"""

# from datetime import timezone
# from background_task import background
# from logging import getLogger
import time
from threading import Thread

from myapp.datapipe.backbone import createBackBone


# logger = getLogger(__name__)

# @background(schedule=60)
def train_model_periodically():
    backbone = createBackBone()

    while True:
        time.sleep(backbone.period * 60)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        # logger.debug("Training turn at: ", current_time)
        print("task start at", current_time)
        backbone.train_model_database_or_runtime(steps=50)

    # logger.debug("This training cycle finished")
    print("This training cycle finished")


class CreateTrainModelPeriodicallyThread(Thread):
    """
    start a new thread at background to
    periodically train the model
    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            print("Train thread start!")
            train_model_periodically()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    train_model_periodically()
