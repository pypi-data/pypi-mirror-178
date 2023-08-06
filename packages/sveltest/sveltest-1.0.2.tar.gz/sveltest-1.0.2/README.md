[GitHub]() | [Gitee]() 

# sveltest 



> sveltest 是一个底层核心基于unittest扩展的，集成式框架、包含自动化测试模块、应用服务器、应用开发工具等
> 该`sveltest `框架使编写测试脚本变得容易、快捷，支持创建复杂的测试。

## Features

1、完善的sveltest CLI工具(支持自动打开官方教程，创建自动化测试项目，运行自动化等)。

2、与unittest无间隙对接、提供更为复杂的TestCase类。

3、更为丰富的测试报告，HTML格式报告输出，以及丰富的测试开发调试信息。

4、更为丰富的参数化管理(数据随机化、可定制化、数据库参数化等)。

5、自动化下载驱动，无需自行去下载驱动程序一切操作均 sveltest 由来操作。

6、提供多种控制器来协助你完成自动化工作，如API测试时可使用认证器(auth)来满足登录依赖需求自动在以后每次的请求中带上token。

7、内置丰富的数据持久化缓存机制，缓存数据更多选择。

8、支持HTTP/WEB UI/APP UI等全栈式测试。

9、提供sveltest特色ORM来操作数据库，让你告别原生SQL的束缚



# install

> 下载最新版本

```shell
pip install sveltest
```

> 下载指定版本

```shell
pip install sveltest==0.12.3
```



# 快速开始


## CLI工具的使用

**查看帮助**

```bash
slt -h
```

```
usage: sveltest [-h] [-ui UI] [-api API] [-p PORT] [-run RUN] [-v] [create] [run] [runserver] [doc]

==================sveltest-CLI==================

positional arguments:
  create                创建工程
  run                   运行脚本
  runserver             运行服务
  doc                   浏览器打开sveltest 官方文档

optional arguments:
  -h, --help            show this help message and exit
  -ui UI                创建ui自动化工程项目模板
  -api API              创建api自动化工程项目模板
  -p PORT, --port PORT  指定端口号
  -run RUN              运行服务
  -v, --version         查看版本

====================sveltest====================
```

**创建项目**

```python
slt create -ui testdemo #创建WebDriver自动化测试项目
slt create -api testdemo #创建HTTP/HTTPS接口自动化测试项目
```



目录结构(以webdriver测试为例)：

> 具有`django style` 的工程项目

```python
│  manage.py # 项目主程序，非DEBUG模式下的项目启动文件
├─case # 存放测试用例集
│      test_baidu.py
├─common # 可进行存放一些自己封装的公共方法
├─pages # POM模式的page元素存放
│      BaiduElement.py
├─report # 测试报告存放
│  ├─html
│  └─logs
└─testdemo # 与项目名称相同，存放整个项目相关配置
        PageBase.py
        settings.py

```

**运行项目**

> sveltest在默认情况下为调试模式(DEBUG)，因此sveltest的执行方式有二种情况。

第一种：在单个测试用例模块下执行，次时不能直接在PyCharm右键运行需要额外配置，具体可查看[官方教程](https://sveltest-team.github.io/docs/unit/execute_test.html)

执行的结果

```

================================ 用例开始执行 =================================
test_case_demo (__main__.TestDemoTo1)   PASS
******************************** 测试结果汇总 *********************************
     执行结果     
┌────────┬───────┐
│ status │ count │
├────────┼───────┤
│ PASS   │ 1     │
│ FAIL   │ 0     │
│ SKIP   │ 0     │
│ ERROR  │ 0     │
│ COUNT  │ 1     │
└────────┴───────┘
================= 总共运行了 1 条测试用例  总共运行了 0.000s ==================
```



第二种：直接运行项目manage.py文件

运行后的结果

```
[ WARNING ] - 2022-11-23 10:24:01 - commandline.py:90 - 测试结果输出存放的目录不存在，正在创建该目录
[ SUCCESS ] - 2022-11-23 10:24:01 - commandline.py:92 - 创建成功，创建的目录路径为：F:/demo/testdemo/report/html/2022-11-23
[ SUCCESS ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1038 - test_search (test_baidu.BaiduTestUi) PASS
[ SUCCESS ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1412 - 测试结果：test_baidu.BaiduTestUi 测试集-总用例：1-成功：1-失败：0-异常：0-跳过：0
[ INFO ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1454 - 本次测试总用例数: 1
[ INFO ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1456 - 执行通过的用例数: 1
[ INFO ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1457 - 执行失败的用例数: 0
[ INFO ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1458 - 执行错误的用例数: 0
[ INFO ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1459 - 跳过的用例数为: 0
[ INFO ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1460 - 测试执行通过率: 100.00%
[ SUCCESS ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1179 - 本次测试已完成，总运行时间：0:00:05.376622
[ INFO ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1180 - 正在统计测试结果并生成测试报告...
[ SUCCESS ] - 2022-11-23 10:24:06 - htmlTestRunner.py:1181 - 测试统计报告已完成，输出的测试报告位置在：F:/demo/testdemo/report/html/2022-11-23/自动化测试报告_2022-11-23.html
[ INFO ] - 2022-11-23 10:24:06 - commandline.py:120 - 正在为你创建测试结果打包存放目录,F:/demo/testdemo/report/zip
[ SUCCESS ] - 2022-11-23 10:24:06 - commandline.py:125 - 创建目录成功
[ INFO ] - 2022-11-23 10:24:06 - commandline.py:128 - 已对目录路径为：F:/demo/testdemo/report/html,下的文件进行打包成zip文件,存放路径为：F:/demo/testdemo/report/zip/自动化测试报告_2022-11-23.zip
```



## 支持参数化

字符串参数化实例：

```python
from sveltest import TestCase
from sveltest import main
from pages.BaiduElement import BaiduUi
from selenium import webdriver
from sveltest.core import  parameterized,char

@parameterized
class BaiduTestUi(TestCase):

    def setUp(self):
        self.driver = BaiduUi(driver=webdriver.Chrome(),path="https://www.baidu.com/")


    @char("全栈自动化","人生苦短，我用Python")
    def test_search(self,text):
        print(text)
        self.driver.search_test(val=text)



    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    main(debug=True,verbosity=3)

```

内置参数化、提供多种可能性选择如：随机数据、自定义参数、数据库读取、文件数据读取等

```
================================ 用例开始执行 =================================
test_baidu.py    test_search_1 (__main__.BaiduTestUi)   PASS
test_baidu.py    test_search_2 (__main__.BaiduTestUi)   PASS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 调试输出 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
test_baidu.py.test_search_1【output】：
 全栈自动化


test_baidu.py.test_search_2【output】：
 人生苦短，我用Python


******************************** 测试结果汇总 *********************************

     执行结果     
┌────────┬───────┐
│ status │ count │
├────────┼───────┤
│ PASS   │ 2     │
│ FAIL   │ 0     │
│ SKIP   │ 0     │
│ ERROR  │ 0     │
│ COUNT  │ 2     │
└────────┴───────┘
================= 总共运行了 2 条测试用例  总共运行了 8.174s ==================
```

数据扩展参数化(支持元组，列表)

> 支持多个列表组来完成数据驱动生成多条测试用例

```python
from sveltest import TestCase
from sveltest import main
from sveltest.core import  parameterized,extends

@parameterized
class parameterizedTest(TestCase):

    def setUp(self):
        pass


    @extends(["全栈自动化","人生苦短，我用Python"])
    def test_search(self,a,b):
        print(a,b)



    def tearDown(self):
        pass


if __name__ == '__main__':
    main(debug=True,verbosity=3)
```

执行结果

```
================================ 用例开始执行 =================================
test_baidu.py    test_search_1_全栈自动化 (__main__.parameterizedTest)   PASS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 调试输出 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
test_baidu.py.test_search_1_全栈自动化【output】：
 全栈自动化 人生苦短，我用Python


******************************** 测试结果汇总 *********************************

     执行结果     
┌────────┬───────┐
│ status │ count │
├────────┼───────┤
│ PASS   │ 1     │
│ FAIL   │ 0     │
│ SKIP   │ 0     │
│ ERROR  │ 0     │
│ COUNT  │ 1     │
└────────┴───────┘
================= 总共运行了 1 条测试用例  总共运行了 0.001s ==================
```



```python
from sveltest import TestCase
from sveltest import main
from sveltest.core import  parameterized,extends

@parameterized
class parameterizedTest(TestCase):

    def setUp(self):
        pass


    @extends(["全栈自动化",],["人生苦短，我用Python"])
    def test_search(self,a):
        print(a)



    def tearDown(self):
        pass


if __name__ == '__main__':
    main(debug=True,verbosity=3)
```



```
================================ 用例开始执行 =================================
test_baidu.py    test_search_1_全栈自动化 (__main__.parameterizedTest)   PASS
test_baidu.py    test_search_2_人生苦短，我用Python 
(__main__.parameterizedTest)   PASS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 调试输出 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
test_baidu.py.test_search_1_全栈自动化【output】：
 全栈自动化


test_baidu.py.test_search_2_人生苦短，我用Python【output】：
 人生苦短，我用Python


******************************** 测试结果汇总 *********************************

     执行结果     
┌────────┬───────┐
│ status │ count │
├────────┼───────┤
│ PASS   │ 2     │
│ FAIL   │ 0     │
│ SKIP   │ 0     │
│ ERROR  │ 0     │
│ COUNT  │ 2     │
└────────┴───────┘
================= 总共运行了 2 条测试用例  总共运行了 0.001s ==================
```

更多的参数化操作可前往教程文档进行查看。



## 文档

有关完整文档，包括安装、教程和 PDF 文档，请参阅  https://sveltest-team.github.io/docs/












​			
