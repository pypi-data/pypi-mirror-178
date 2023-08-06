#!/usr/bin/env python
#-*- coding:utf-8 -*-

# authors:guanfl
# 2022/11/25
from sveltest import models

models.sessionmaker.port = 3306
models.sessionmaker.host = "127.0.0.1"
models.sessionmaker.user = "root"
models.sessionmaker.database = "data"
models.sessionmaker.charset = "utf8"
models.sessionmaker.password = "gfl123456"



class SveltestModel(models.BaseModel):

    id = models.AutoField(
    )

    class Meta:
        # 用于定义额外的配置
        table = "sveltest_model"

if __name__ == '__main__':
    SveltestModel().create_db()
