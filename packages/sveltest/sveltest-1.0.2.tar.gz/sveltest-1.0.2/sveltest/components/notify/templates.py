#!/usr/bin/env python
#-*- coding:utf-8 -*-

# authors:guanfl
# 2022/11/22



MAKE_TEMPLATES = {
    0:"# <font color='#dd0000'>{{title}}</font><br />\n > <font color='#007adf'>  {{describe}}</font>\n\n"
      "## ------ 测试基本信息 ------\n\n"
      "### 本次测试环境:{% if run_env=='SIT' %} <font color='#0acffe'>{{run_env}}</font>{% elif run_env=='UAT' %} <font color='#00dd00'>{{run_env}}</font> {% endif %}\n\n"
      "### 测试人员:{% for item in tester %}{% if loop.last %} {{ item }}{%else%} {{ item }}, {% endif %}{% endfor %}\n"
      "### 本轮测试用例总数量：{{count_case}}\n### 本次测试执行通过率：{{pass_rate}}\n### 开始时间：{{start_time}}\n### 运行时长：{{run_time}}\n"
      "## ------ 用例执行结果统计 ------\n\n"
      "|  <font color='#dd0000'>status</font> | <font color='#dd0000'>count</font> |\n"
      "| ------ | ----- |\n"
      "| PASS   |    {{pass_count}}   | \n"
      "| FAIL   |   {{fail_count}}    |\n"
      "| SKIP   |  {{skip_count}}     |\n"
      "| <font color='#dd0000'>ERROR</font> ||   <font color='#dd0000'>{{error_count}}</font>| \n"
      "| COUNT  |  {{count_case}}    | \n\n"
      "\n\n\n**测试报告生成完成**-存放路径为：{{result_file_path}}"
  ,
}

# 0acffe
# 007adf

# 浅红色文字：<font color="#dd0000">浅红色文字：</font><br />
# 深红色文字：<font color="#660000">深红色文字</font><br />
# 浅绿色文字：<font color="#00dd00">浅绿色文字</font><br />
# 深绿色文字：<font color="#006600">深绿色文字</font><br />
# 浅蓝色文字：<font color="#0000dd">浅蓝色文字</font><br />
# 深蓝色文字：<font color="#000066">深蓝色文字</font><br />
# 浅黄色文字：<font color="#dddd00">浅黄色文字</font><br />
# 深黄色文字：<font color="#666600">深黄色文字</font><br />
# 浅青色文字：<font color="#00dddd">浅青色文字</font><br />
# 深青色文字：<font color="#006666">深青色文字</font><br />
# 浅紫色文字：<font color="#dd00dd">浅紫色文字</font><br />
# 深紫色文字：<font color="#660066">深紫色文字</font><br />
# background-image: linear-gradient(to top, #9be15d 0%, #00e3ae 100%);
