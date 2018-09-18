#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging  # 引入logging模块
import os
import time
import json
import requests
from flask import Flask, request
app = Flask(__name__)


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

# 设置跨域
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
app.after_request(after_request)

# 创建任务
def creatScan(url):
  r = requests.get('http://127.0.0.1:8775/task/new')
  if r.status_code == requests.codes.ok:
    if r.json()['success']:
      # 启动
      taskid = r.json()['taskid']
      my_data = {
        'url': url
      }
      # 设置扫描url
      cs_url = 'http://127.0.0.1:8775/option/' + taskid + '/set'
      r = requests.post (cs_url, data = json.dumps(my_data), headers={'Content-Type': 'application/json'})
      if r.status_code == requests.codes.ok:
        if r.json()['success']:
          cs_url = 'http://127.0.0.1:8775/scan/' + taskid + '/start'
          r = requests.post (cs_url, data = json.dumps({}), headers={'Content-Type': 'application/json'})
          if r.status_code == requests.codes.ok:
            jsonData = r.json()
            if jsonData['success']:
              jsonData['taskid'] = taskid
              print(jsonData)
              return json.dumps(jsonData)
            else:
              return r.text
        else:
          logger.error(r.json()['message'])
          return r.text
    else:
      logger.error('新建任务失败!')
      return '{ "message": "Creat scan failed", "success": false }'

# 查询状态
@app.route('/getStatus/<id>')
def getStatus(id):
  r = requests.get('http://127.0.0.1:8775/scan/' + id + '/data')
  return r.text

@app.route('/creatScan', methods = ['POST'])
def creatScan():
  jsonData = json.loads(request.get_data())
  printf(jsonData)
  if (jsonData, jsonData['url']):
    return creatScan(jsonData['url'])
  return '{ "message": "Parameter error", "success": false }'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5005)