#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

###Starting the logger###
try:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except:
    print("!!! Failed to launch logger !!!")
    print("!!!   Immediate shutdown    !!!")
    exit()
###End of logger starting###

logger.info("Server starting...")