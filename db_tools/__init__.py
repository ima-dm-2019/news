import pymysql

host = 'localhost'
user = 'root'
password = '123456'
port = 3306


class MyDBM:
    def __init__(self):
        self.database = pymysql.connect(host=host, user=user, password=password, port=port)
        self.handler = self.database.cursor()
        self.use_database()

    def use_database(self, database='news'):
        if not self.handler.execute(f"select * from information_schema.SCHEMATA where SCHEMA_NAME='{database}'"):
            self.handler.execute(f"create database {database}")  # 先建立再选定
        self.handler.execute(f'use {database};')

    def is_exits_table(self, table):
        '''判断某天的数据表是否存在'''
        self.handler.execute('show tables;')
        tables = self.handler.fetchall()
        return (table, ) in tables

