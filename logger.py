import configparser
import os
import logging
import sys

config = configparser.ConfigParser()
config.read('config/config.ini')

if not os.path.exists(config["log_file"]["path"]):
    os.makedirs(config["log_file"]["path"])

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
       self.logger = logger
       self.level = level
       self.linebuf = ''

    def write(self, buf):
       for line in buf.rstrip().splitlines():
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass

logging.basicConfig(filename=config["log_file"]["path"] + config["log_file"]["file"],
                    format='[%(asctime)s] - %(message)s',
                    filemode='a+',
                    level=logging.INFO)

logger = logging.getLogger()
sys.stdout = StreamToLogger(logger,logging.INFO)
sys.stderr = StreamToLogger(logger,logging.ERROR)