# from root_constants import *
# from py_utils_includes import *
import logging
import os
ROOT_DIR = "./"
ROOT_LOG_FILE = "pod.log"
ROOT_APPLOG_FILE = "podapp.log"
ROOT_ERROR_LOG_FILE = "error.log"
ROOT_LOG_DIR = ROOT_DIR + "logs/"

# Setup these objects here to supress link warnings
initialized_logobj = None
Log = None
AppLog = None

# Debug (10), Info (20), Warning (30), Error (40), Critical (50)

# for Production
# Log.setLevel(logging.WARNING)
# for Dev
# Log.setLevel(logging.DEBUG)


def logger_initialize(slogname=ROOT_LOG_FILE, sdir=ROOT_LOG_DIR, btoconsole=True,
                      btofile=True, file_level=logging.DEBUG, console_level=logging.INFO):
    
    logger = filehandler = consolehandler = None

    slogpath = os.path.join(str(sdir), str(str(slogname)))
    logformat = logging.Formatter(
            '%(asctime)s - %(levelname)-9s| %(message)-90s [L:%(lineno)-04d M:%(module)-s F:%(funcName)-s]',
            datefmt='%Y-%m-%d %H:%M:%S')

    if logger is None:
        logger = logging.getLogger(str(slogpath))
        logger.setLevel(logging.DEBUG)
    else:
        if filehandler is not None:
            logger.removeHandler(filehandler)
            del filehandler
        if consolehandler is not None:
            logger.removeHandler(consolehandler)
            del consolehandler

    filehandler = consolehandler = None

    # create a file handler if log_file is supplied as parameter
    if btofile:
        if (str(slogpath) is not None) and (len(str(slogpath)) > 0):
            filehandler = logging.FileHandler(str(slogpath), mode='a')
            filehandler.setFormatter(logformat)
            filehandler.setLevel(file_level)
            logger.addHandler(filehandler)

    if btoconsole:
        consolehandler = logging.StreamHandler()
        consolehandler.setFormatter(logformat)
        consolehandler.setLevel(console_level)
        logger.addHandler(consolehandler)

    return logger

if ('initialized_logobj' not in globals()) or (initialized_logobj is None) or (Log is None):
    initialized_logobj = True

# Dev Settings
#    Log = logger_initialize(slogname=ROOT_LOG_FILE, sdir=ROOT_LOG_DIR, btoconsole=True, btofile=True, file_level=logging.DEBUG, console_level=logging.INFO)
#    AppLog = logger_initialize(slogname=ROOT_APPLOG_FILE, sdir=ROOT_LOG_DIR, btoconsole=True, btofile=True, file_level=logging.DEBUG, console_level=logging.INFO)

# Production Settings
    Log = logger_initialize(slogname=ROOT_LOG_FILE, sdir=ROOT_LOG_DIR, btoconsole=True, btofile=True, file_level=logging.INFO, console_level=logging.INFO)
    # AppLog = logger_initialize(slogname=ROOT_APPLOG_FILE, sdir=ROOT_LOG_DIR, btoconsole=True, btofile=True, file_level=logging.WARNING, console_level=logging.INFO)


#    Log.debug("*** LOADING MODULE = [LOGUTILS] DEBUG ***")
#    Log.info("*** LOADING MODULE = [LOGUTILS] INFO ***")
#    Log.warning("*** LOADING MODULE = [LOGUTILS] WARNING ***")
#    Log.error("*** LOADING MODULE = [LOGUTILS] ERROR ***")
#    Log.critical("*** LOADING MODULE = [LOGUTILS] CRITICAL ***")


