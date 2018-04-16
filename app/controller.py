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
        sql = " SELECT * FROM `admin` WHERE `username` = '%s' AND `password` = '%s' " % (username, password)
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
    return render_template('log/list.html', version=version, username=admin['username'], current_url='/loglist')

# ajax 加载数据
@app.route('/ajaxlist', methods=['GET', 'POST'])
def getlist():
    data = {}
    page = request.values.get('page')
    pageSize = request.values.get('pageSize')
    start = (int(page) - 1) * int(pageSize)
    sql = " SELECT * FROM `log` ORDER BY `id` DESC LIMIT %s , %s " % (str(start), str(pageSize))
    countsql = " SELECT count(*) as cnt FROM log "
    countInfo = mysql.queryOnlyRow(countsql)
    logs = mysql.queryAll(sql)
    count = int(countInfo['cnt'])
    data['count'] = count
    data['current'] = int(page)
    if logs == None:
        data['logs'] = []
    else:
        data['logs'] = logs
    return json.dumps(data)

# ajax 搜索加载数据
@app.route('/ajaxsearch', methods=['GET', 'POST'])
def getsearchlist():
    searchkey = request.values.get('searchkey')
    if searchkey=='' or searchkey==None:
        return -1
    data = {}
    sql = "SELECT * FROM `log` WHERE MATCH (`uid`, `method`, `route`, `header`, `query`, `date`, `time`) AGAINST ('%s' IN BOOLEAN MODE)" % (searchkey)
    countsql = "SELECT count(*) as cnt FROM `log` WHERE MATCH (`uid`, `method`, `route`, `header`, `query`, `date`, `time`) AGAINST ('%s' IN BOOLEAN MODE)" % (searchkey)
    countInfo = mysql.queryOnlyRow(countsql)
    logs = mysql.queryAll(sql)
    count = int(countInfo['cnt'])
    data['count'] = count
    data['current'] = 1
    if logs == None:
        data['logs'] = []
    else:
        data['logs'] = logs
    return json.dumps(data)

# 获取线性压力图
@app.route('/pv')
def pv():
    json_admin = redis.get(env.get('cache_key', 'logadminsession'));
    if json_admin == None :
        return redirect(url_for('login'))
    admin = json.loads(json_admin)
    # 获取线性分布图数据
    sql = "SELECT `date`, count(*) AS pv FROM `log` GROUP BY `date`"
    data = mysql.queryAll(sql)
    jsondata = json.dumps(data, ensure_ascii=False)
    return render_template('log/pv.html', version=version, username=admin['username'], jsondata=jsondata, current_url='/pv')

# 接收日志信息请求
@app.route('/logapi', methods=['GET', 'POST'])
def logapi():
    if request.method == 'GET':
        data = {}
        data['status'] = -1
        data['message'] = u'传递方式错误'
        return json.dumps(data)
    uid = request.values.get('uid') # 用户id
    method = request.values.get('method') # 传参方式
    route = request.values.get('route') # 路由
    header = request.values.get('header') # 头信息 
    query = request.values.get('query') # 参数 ?x=y&a=b
    date = request.values.get('date') # 日期 Y-m-d
    time = request.values.get('time') # 时间 H:i:s
    if uid=='' or method=='' or route=='' or header=='' or date=='' or time=='':
        data = {}
        data['status'] = -2
        data['message'] = u'必填参数不能为空'
        return json.dumps(data)
    # 队列操作 该位置将信息存储到redis的队列中
    loginfo = {}
    loginfo['uid'] = uid
    loginfo['method'] = method
    loginfo['route'] = route
    loginfo['header'] = header
    loginfo['query'] = query
    loginfo['date'] = date
    loginfo['time'] = time
    logstr = json.dumps(loginfo)
    redis.lpush(env.get('cache_key', 'logcachekey'), logstr)
    data = {}
    data['status'] = 1
    data['message'] = u'操作OK'
    return json.dumps(data)


# 循环在队列中获取多个信息，并将其保存到数据库
# 该操作将其放入定时任务中按一定频次执行
# TODO 未完待续... 将其修改成循环获取30个 sql处理成一次多个加入数据库
@app.route('/logloop')
def logloop():
    sql = " INSERT INTO `log` (`uid`, `method`, `route`, `header`, `query`, `date`, `time`) VALUES "
    log_sql_list = []
    for x in xrange(0, 30):
        log_json = redis.lpop(env.get('cache_key', 'logcachekey'))
        log = json.loads(log_json)
        uid = log['uid']
        method = log['method']
        route = log['route']
        header = log['header']
        query = log['query']
        date = log['date']
        time = log['time']
        log_sql_point = "('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (uid,method,route,header,query,date,time)
        log_sql_list.append(log_sql_point)
    sql = sql + ','.join(log_sql_list)
    mysql.query(sql)
    return log_json

# [ 启动项 ]
if __name__ == '__main__':
    app.secret_key = env.get('secret_key', 'key') # session会使用到
    app.debug = env.get('debug', 'debug') # 开启调式模式
    app.run(host='0.0.0.0')
