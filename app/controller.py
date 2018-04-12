# -*- coding: UTF-8 -*- 
from flask import Flask, render_template
import os, sys, json
# import redis
import ConfigParser as cp
from MySQLHelper import *
from RedisHelper import *

app = Flask(__name__)

# [ 初始路径 ]
BASE_PATH = os.getcwd()
APP_PATH = BASE_PATH + '/app' # 根路径
UPLOAD_PATH = BASE_PATH + '/upload' # 上传路径

# [ 加载配置文件 ]
env = cp.ConfigParser()
env.read(BASE_PATH + '/.env')

# [ 加载数据库 ]
mysql_host = env.get('mysql', 'host')
mysql_user = env.get('mysql', 'user')
mysql_password = env.get('mysql', 'password')
mysql_db = env.get('mysql', 'db')
mysql = MySQLHelper(mysql_host, mysql_user, mysql_password, mysql_db)

# [ Redis ]
redis_host = env.get('redis', 'host')
redis_port = env.get('redis', 'port')
redis = RedisHelper(redis_host, redis_port).handler()

# [ 控制器 ]
@app.route('/')
@app.route('/login')
def index():
    redis.set('k', 'zzzzz', 60)
    r = redis.get('k')
    return r

# [ 启动项 ]
if __name__ == '__main__':
    app.secret_key = env.get('secret_key', 'key') # session会使用到
    app.debug = env.get('debug', 'debug') # 开启调式模式
    app.run(host='0.0.0.0')