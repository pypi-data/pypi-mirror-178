#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
用于对群机器人自动发送报告进行封装的方法,钉钉开放平台：
https://open.dingtalk.com/document/group/receive-message
"""

# authors:guanfl
# 2022/11/22
import os
import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import (Sequence, Tuple, Optional, List, Text, Union)
from sveltest.bin.conf import settings
from sveltest.components.jinja_template import StringTemplate
from sveltest.components.notify.templates import MAKE_TEMPLATES
from sveltest.support.common import ObjectDict
from sveltest.components.network.main import RequestBase

DINGTALKOAPO = "https://oapi.dingtalk.com/robot/send?access_token={access_token}"

DINGDING_WEBHOOK = {
    "URL": "https://oapi.dingtalk.com/robot/send?access_token={}",
    "SECRET": "SECf204470dbbd151188c50bb903ee1a57e6396a3a3e52288af8749d0744daa50e6",
    "KEYWORD": "自动化测试报告",
}

ding_temp = StringTemplate(MAKE_TEMPLATES)


class DingTalkClient:
    def __init__(self):
        self.ret = RequestBase()
        self.dingding = ObjectDict(settings.DINGDING_WEBHOOK)


    def __get_string(self,field_type:Optional[int]=0):
        """

        """

        return ding_temp.get_string(field_type)

    def __signature(self, secret: Optional[str]) -> Tuple:
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def __join_url(self) -> str:
        """拼接完整的url"""

        if self.dingding:
            hmac_code, sign = self.__signature(self.dingding.SECRET)
            join_sign = f"&timestamp={hmac_code}&sign={sign}"
            return self.dingding.URL + join_sign

    def send_text(self, text: Optional[Text], phone: List = None, userid: List = None, isat: bool = False):
        """发送文本类型
        Args:
           isat:是否进行全员@
           content:文本
           phone:发送人的手机号
           userid:发送人的用户id
        Returns:
            example:
        Raises:
        """
        try:
            data = {"at": {"atMobiles":  # @人的手机号码
                               phone, "atUserIds": userid,  # @的用户id
                           "isAtAll": isat  # 是否艾特所有人
                           },
                    "text": {
                        "content": text
                    },
                    "msgtype": "text"
                    }
            re = self.ret.post(router=self.__join_url(), data=data, env_control=False)
            return re, 0
        except:
            return 1

    def send_image_msg(self, photoURL:Optional[str], phone: list = None, userid: list = None, isat=False):
        """发送图片类型
        Args:
           isat:是否进行全员@
           photoURL:支持在线图片链接，也支持本地文件路径
           phone:发送人的手机号
           userid:发送人的用户id
        Returns:
            example:
        Raises:
        """
        try:
            data = {"at": {"atMobiles":  # @人的手机号码
                               phone, "atUserIds": userid,  # @的用户id
                           "isAtAll": isat  # 是否艾特所有人
                           },
                    'photo': {
                        "photoURL": photoURL,
                    },
                    "msgtype": "photo"
                    }

            re = self.ret.post(router=self.__join_url(), data=data, env_control=False)
            return re, 0
        except:
            return 1


    def send_markdown(self, title:str, content:Optional[Text], phone:List= None, users: List = None):
        """发送markdown类型
        Args:
            title:标题
            content:文本
            phone:发送人的手机号
            users:发送人的用户名
        Returns:
            example:
        Raises:
        """
        data = {
            "msgtype": "markdown",
            "markdown": {"title": title, "text": content},
            "at": {"atMobiles": phone, "atUserIds": users, "isAtAll": False}}

        re = self.ret.post(router=self.__join_url(), data=data, env_control=False)
        return re, 0

    def send_link(self, link, text, title):
        """发送的内容中包含链接
        Args:
            title:标题
            content:文本
            link:链接
        Returns:
            example:
        Raises:
        """
        data = {
            "msgtype": "link",  # 类型为link类型
            "link": {"text": text,
                     "title": title, "picUrl": "",
                     "messageUrl": link
                     }
        }
        re = self.ret.post(router=self.__join_url(), data=data, env_control=False)
        return re, 0


    def templates(self, type: Optional[int] = 0):
        self.send_markdown(
            content=self.__get_string(type).render(title="sveltest 自动化测试dingtalk结果报告", describe="本次是JIDEAI+ 云端接口测试",run_env="SIT",
                                                 tester=["测试测试",2],count_case=100,pass_rate="99%",pass_count=25,skip_count=0,fail_count=1,error_count=2

        ),
            title="测试测试"
        )



"""
# {{title}}
"""


if __name__ == '__main__':
    d = DingTalkClient()
    # d.send_markdown(content="https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/a/RV0Dej1grUlPeWgb/0d950f02df1d4b57b0df1d1bd27326050521.png",title="测试测试")
    d.templates()


