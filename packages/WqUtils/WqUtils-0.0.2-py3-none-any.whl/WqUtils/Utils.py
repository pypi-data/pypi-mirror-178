#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ Author: stephen.wan
@ Date: 2022-11-08 17:35
@ Email: stephen.wan@colourdata.com.cn
@ LastEditors: stephen.wan
@ LastEditTime: 2022-11-08 17:35
@ ProjectName: YiliEcommerceNewProductProject
@ Description: to do
"""
import os
import logging
from logging import handlers


def get_base_file(name=None):
    base_path = os.path.dirname(os.path.abspath(name))
    return base_path


class Log(object):
    def __init__(self, filename=None):
        """日志logger类"""
        # 创建logs文件夹
        self.file_name = filename
        cur_path = os.path.dirname(os.path.realpath(self.file_name))
        self.log_path = os.path.join(cur_path, 'logs')
        # 如果不存在这个logs文件夹，就自动创建一个
        if not os.path.exists(self.log_path): os.mkdir(self.log_path)
        # 文件的命名
        self.logname = os.path.join(self.log_path, f"{os.path.basename(self.file_name).split('.')[0]}.txt")
        logging.basicConfig()
        self.logger = logging.getLogger(self.logname)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(self.formatter)
        # self.logger.addHandler(fh)
        th = handlers.TimedRotatingFileHandler(filename=self.logname, interval=1, when='MIDNIGHT', backupCount=7,
                                               encoding='utf-8')
        th.suffix = "%Y-%m-%d.log"  # 设置文件后缀
        th.setFormatter(self.formatter)  # 设置文件里写入的格式
        self.logger.addHandler(th)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(th)

    def set_log_level(self, log_level=logging.INFO):
        self.logger.setLevel(log_level)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


if __name__ == '__main__':
    print(get_base_file(__file__))
