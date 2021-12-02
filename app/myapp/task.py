"""
This file has tasks for running periodically, and
will not be imported by any other module

data center running: Heroku
"""

# from datetime import timezone
# from background_task import background
from logging import getLogger
import time

from app.myapp.datapipe.backbone import createBackBone

logger = getLogger(__name__)

# @background(schedule=60)
def train_model_periodically():
   """
   Does something that takes a long time
   :param p1: first parameter
   :param p2: second parameter
   :return: None
   """
   backbone = createBackBone()

   for i in range(50 // backbone.period):
      time.sleep(backbone.period * 60)
      backbone.train_model_with_database(steps=50)

      t = time.localtime()
      current_time = time.strftime("%H:%M:%S", t)
      logger.debug("Training turn at: ", current_time)
   print("This training cycle finished")
   logger.debug("This training cycle finished")

if __name__ == "__main__":
   train_model_periodically()

