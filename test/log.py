# -*- coding: UTF-8 -*- 
from flask import Flask, url_for, request # 处理url
from flask import render_template, redirect # 页面输出跳转
from flask import abort, make_response # 页面相应操作
from flask import session # 会话 
import os, datetime, random, json # 系统 时间 随机
from flaskext.mysql import MySQL # 数据库

app = Flask(__name__)
APP_PATH = os.getcwd() # 根路径
UPLOAD_FOLDER = APP_PATH + '/upload' # 上传路径

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'logger'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/mysql_conn')
def mysql_conn():
    cursor = mysql.connect().cursor()
    sql = "SELECT * FROM log"
    cursor.execute(sql)
    data = cursor.fetchone()
    return json.dumps(data, ensure_ascii=False, encoding='UTF-8')

if __name__ == '__main__':
    app.secret_key = 'dc1d71bbb5c4d2a5e936db79ef10c19f'
    app.debug = True # 开启调式模式
    app.run(host='0.0.0.0')