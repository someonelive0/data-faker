# -*- coding: utf-8 -*-
# 产生模拟http pcap文件，方法是访问本地 faka_api，然后把请求和响应保存成pcap文件

import random, time, sys, logging, argparse


logger = logging.getLogger('fake_pcap')
ARG_TABLE_NUMBER = 2
ARG_ITEM_MIN = 20
ARG_ITEM_MAX = 100
ARG_DB = 'mysql'
ARG_INSERT_BENTCH = 40


def init():
    logger.setLevel(logging.DEBUG)
    formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d行 | [ %(levelname)s ] | [%(message)s]", datefmt="%Y/%m/%d/%X")
    sh = logging.StreamHandler()
    fh = logging.FileHandler("fake_pcap.log", encoding="utf-8")
    sh.setFormatter(formator)
    fh.setFormatter(formator)
    logger.addHandler(sh)
    logger.addHandler(fh)


# 主函数
if __name__ == '__main__':
    init()
