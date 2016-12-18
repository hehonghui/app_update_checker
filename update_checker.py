# -*- coding: utf-8 -*-
# base on python 2.7

import os
import sys
print sys.path
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import platform

# windows的风格
seprator = "\\"

print "系统环境变量为: " + str(os.environ)

env_path = os.environ['PATH']
# 通过PATH环境变量的格式来判断是什么操作系统, windows的环境变量是通过;来分割, 而mac是通过:.
if str(env_path).find(";") == -1 or str(platform.platform()).lower().__contains__("mac"):
    seprator = "/"
    print "Max OS X or Linux"

apks_dir = "apks_dir"
if len(sys.argv) == 2:
    apks_dir = sys.argv[1]

print "apk目录为 ==> " + apks_dir

# 判断目录是否存在
if not os.path.exists(apks_dir):
    print "apks_dir no exsit."
    exit()

# 获取apk列表
apk_list = []
for file in os.listdir(apks_dir):
    apk_path = os.path.abspath(file)
    # 构造完整的路径
    apk_path = apk_path.replace(file, apks_dir + seprator + file)
    # 这里被替换为jhthon的路径
    print "apk file name : " + apk_path
    apk_list.append(apk_path)


apk_list.sort()
print apk_list


index = len(apk_list) - 1
# 最新版的apk
lastest_apk = apk_list.pop( )
print "最新版的apk ==> "+ lastest_apk

device = MonkeyRunner.waitForConnection()


# 开始自动升级检测
def start_update_test(apks_list,lastest):
    for apk in apk_list:
        if apk.endswith(".apk"):
            print "安装 ==> " + apk
            # 清除最新版apk
            os.system("adb uninstall com.newsdog")
            # 执行操作
    print "安装最新版的apk ==> " + lastest
    device.installPackage(lastest)


start_update_test(apk_list, lastest_apk)



