#!/usr/bin/env python
#-*- coding:utf-8 -*-

# authors:guanfl
# 2022/10/19


from peewee import *

# test 指的数据库名称，host 指 MySql 主机地址，port 指 MySql 端口，user 用户名，password 密码
db = MySQLDatabase('test', host='127.0.0.1', port=3306, user='root', password='123456')


class BaseModel(Model):
    class Meta:
        database = db  # 将实体与数据库进行绑定


# 继承自 BaseModel，直接关联 db，并且也继承了 Model，Model 提供增删改查的函数
class Person(BaseModel):
    name = CharField(verbose_name='姓名', max_length=10, null=False, index=True)
    passwd = CharField(verbose_name='密码', max_length=20, null=False, default='111111')
    gender = IntegerField(verbose_name='性别', null=False, default=1)
    is_admin = BooleanField(verbose_name='是否是管理员', default=False)


if __name__ == "__main__":
    # 查询数据库是否连接
    db.is_closed()
    # 连接数据库
    db.connect()
    # 创建table
    Person.create_table()
