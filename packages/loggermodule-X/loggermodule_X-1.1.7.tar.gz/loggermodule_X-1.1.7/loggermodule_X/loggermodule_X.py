import logging
from pathlib import Path
import sys
from datetime import datetime
from logging import handlers

LEVEL_LIST = ['NOTSET', 'INFO', 'DEBUG', 'ERROR', 'WARNING', 'CRITICAL']
MODE_LIST = ['split', 'midnight']

class logger_x:
    def __init__(self, file, mode=None, console=None, rfile=None):
        self.formatter = logging.Formatter('[%(asctime)s] [PID:%(process)d ThreadID:%(thread)d] [%(levelname)s] [%(name)s.%(funcName)s:%(lineno)d]  %(message)s')
        self.name = Path(file).stem
        self.file = Path(file).parent.absolute()
        self.mode = mode if mode and mode in MODE_LIST else 'midnight'
        self.s_console = console if console and console in LEVEL_LIST else 'DEBUG'
        self.r_file = rfile if rfile and rfile in LEVEL_LIST else 'DEBUG'
        self.log_path = self.file / "log"
        self.log_name = self.name + '.log'
        self.full_path = self.log_path / self.log_name

    def namer(self, name):
        return name.replace(".log", "") + ".log"

    def configLogger(self):
        logging.getLogger().setLevel(level=self.s_console)
        logging.getLogger("filelock").setLevel(logging.ERROR) ## Avoid lockfile log
        log_path = self.log_path / datetime.now().strftime("%Y%m%d")
        log_path.mkdir(parents=True, exist_ok=True)
        full_path = log_path / self.log_name
        if self.mode == 'midnight':
            fileHandler = handlers.TimedRotatingFileHandler(full_path, when='midnight', backupCount=0, encoding='utf-8')
        elif self.mode == 'split':
            fileHandler = handlers.RotatingFileHandler(full_path, maxBytes=800000000, backupCount=10, encoding='utf-8')
        # fileHandler.handlers.clear()
        # consoleHandler.handlers.clear()
        logging.getLogger().handlers.clear()
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(level=self.s_console)
        consoleHandler.setFormatter(self.formatter)
        logging.getLogger().addHandler(consoleHandler)
        fileHandler.namer = self.namer
        fileHandler.setLevel(level=self.r_file)
        fileHandler.setFormatter(self.formatter)
        logging.getLogger().addHandler(fileHandler)
        log = logging.getLogger("app." + self.name)
        return log

if __name__ == '__main__':
    loggerX = logger_x(__file__)
    log = loggerX.configLogger()
    log.info('THIS is info msg !!')
    log.debug('THIS is debug msg !!')
    log.error('THIS is error msg !!')
    log.warning('THIS is warning msg !!')
    log.critical('THIS is critical msg !!')
