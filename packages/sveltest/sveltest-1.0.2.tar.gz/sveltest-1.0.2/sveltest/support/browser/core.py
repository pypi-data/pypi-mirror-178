#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import subprocess
import sys
import requests
import zipfile
import win32api
from selenium.webdriver.chrome.options import Options
from sveltest.support.logger_v2 import log_v2
from typing import (Optional, NoReturn, Generator, List, Sequence)
from datetime import datetime

ie = ["IE", 'Ie', 'ie']

#  xml
# https://registry.npmmirror.com/-/binary/chromedriver json
# https://registry.npmmirror.com/-/binary/geckodriver geckodriver 火狐  json
# https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver?delimiter=%2F&maxresults=100&restype=container&comp=list&_=1663815950611&timeout=60000

#  geckodriver edge  json
# href="https://msedgedriver.azureedge.net/44.19041.1266.0/edgedriver_win64.zip" edge


OPEN_DERVER_URL = {
    "XML": [
        {"CHROMEDRIVER": ["https://chromedriver.storage.googleapis.com/"]},
        {"IEDRIVERSERVER": ["https://selenium-release.storage.googleapis.com/"]},
    ],
    "JSON": ["https://registry.npmmirror.com/-/binary/{webdriver}"],
    "URL": ["https://msedgedriver.azureedge.net"]  # edge
}


class DownloadDriver:

    # 进行解压
    def _unzip(self, to_path: Optional[str], zip_file: Optional[str]) -> NoReturn:
        """
        解压Chromedriver压缩包到指定目录
        :param to_path:
        :param zip_file:
        :return:
        """
        f = zipfile.ZipFile(zip_file)
        for files in f.namelist():
            f.extract(files, to_path)

    # 配置不显示浏览器
    def head(self) -> Optional[object]:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(
            'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')
        return chrome_options

    def timestamp(self, timedate: Optional[str]) -> int:
        """
        :param shijian:
        :return:
        """
        s_t = time.strptime(timedate, "%Y-%m-%d %H:%M:%S")
        mkt = int(time.mktime(s_t))
        return (mkt)

    def get_driver_data(self, driver: Optional[str] = "chrome") -> Optional[Generator]:
        """

        :param driver:
        :return:
        """

        log_v2.info(f"当前正在搜索{driver}浏览器驱动")
        if driver in ie:

            url = OPEN_DERVER_URL["XML"][1]["IEDRIVERSERVER"][0]

        else:
            # xml
            url = OPEN_DERVER_URL["XML"][0]["CHROMEDRIVER"][0]

        log_v2.info(f"正在从 {url} 查找最新版本驱动程序...")

        _file = 'storage.xml'
        with open(_file, 'w', encoding="utf-8") as f:
            f.write(requests.get(url=url).text)
            f.close()

        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET

        tree = ET.parse(_file)

        # 获取根节点
        root = tree.getroot()
        if driver == "chrome":
            for x in root:
                if len(x) > 2:
                    ds = {}

                    for d in x:

                        d_ = str(d.text).split("/")
                        if d_[-1].startswith("chromedriver"):
                            ds["download"] = os.path.join(OPEN_DERVER_URL["XML"][0]["CHROMEDRIVER"][0], d.text)
                            ds["version"] = str(d.text).split("/")[0]
                        if d.tag.split("}")[-1] == "LastModified":
                            ds["updateTime"] = str(d.text).replace('T', ' ').split('.')[0]
                            ds["timestamp"] = int(self.timestamp(str(d.text).replace('T', ' ').split('.')[0]))

                    try:
                        if ds["download"]:
                            yield ds
                    except:
                        pass

        if driver in ie:
            for x in root:
                if len(x) > 2:
                    ds = {}

                    for d in x:

                        d_ = str(d.text).split("/")

                        if d_[-1].startswith("IEDriverServer"):
                            ds["download"] = os.path.join(OPEN_DERVER_URL["XML"][1]["IEDRIVERSERVER"][0], d.text)
                            ds["version"] = str(d.text).split("/")[0]

                        if d.tag.split("}")[-1] == "LastModified":
                            ds["updateTime"] = str(d.text).replace('T', ' ').split('.')[0]
                            ds["timestamp"] = int(self.timestamp(str(d.text).replace('T', ' ').split('.')[0]))

                    try:
                        if ds["download"]:
                            yield ds
                    except:
                        pass

    # 获取python安装路径
    def _get_python_path(self) -> str:
        """
        获取python安装路径
        :return:
        """
        try:
            p1 = subprocess.Popen("where python", stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode("gbk").split("\r")[0].replace("\\", "/")
        except:
            output = 0
        return output

    def _get_latest_version(self, driver: Optional[str] = "chrome") -> Optional[List]:
        """获取最新版本"""

        log_v2.info("正在搜索最新版本驱动" + driver)
        x = [x for x in self.get_driver_data(driver=driver)]

        x.sort(key=lambda s: s["timestamp"], reverse=True)

        if driver == "chrome":
            return x[:4]

        if driver in ie:
            return x[:4]

    def _get_latest_from_version(self, v: Optional[str], driver: Optional[str] = "chrome") -> Optional[List]:

        """根据指定的驱动版本从中进行获取最新版本驱动"""

        x = [x for x in self._get_version_driver(
            v=v,
            driver=driver
        )]
        x.sort(key=lambda x: x["timestamp"], reverse=True)
        return x[:4]

    def _get_version_driver(self, v, driver="chrome", ):
        """按照版本匹配"""
        x = [x for x in self.get_driver_data(driver=driver)]
        for s in x:
            if s["version"].startswith(v):
                yield s

    def platform(self, p: Optional[str] = "win32", driver: Optional[str] = 'chrome',
                 version: Optional[str] = None) -> List:
        """
        version :
        :paramp: chrome:linux64 mac64 mac64_m1 win32
                ie:x64 win32
        :return:
        """

        log_v2.debug(driver)
        if driver == "chrome":
            if version:

                for x in self._get_latest_from_version(
                        v=self._get_chrome_current_version().split(".")[0],
                        driver=driver
                ):
                    if x["download"].split("/")[-1].split('.')[0].endswith(p):
                        return x

            else:
                for x in self._get_latest_version(driver=driver):
                    if x["download"].split("/")[-1].split('.')[0].endswith(p):
                        return x
        if driver in ie:

            for x in self._get_latest_version(driver=driver):

                if x["download"].split("/")[-1].split('_')[1].lower() == p:
                    try:
                        log_v2.success(
                            f'已成功找到 IEDriverServer 驱动程序版本为：{x["download"].split("/")[-1].split("_")[-1].strip("zip").strip(".").lstrip(".")}')
                    except:
                        log_v2.success(
                            '已成功找到 IEDriverServer 驱动程序')
                    return x

    def download_driver(self, path_url, filename):
        # 判断输入的文件夹或路径是否真实存在

        log_v2.debug(f"{path_url}-{filename}")

        path = "d:/drivers"
        if sys.platform[:-2] == "win":
            try:
                log_v2.info("正在创建存放驱动目录")
                os.mkdir(path)

            except:
                pass
        log_v2.success("存放驱动目录已创建成功：" + path)
        file = requests.get(url=path_url)
        save = os.path.join(path, filename).replace("\\", "/")
        # 保存文件到脚本所在目录
        with open(save, 'wb') as zip_file:
            zip_file.write(file.content)
            log_v2.success("浏览器驱动下载成功...")
            return save

    def _download(self, p="win32", driver="chrome", version=None):

        v = self.platform(p=p, driver=driver, version=version)
        log_v2.debug(v)

        if v:

            save = self.download_driver(
                path_url=v["download"],
                filename=v["download"].split("/")[-1]
            )
            log_v2.info("驱动下载路径为：" + save)
            return save
        else:
            log_v2.error("没有找到合适版本的驱动程序")

    def _unzip_driver(self, zip_path):
        log_v2.info("正在解压压缩包：" + zip_path)
        zip_path_ = self._get_python_path().split("/")
        _path = '/'.join(zip_path_[:-1])
        self._unzip(_path, zip_file=zip_path)
        log_v2.info("解压完成,解压后存放的目录为：" + _path)

    def get_chrome_current_driver_version(self):
        """

        :return:
        """
        try:
            p1 = subprocess.Popen("chromedriver -version", stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(' ')
        except:
            output = 0
        return output

    def get_ie_current_driver_version(self):
        """

        :return:
        """
        try:
            p1 = subprocess.Popen("where IEDriverServer", stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode("gbk").split("\r")[0].replace("\\", "/")
            info = win32api.GetFileVersionInfo(output, os.sep)
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = '%d.%d.%d.%d' % (
                win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)
            )
        except Exception as e:
            version = 0
        return version

    def get_edge_current_driver_version(self):
        """

        :return:
        """
        try:
            p1 = subprocess.Popen("where msedgedriver", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p1.communicate()[0].decode("gbk").split("\r")[0].replace("\\", "/")
            info = win32api.GetFileVersionInfo(output, os.sep)
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = '%d.%d.%d.%d' % (
                win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)
            )
        except Exception as e:
            version = 0
        return version

    def get_firefox_current_driver_version(self):
        """
        获取当前ie浏览器
        :return:
        """
        try:
            p1 = subprocess.Popen('geckodriver -V',
                                  stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(" ")[:2]
        except:
            output = 0
        return output

    def _get_chrome_current_version(self):
        """
        获取当前chrome浏览器
        :return:
        """
        try:
            p1 = subprocess.Popen('reg query HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon /v version',
                                  stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(" ")[-1].strip()
        except:
            output = 0
        return output

    def _get_ie_current_version(self):
        """
        获取当前ie浏览器
        :return:
        """
        try:
            p1 = subprocess.Popen('reg query "HKLM\SOFTWARE\Microsoft\Internet Explorer" /v Version',
                                  stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(" ")[-1].strip()
        except:
            output = 0
        return output

    def _get_edge_current_version(self):
        """
        获取当前ie浏览器
        :return:
        """
        try:
            p1 = subprocess.Popen('reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\BLBeacon" /v version',
                                  stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(" ")[-1].strip()
        except:
            output = 0
        return output

    def open_chrome(self, p="win32"):

        x_ = self.get_chrome_current_driver_version()
        if x_ != 0:
            log_v2.warning("已存在 chromedriver 驱动，将进行查找最新浏览器驱动...")
            dr = self.get_chrome_current_driver_version()[1]
            br = self._get_chrome_current_version()
            if int(dr.split(".")[0]) == int(br.split(".")[0]):
                log_v2.info("当前Chrome 浏览器版本为" + br + " chromedriver驱动程序版本为：" + dr)
                log_v2.info("正在查找最新驱动...")
                lv = self.platform(p=p, driver='chrome', version=br.split(".")[0])["version"]
                log_v2.info("当前符合浏览器版本的驱动最新版本为：" + lv)
                if dr == lv:
                    log_v2.warning("当前驱动程序已是最新版本，跳过下载...")
                else:
                    self._unzip_driver(zip_path=lv)
            else:
                log_v2.info("当前Chrome 浏览器版本为" + br + " chromedriver驱动程序版本为：" + dr)
                self._unzip_driver(zip_path=self._download(
                    p=p,
                    version=self._get_chrome_current_version().split(".")[0],
                ))
        else:

            self._unzip_driver(zip_path=self._download(
                p=p,
                version=self._get_chrome_current_version().split(".")[0],
            ))

    def open_ie(self, p="win32"):

        x_ = self.get_ie_current_driver_version()
        br = self._get_ie_current_version()

        if x_ != 0:
            log_v2.warning("已存在 IEDriverServer 驱动，将进行查找最新浏览器驱动...")

            dr = self.get_ie_current_driver_version()

            log_v2.debug(br)
            if int(dr.split(".")[0]) == int(br.split(".")[0]):
                log_v2.info("当前IE 浏览器版本为" + br + " IEDriverServer驱动程序版本为：" + dr)
                log_v2.info("正在查找最新驱动...")
                lv = self.platform(p=p, driver='ie', version=br.split(".")[0])["version"]
                log_v2.info("当前符合浏览器版本的驱动最新版本为：" + lv)
                if dr == lv:
                    log_v2.warning("当前驱动程序已是最新版本，跳过下载...")
                else:
                    self._unzip_driver(zip_path=lv)
            else:

                log_v2.info("当前Ie 浏览器版本为" + br + " IEDriverServer驱动程序版本为：" + dr)
                self._unzip_driver(zip_path=self._download(
                    p=p,
                    version=self._get_ie_current_version().split(".")[0],
                    driver="ie"
                )
                )
        else:
            log_v2.info("当前系统未安装有 IEDriverServer驱动程序")
            self._unzip_driver(zip_path=self._download(
                p=p,
                version=self._get_ie_current_version().split(".")[0],
                driver="ie"
            )
            )


class JsonDownloadDriver(DownloadDriver):

    def _get_latest_version(self, driver="chrome"):
        """获取最新版本"""

        log_v2.info("正在搜索最新版本驱动" + driver)
        x = [x for x in self.get_driver_data(driver=driver)]
        # print()
        x.sort(key=lambda s: s["timestamp"], reverse=True)

        if driver == "chrome":
            return x[:4]

        if driver in ie:
            return x[:4]

    def _get_latest_from_version(self, v, driver="chrome"):

        """根据指定的驱动版本从中进行获取最新版本驱动"""

        x = [x for x in self._get_version_driver(
            v=v,
            driver=driver
        )]
        x.sort(key=lambda x: x["timestamp"], reverse=True)
        return x[:4]

    def _get_version_driver(self, v, driver="chrome", ):
        """按照版本匹配"""
        x = [x for x in self.get_driver_data(driver=driver)]
        for s in x:
            if s["version"].startswith(v):
                yield s

    def platform(self, p="win32", driver='chrome', version=None):
        """
        version :
        :paramp: chrome:linux64 mac64 mac64_m1 win32
                ie:x64 win32
        :return:
        """

        log_v2.debug(driver)
        if driver == "chrome":
            if version:

                for x in self._get_latest_from_version(
                        v=self._get_chrome_current_version().split(".")[0],
                        driver=driver
                ):
                    if x["download"].split("/")[-1].split('.')[0].endswith(p):
                        return x

            else:
                for x in self._get_latest_version(driver=driver):
                    if x["download"].split("/")[-1].split('.')[0].endswith(p):
                        return x
        if driver in ie:

            for x in self._get_latest_version(driver=driver):

                if x["download"].split("/")[-1].split('_')[1].lower() == p:
                    try:
                        log_v2.success(
                            f'已成功找到 IEDriverServer 驱动程序版本为：{x["download"].split("/")[-1].split("_")[-1].strip("zip").strip(".").lstrip(".")}')
                    except:
                        log_v2.success(
                            '已成功找到 IEDriverServer 驱动程序')
                    return x

    def download_driver(self, path_url, filename):
        # 判断输入的文件夹或路径是否真实存在
        path = "d:/drivers"
        if sys.platform[:-2] == "win":
            try:
                log_v2.info("正在创建存放驱动目录")
                os.mkdir(path)

            except:
                pass
        log_v2.success("存放驱动目录已创建成功：" + path)
        file = requests.get(url=path_url)
        save = os.path.join(path, filename).replace("\\", "/")
        # 保存文件到脚本所在目录
        with open(save, 'wb') as zip_file:
            zip_file.write(file.content)
            log_v2.success("浏览器驱动下载成功...")
            return save

    def _download(self, p="win32", driver="chrome", version=None):

        v = self.platform(p=p, driver=driver, version=version)
        log_v2.debug(v)

        if v:

            save = self.download_driver(
                path_url=v["download"],
                filename=v["download"].split("/")[-1]
            )
            log_v2.info("驱动下载路径为：" + save)
            return save
        else:
            log_v2.error("没有找到合适版本的驱动程序")

    def _unzip_driver(self, zip_path):
        log_v2.info("正在解压压缩包：" + zip_path)
        zip_path_ = self._get_python_path().split("/")
        _path = '/'.join(zip_path_[:-1])
        self._unzip(_path, zip_file=zip_path)
        log_v2.info("解压完成,解压后存放的目录为：" + _path)

    def get_chrome_current_driver_version(self):
        """

        :return:
        """
        try:
            p1 = subprocess.Popen("chromedriver -version", stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(' ')
        except:
            output = 0
        return output

    def get_ie_current_driver_version(self):
        """

        :return:
        """
        try:
            p1 = subprocess.Popen("where IEDriverServer", stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode("gbk").split("\r")[0].replace("\\", "/")
            info = win32api.GetFileVersionInfo(output, os.sep)
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = '%d.%d.%d.%d' % (
                win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)
            )



        except Exception as e:
            print(e)
            version = 0
        return version

    def _get_chrome_current_version(self):
        """
        获取当前chrome浏览器
        :return:
        """
        try:
            p1 = subprocess.Popen("reg query \"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon\" /v version",
                                  stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(" ")[-1].strip()
        except:
            output = 0
        return output

    def _get_ie_current_version(self):
        """
        获取当前ie浏览器
        :return:
        """
        try:
            p1 = subprocess.Popen('reg query "HKLM\SOFTWARE\Microsoft\Internet Explorer" /v Version',
                                  stdout=subprocess.PIPE)
            output = p1.communicate()[0].decode().split(" ")[-1].strip()
        except:
            output = 0
        return output

    def edge_platform(self, p: Sequence[str] = "win32", v: Sequence[str] = None) -> Sequence[str]:

        """
        arm64
        win64
        win32
        """
        u = os.path.join("https://msedgedriver.azureedge.net", f'{v}/edgedriver_{p}.zip').replace("\\", '/')
        return str(u)

    def _get_firefox_data(self):
        ret = requests.get(url=OPEN_DERVER_URL["JSON"][0].format(webdriver="geckodriver"))
        if ret.status_code == 200:
            for xt in ret.json():
                to_strptime = datetime.strptime(xt['date'].replace("T", " ").rstrip("Z"), '%Y-%m-%d %H:%M:%S')
                yield {"date": to_strptime.timestamp(), "name": "geckodriver", "url": xt["url"],
                       "version": xt["name"]}

        else:
            pass

    def get_firefox_latest(self):

        data = [x for x in self._get_firefox_data()]
        data.sort(key=lambda x: x["date"], reverse=True)

        ret = requests.get(url=data[0]["url"])

        if ret.status_code == 200:
            for xt in ret.json():

                v = data[0]["version"].rstrip("/")
                c_ = str(xt["name"].split(v)[-1])
                if c_.startswith("-"):

                    yield { "url": xt["url"],"platform":c_.lstrip("-").split(".")[0],
                           "version": data[0]["version"].rstrip("/")}
                else:

                    yield {"url": xt["url"], "platform": None,
                           "version": data[0]["version"].rstrip("/")}



        else:
            pass
        return

    def firefox_platform(self, p: Sequence[str] = "win32", v: Sequence[str] = None) -> Sequence[str]:

        """
        arm64
        win64
        win32
        """
        for xe in self.get_firefox_latest():
            if xe["platform"] == p:
                return xe["url"]


    def open_edge(self, p="win32"):
        """实现支持edge下载"""
        x_ = self._get_edge_current_version()
        dr = self.get_edge_current_driver_version()
        if dr != 0:
            log_v2.warning("已存在 MicrosoftEdge 驱动，将进行查找最新浏览器驱动...")

            if x_ == dr:
                log_v2.info("当前MicrosoftEdge 浏览器版本为" + x_ + " msedgedriver驱动程序版本为：" + dr)
                log_v2.info("当前浏览器驱动版本与浏览器一致无需更新下载...")
            else:
                log_v2.info("当前MicrosoftEdge 浏览器版本为" + x_ + " msedgedriver驱动程序版本为：" + dr)
                log_v2.info("驱动程序与浏览器版本不匹配，进行下载与其相对应的浏览器驱动版本...")
                url = self.edge_platform(p=p, v=x_)
                self._unzip_driver(zip_path=self.download_driver(path_url=url, filename=str(url).split("/")[-1]))

        else:
            log_v2.warning("系统不存在 MicrosoftEdge 驱动，将进行下载最新浏览器驱动...")
            log_v2.info("当前MicrosoftEdge 浏览器版本为" + x_)
            log_v2.info("正在下载与浏览器版本匹配的驱动程序...")
            url = self.edge_platform(p=p, v=x_)
            self._unzip_driver(zip_path=self.download_driver(path_url=url, filename=str(url).split("/")[-1]))

    def open_firefox(self, p="win32"):
        """实现支持firefox下载"""
        # x_ = self._get_edge_current_version()
        dr = self.get_firefox_current_driver_version()
        vr = [x for x in self.get_firefox_latest()]
        if dr:
            if vr[0]["version"].lstrip("v") == dr[-1]:
                log_v2.warning("当前 geckodriver 驱动，已是最新版本。")
            else:
                log_v2.warning("当前 geckodriver 驱动，不是最新版本，正在为你查找最新版本驱动")
                log_v2.info("目前最新 geckodriver 版本为" + vr[0]["version"])
                log_v2.info("正在下载匹配的驱动程序...")
                url = self.firefox_platform(p=p)
                self._unzip_driver(zip_path=self.download_driver(path_url=url, filename=str(url).split("/")[-1]))

        else:
            log_v2.warning("系统不存在 geckodriver 驱动，将进行查找最新浏览器驱动...")
            log_v2.info("目前最新 geckodriver 版本为" + vr[0]["version"])
            log_v2.info("正在下载匹配的驱动程序...")
            url = self.firefox_platform(p=p)
            self._unzip_driver(zip_path=self.download_driver(path_url=url,filename=str(url).split("/")[-1]))



if __name__ == '__main__':
    JsonDownloadDriver().open_chrome()
