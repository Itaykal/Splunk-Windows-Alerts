""" 
    SETTING GLOBALS
"""

TEAM = 'monitoring'
INTERVAL = 10
ONE_HOUR = 3600
EXIT_CODES = {
    6: True, # 6 = vbYes - Yes was clicked
    7: False # 7 = vbNo - No was clicked
}

EMERGANCY_KILL = "kill.bat"
POPUP_SCRIPT = "quick_popup.vbs"
LOGGER_FILE = "audit.log"


import sys
import logging
from logging.handlers import RotatingFileHandler

def create_rotating_log(path):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("alert_notification")
    logger.setLevel(logging.INFO)
    
    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=10*1024*1024,
                                  backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
    
# Default Logger
LOGGER = create_rotating_log(LOGGER_FILE)


def exception_handler(exc_type, value, traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        logger.info("stopping...")
        sys.__excepthook__(exc_type, value, traceback)
        
    LOGGER.exception(f"Uncaught exception: ", exc_info=(exc_type, value, traceback))

# Default Exception Hook
sys.excepthook = exception_handler

