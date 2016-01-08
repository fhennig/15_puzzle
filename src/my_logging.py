import logging
import sys


level = logging.DEBUG
log = logging.getLogger()
log.setLevel(level)

if len(log.handlers) == 0:
   ch = logging.StreamHandler(sys.stdout)
   ch.setLevel(logging.DEBUG)
   formatter = logging.Formatter(logging.BASIC_FORMAT)
   ch.setFormatter(formatter)
   log.addHandler(ch)
