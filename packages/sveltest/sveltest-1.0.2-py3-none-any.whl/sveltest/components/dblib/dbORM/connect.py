#!/usr/bin/env python
#-*- coding:utf-8 -*-
import logging

import pymysql
from typing import Optional,Dict,List,Union
from sveltest.bin.conf import settings
from sveltest.support.common import ObjectDict

LOGGER = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)
class DBConnect(object):
    """
    数据库连接驱动
    """

    def __init__(self,user:Optional[str]=None,database:Optional[str]=None,
                 password:Optional[Union[str,int]]=None,
                 port:Optional[Union[str,int]]=3306,charset:Optional[str]="utf8",
                 host:Optional[str]="127.0.0.1",
                 driver:Optional[str]="sveltest.mysql"
                 ):
        """
        v1.0
        使用pymysql可配置的相关参数，后续将陆续完成下述所有参数配置
        password='',        # 密码
        database=None,      # 要连接的数据库
        port=0,             # 端口，一般为 3306
        unix_socket=None,   # 选择是否要用unix_socket而不是TCP/IP
        charset='',         # 字符编码
        sql_mode=None,      # Default SQL_MODE to use.
        read_default_file=None, # 从默认配置文件(my.ini或my.cnf)中读取参数
        conv=None,          # 转换字典
        use_unicode=None,   # 是否使用 unicode 编码
        client_flag=0,      # Custom flags to send to MySQL. Find potential values in constants.CLIENT.

        init_command=None,  # 连接建立时运行的初始语句
        connect_timeout=10, # 连接超时时间，(default: 10, min: 1, max: 31536000)
        ssl=None,           # A dict of arguments similar to mysql_ssl_set()'s parameters.For now the capath and cipher arguments are not supported.
        read_default_group=None, # Group to read from in the configuration file.
        compress=None,      # 不支持
        named_pipe=None,    # 不支持
        no_delay=None,      #
        autocommit=False,   # 是否自动提交事务
        db=None,            # 同 database，为了兼容 MySQLdb
        passwd=None,        # 同 password，为了兼容 MySQLdb
        local_infile=False, # 是否允许载入本地文件
        max_allowed_packet=16777216, # 限制 `LOCAL DATA INFILE` 大小
        defer_connect=False, # Don't explicitly connect on contruction - wait for connect call.
        auth_plugin_map={}, #
        read_timeout=None,  #
        write_timeout=None,
        bind_address=None   # 当客户有多个网络接口，指定一个连接到主机

        """

        LOGGER.debug(f"sveltest orm start connect ...")


        self.database_node ="default"
        if settings.DATABASES:
            settings_conf = ObjectDict(settings.DATABASES[self.database_node])
            self.host = settings_conf.HOST
            self.user = settings_conf.USER
            self.database = settings_conf.NAME
            self.charset = charset
            self.password = settings_conf.PASSWORD
            self.port = settings_conf.PORT
            self.driver = settings_conf.ENGINE
            if settings_conf.OPTIONS:
                options_conf = ObjectDict(settings_conf.OPTIONS)
                self.charset = options_conf.charset
            LOGGER.debug(f"node {self.database_node} | config {settings.DATABASES}")

        else:
            LOGGER.debug(f"非sveltest 集成模式启动sveltest orm")
            self.host = host
            self.user = "root"
            self.database = "data"
            self.charset = charset
            self.password = "gfl123456"
            self.port = port
            self.driver = driver



    def connect_db(self):
        """
        内置的数据库驱动连接
        :return:
        """
        if self.driver == "sveltest.mysql":
            LOGGER.debug(f"host={self.host}, user={self.user}, database={self.database}, charset={self.charset},password={self.password}, port={self.port}")
            return pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                port=self.port,

            )


# 为了后续兼容
db_connect = DBConnect



