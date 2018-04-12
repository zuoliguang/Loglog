#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import redis

class RedisHelper:
    version=0.1  
    # 初始化
    def __init__(self, host, port=6379):
        self.config = {
            'host' : host,
            'port' : port
        }
        self.pool = redis.ConnectionPool(**self.config) # 使用连接池
        self.r = redis.Redis(connection_pool=self.pool)
    
    def handler(self):
        return self.r