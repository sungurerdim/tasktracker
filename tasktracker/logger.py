import logging
import sys
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
log_file = "logs/tasktracker.log"

logger = logging.getLogger("TaskTracker")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)

# Optional: redirect all print/stdout/stderr to logger
class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line)

    def flush(self):
        pass

# sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)