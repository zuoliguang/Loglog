# -*- coding: UTF-8 -*- 
from flask import Flask, url_for, request # 处理url
from flask import render_template, redirect # 页面输出跳转
from flask import session, escape # 会话 
from flask import flash # 闪现 
import os, json, datetime, random, md5, math # 系统 时间 随机 ...
from PIL import Image # 图片

import ConfigParser as cp
from MySQLHelper import *
from RedisHelper import *

app = Flask(__name__)

# [ 系统版本 ]
version = 1.0

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

# [ page 参数 ]
pageSize = 2

# [ 控制器 业务逻辑部分 ]
# 首页
@app.route('/')
def index():
    json_admin = redis.get(env.get('cache_key', 'logadminsession'));
    if json_admin == None :
        return redirect(url_for('login'))
    admin = json.loads(json_admin)
    return render_template('log/index.html', version=version, username=admin['username'])

# 登录页面
@app.route('/login')
def login():
    return render_template('log/main/login.html')

# 身份验证
@app.route('/do_login', methods=['GET', 'POST'])
def doLogin():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form :
            return render_template('log/main/login.html', error_info=u'用户名、密码不能为空!')
        username = request.form['username']
        pwd = request.form['password']
        # md5 密码
        m1 = md5.new()
        m1.update(pwd.encode(encoding='utf-8'))
        password = m1.hexdigest()
        sql = " SELECT * FROM admin WHERE username = '%s' AND password = '%s' " % (username, password)
        admin = mysql.queryOnlyRow(sql)
        if admin == None :
            return render_template('log/main/login.html', error_info=u'用户名、密码错误!')
        else:
            # 登录操作
            redis.set(env.get('cache_key', 'logadminsession'), json.dumps(admin), 3600)
            return redirect(url_for('index'))
    else:
        return render_template('log/main/login.html', error_info=u'请求错误!')

# 退出
@app.route('/logout')
def logout():
    redis.delete(env.get('cache_key', 'logadminsession'))
    return redirect(url_for('index'))

# 日志列表
@app.route('/loglist')
def loglist():
    json_admin = redis.get(env.get('cache_key', 'logadminsession'));
    if json_admin == None :
        return redirect(url_for('login'))
    admin = json.loads(json_admin)
    return render_template('log/list.html', version=version, username=admin['username'])

# ajax 加载数据
@app.route('/ajaxlist', methods=['GET', 'POST'])
def getlist():
    data = {}
    page = request.values.get('page')
    start = (int(page) - 1) * int(pageSize)
    sql = " SELECT * FROM log LIMIT %s , %s " % (str(start), str(pageSize))
    countsql = " SELECT count(*) as cnt FROM log "
    countInfo = mysql.queryOnlyRow(countsql)
    logs = mysql.queryAll(sql)
    count = int(countInfo['cnt'])
    data['count'] = count
    if logs == None:
        data['pages'] = 0
        data['logs'] = []
    else:
        data['pages'] = math.trunc(count / int(pageSize)) + 1
        data['logs'] = logs
    return json.dumps(data)

# [ 启动项 ]
if __name__ == '__main__':
    app.secret_key = env.get('secret_key', 'key') # session会使用到
    app.debug = env.get('debug', 'debug') # 开启调式模式
    app.run(host='0.0.0.0')