import logging
import os
import shutil
from datetime import datetime
from soccminer.environment import Platform


class SoCCMinerLogger:
    main_logger = None
    log_dir = ""
    if Platform.is_unix_platform():
        log_dir = os.getcwd() + '/soccminer_log'
    elif Platform.is_windows_platform():
        log_dir = os.getcwd() + '\\soccminer_log'

    def __init__(self, log, file_name: str = ""):
        self.main_log_file = None
        self.log = 0
        if log == 1:
            self.log = logging.INFO
        elif log == 2:
            self.log = logging.DEBUG
        elif log == 0:
            self.log = logging.NOTSET

        if log != 0:
            if SoCCMinerLogger.main_logger is None and len(file_name) == 0:
                fname = None
                if not os.path.isdir(SoCCMinerLogger.log_dir):
                    os.makedirs(SoCCMinerLogger.log_dir)
                if Platform.is_unix_platform():
                    fname = SoCCMinerLogger.log_dir + "/" + "soccminer_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.log'
                elif Platform.is_windows_platform():
                    fname = SoCCMinerLogger.log_dir + "\\" + "soccminer_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.log'

                self.main_log_file = fname
                logging.basicConfig(filename=fname, format='%(asctime)s:%(levelname)s:%(funcName)s:%(message)s', level=self.log)
                SoCCMinerLogger.main_logger = True

    @staticmethod
    def create_log_handle(log_file, level):
        logger = logging.getLogger(log_file)
        if level == 1:
            level = logging.INFO
        elif level == 2:
            level = logging.DEBUG
        elif level == 0:
            level = logging.NOTSET

        logger.setLevel(level)
        format_string = ("%(asctime)s — %(levelname)s — %(funcName)s:"
                        "%(lineno)d — %(message)s")
        log_format = logging.Formatter(format_string)
        # Creating and adding the file handler
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def fetch_ast_parsing_log(ast_parsing_log_file, log_level):
        if Platform.is_unix_platform():
            SoCCMinerLogger.log_dir = SoCCMinerLogger.log_dir + '/'
        elif Platform.is_windows_platform():
            SoCCMinerLogger.log_dir = SoCCMinerLogger.log_dir + '\\'

        if not os.path.isdir(SoCCMinerLogger.log_dir):
            os.makedirs(SoCCMinerLogger.log_dir)
        else:
            shutil.rmtree(SoCCMinerLogger.log_dir)
            os.makedirs(SoCCMinerLogger.log_dir)
        ast_log_file = SoCCMinerLogger.log_dir + ast_parsing_log_file
        ast_log_obj = SoCCMinerLogger.create_log_handle(ast_log_file, log_level)
        return ast_log_obj
