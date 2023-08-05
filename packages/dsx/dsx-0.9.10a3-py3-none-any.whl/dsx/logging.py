# Setup Logger
import logging


def set_logging(logpath:str = "test.log", level=logging.DEBUG, debug:bool=True):
    # create logger
    logger = logging.getLogger(__name__)
    # set log level for all handlers to debug
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(level)

    # create file handler and set level to debug
    fileHandler = logging.FileHandler(logpath)
    fileHandler.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to handlers
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    # set log level for development
    if debug:
        logger.setLevel(logging.DEBUG)

    return logger

if __name__=='__main__':
    set_logging()