import click


"""


                   _  _              _
                  | || |            | |
  ___ __   __ ___ | || |_  ___  ___ | |_
 / __|\ \ / // _ \| || __|/ _ \/ __|| __|
 \__ \ \ V /|  __/| || |_|  __/\__ \| |_
 |___/  \_/  \___||_| \__|\___||___/ \__|



sveltest

"""

import argparse
import os
import sys

from sveltest.support import StFile
from sveltest.support import ReNumber
from sveltest.bin.conf.base import BASE_DIRs

st_os = StFile()

"""
v1.0.2
guanfl
20220926
"""
from sveltest.version import version, updateTime

version_ = ''
if sys.platform == "win32" or sys.platform != "Linux":
    version_ = f"sveltest@Windows {version}  win32_x86\nUpdateTime:{updateTime}\nversion: {version}"
else:
    version_ = f"sveltest@Linux {version}  Linux32 \nUpdateTime:{updateTime}\nversion: {version}"

# try:
text_logo = """
                       _  _              _
                      | || |            | |
      ___ __   __ ___ | || |_  ___  ___ | |_
     / __|\ \ / // _ \| || __|/ _ \/ __|| __|
     \__ \ \ V /|  __/| || |_|  __/\__ \| |_
     |___/  \_/  \___||_| \__|\___||___/ \__|



sveltest 专注于让自动化更简洁、更简单、高效率！！！
输入 slt -h 命令你可以进行查看 sveltest cli的所有命令哦。

你也可以进行浏览器输入 sveltest 官方教程文档 ： https://sveltest-team.github.io/docs/
那么我们开始体验下吧！！！
"""




@click.group(invoke_without_command=True)
@click.option('-v/--version', default=False,help="查看版本")

@click.pass_context
def sveltest_cli_tools(ctx,v):

    # print(ctx.get_help())
    if v:
        click.echo(version_)
        # print(text_logo)
    # if ctx.invoked_subcommand is None:
    #     print (ctx.get_help())
    # else:
    #     print('gonna invoke %s' % ctx.invoked_subcommand)


@sveltest_cli_tools.command(help='浏览器打开sveltest 官方文档')

def doc():
    """浏览器打开sveltest 官方文档"""
    os.system("start https://sveltest-team.github.io/docs/")

@sveltest_cli_tools.command()
@click.option('-ui/--webui', default=False,help="创建web/app UI自动化工程")
@click.option('-api/--interface', default=False,help="创建Http api自动化工程")
def create():
    """创建工程"""

@sveltest_cli_tools.command()
def run():
    """运行脚本"""

@sveltest_cli_tools.command()

def runserver():
    """运行demo服务"""


# Object.defineProperty(navigator, 'webdriver', {
#     get: () => false,
#   });



if __name__ == '__main__':
    sveltest_cli_tools()
