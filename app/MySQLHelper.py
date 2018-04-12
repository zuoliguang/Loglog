#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import pymysql # 数据库

class MySQLHelper:
    version=0.1
    # 初始化
    def __init__(self, host, user, password, database, charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        try:  
            self.conn = pymysql.connect(self.host, self.user, self.password)
            self.conn.select_db(self.database)
            self.conn.set_charset(self.charset)
            self.cursor=self.conn.cursor()
        except Exception as e:  
            print ('MySql Error : %d %s' %(e.args[0],e.args[1]))  
    
    # 执行SQL 返回SQL的执行结果
    def query(self,sql):  
        try:  
            rows=self.cursor.execute(sql)  
            return rows;  
        except Exception as e:  
            print('MySql Error: %s SQL: %s'%(e,sql))  
 
    # 执行SQL 返回第一条记录
    def queryOnlyRow(self,sql):  
        try:  
            self.query(sql)  
            result=self.cursor.fetchone()  
            desc=self.cursor.description  
            row={}  
            for i in range(0,len(result)):  
                row[desc[i][0]]=result[i]  
            return row;  
        except Exception as e:  
            print('MySql Error: %s SQL: %s'%(e,sql))  

    # 返回SQL查询的所有结果
    def queryAll(self,sql):
        try:  
            self.query(sql)  
            result=self.cursor.fetchall()  
            desc=self.cursor.description  
            rows=[]  
            for cloumn in result:  
                row={}  
                for i in range(0,len(cloumn)):  
                    row[desc[i][0]]=cloumn[i]  
                rows.append(row)    
            return rows;  
        except Exception as e:  
            print('MySql Error: %s SQL: %s'%(e,sql))  

    # 向指定表插入数据
    def insert(self,tableName,pData):  
        try:  
            newData={}  
            for key in pData:  
                newData[key]="'""'"+pData[key]+"'"  
            key=','.join(newData.keys())  
            value=','.join(newData.values())  
            sql="insert into "+tableName+"("+key+") values("+value+")"  
            self.query("set names 'utf8'")  
            self.query(sql)  
            self.commit()  
        except Exception as e:  
            self.conn.rollback()  
            print('MySql Error: %s %s'%(e.args[0],e.args[1]))  
        finally:  
            self.close()  

    # 更新表数据
    def update(self,tableName,pData,whereData):  
        try:  
            newData=[]  
            keys=pData.keys()  
            for i in keys:  
                item="%s=%s"%(i,"'""'"+pData[i]+"'")  
                newData.append(item)  
            items=','.join(newData)  
            newData2=[]  
            keys=whereData.keys()  
            for i in keys:  
                item="%s=%s"%(i,"'""'"+whereData[i]+"'")  
                newData2.append(item)  
            whereItems=" AND ".join(newData2)  
            sql="update "+tableName+" set "+items+" where "+whereItems  
            self.query("set names 'utf8'")  
            self.query(sql)  
            self.commit()  
        except Exception as e:  
            self.conn.rollback()  
            print('MySql Error: %s %s'%(e.args[0],e.args[1]))  
        finally:  
            self.close()  

    def getLastInsertRowId(self):  
        return self.cursor.lastrowid  

    def getRowCount(self):  
        return self.cursor.rowcount  

    def commit(self):  
        self.conn.commit()  

    def close(self):  
        self.cursor.close()  
        self.conn.close()


