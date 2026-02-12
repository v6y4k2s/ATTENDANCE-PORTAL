import logging
import sys #line number
import os #files

#Create logs folder if not exists

LOG_DIR= "logs"

os.makedirs(LOG_DIR, exist_ok=True)

def get_log(name="attendance"):
    """Create and return a logger that logs to both console and logs/app.log.
    Prevents duplicate handlers and keeps formatting consistent."""

    log=logging.getLogger(name)

    #if handlers already exists return existing loggers
    if log.handlers:
        return log
    
    log.setLevel(logging.DEBUG)

    #prepare formatter (single definition)
    formatter =logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(funcName)s() | %(message)s"
        )
    
    #Console Handler
    console_handler=logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    #file handler
    file_handler =logging.FileHandler(
        os.path.join(LOG_DIR, "app.log"),
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    #register Handlers
    log.addHandler(console_handler)
    log.addHandler(file_handler)

    log.propagate =False
    return log