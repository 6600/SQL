#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging  # 引入logging模块
import os
import time
import requests

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 判断日志目录是否存在
folder = os.path.exists('./Logs')
# 如果文件夹不存在创建文件夹
if not folder:
  os.makedirs('./Logs')

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.getcwd() + '/Logs/'
log_name = log_path + rq + '.log'
# 判断日志目录是否存在
file = os.path.exists(log_name)

fh = logging.FileHandler(log_name, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')

r = requests.get('http://127.0.0.1:8775/task/new')
print(r.text)