#!/usr/bin/env python
#-*- coding:utf-8 -*-

# authors:guanfl
# 2022/11/25

from selenium import webdriver
#
# option= webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=option)
#
# option.add_experimental_option("excludeSwitches", ["enable-automation"])
#
# option.add_experimental_option('useAutomationExtension', False)
# print(option.arguments) # 返回已设置的浏览器配置参数列表
# res = driver.execute_cdp_cmd('Page.captureScreenshot', {}) # 第一个是cmd 第二个是cmd 的参数
# driver.quit()
#



import time
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# # 加载用户配置
# options = Options()
# 设置成用户自己的数据目录
# options.add_argument(r'--user-data-dir=C:\Users\Admin\AppData\Local\Google\Chrome\User Data')
# options.add_argument(r'--window-size=500,50')

# url = 'https://blog.csdn.net'
# driver = webdriver.Chrome(options=options)
# driver.get(url)
# time.sleep(5)
# driver.quit()




# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# options = Options()
# # 设置中文编码格式
# options.add_argument('lang=zh_CN.UTF-8')
# options.add_argument('Host=www.baidu666.com')
# # 通过设置user-agent，用来模拟移动设备
# options.add_experimental_option("excludeSwitch",{
#
# }) #设置最小尺寸
# driver = webdriver.Firefox()
# print(options.arguments)
#
# driver.get('https://baidu.com')
# time.sleep(40)
# driver.quit()

# from selenium import webdriver
#
# options = webdriver.ChromeOptions()
#
# options.add_experimental_option('androidPackage', 'com.android.chrome')
#
# driver = webdriver.Chrome(options=options)
#
# driver.get('https://google.com')
#
# driver.quit()


from selenium import webdriver
import time

# 实例化 webdriver
browser = webdriver.Chrome()
# 最大浏览器尺寸
browser.maximize_window()

# browser.fullscreen_window()
# 浏览器输入url，并传送至指定的url页面
browser.get(url="http://127.0.0.1:8066/")

login_btn = browser.find_element_by_id("login-btn")
login_btn.click()
username = browser.find_element_by_id('username')
pwd = browser.find_element_by_id('password')
btu = browser.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div[2]/button')
username.send_keys("13453001")
pwd.send_keys("123456")
btu.click()

time.sleep(10)
browser.quit()
