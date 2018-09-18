#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import json
import requests
from flask import Flask, request
app = Flask(__name__)

# 设置跨域
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
app.after_request(after_request)

# 创建任务
def creatScanUrl(url):
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
  print(jsonData['url'])
  # print('-----------------------')
  if (jsonData and jsonData['url']):
    return creatScanUrl(jsonData['url'])
  return '{ "message": "Parameter error", "success": false }'

print('----------------- V1.0.0 -----------------')
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5005)