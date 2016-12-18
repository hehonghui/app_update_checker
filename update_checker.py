# -*- coding: utf-8 -*-
# base on python 2.7

import os
import sys
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

from com.android.monkeyrunner import MonkeyImage
from com.android.monkeyrunner.easy import EasyMonkeyDevice
from com.android.monkeyrunner.easy import By
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
lastest_apk = apk_list.pop()
print "最新版的apk ==> "+ lastest_apk

device = MonkeyRunner.waitForConnection()
easy_device = EasyMonkeyDevice(device)

package_name = "com.newsdog"

os.system("rm -rf apk_screenshots")
os.system("mkdir apk_screenshots")
screenshot_dir = "apk_screenshots"


# 开始自动升级检测
def start_update_test():
    for apk in apk_list:
        if apk.endswith(".apk"):
            # 截图的子目录名
            scr_dir = get_apk_name(apk) + "-" + get_apk_name(lastest_apk)
            # 创建截屏目录
            os.mkdir(screenshot_dir + seprator + scr_dir)
            print "安装 ==> " + apk
            # 清除最新版apk
            os.system("adb uninstall com.newsdog")

            # ===> 安装旧版的apk
            device.installPackage(apk)
            # 执行测试
            test_latest_apk(scr_dir, apk)

            # ===> 安装最新版
            print "安装最新版的apk ==> " + lastest_apk
            device.installPackage(lastest_apk)
            # 启动应用
            device.startActivity('com.newsdog/.mvp.ui.splash.SplashActivity')
            # 执行测试
            MonkeyRunner.sleep(10)
            # 随机点击一下
            click(600, 1080)
            # 截图
            take_screen_shot(scr_dir, '6_latest-main.png')


# 获取apk名字
def get_apk_name(full_name):
    session = full_name.split(seprator)
    apk_name = session[len(session) - 1]
    return apk_name.replace("NewsDog_", "").replace(".apk", "")


# 分版本点击不同的区域即可
def test_latest_apk(scr_dir, apk_file):

    print "version ==> " + get_apk_name(apk_file)

    device.startActivity('com.newsdog/.mvp.ui.splash.SplashActivity')
    MonkeyRunner.sleep(2)
    print "等待选择语言"
    take_screen_shot(scr_dir, '1_lan_choose.png')
    # 点击english按钮
    click(600, 900)
    MonkeyRunner.sleep(8)

    # 感兴趣页面
    take_screen_shot(scr_dir, '2_interest_choose.png')
    click(950, 100)
    print "跳过兴趣选择"
    MonkeyRunner.sleep(2)

    # 在主页
    take_screen_shot(scr_dir, '3_in_main.png')
    # 弹出兴趣选择
    MonkeyRunner.sleep(10)

    # 弹出quick 选择框
    take_screen_shot(scr_dir, '4_quick_view_dialog.png')
    # 选择开启quick view
    click(600, 1080)

    MonkeyRunner.sleep(8)
    take_screen_shot(scr_dir, '5_main.png')


def take_screen_shot(scr_dir, name):
    # 截取屏幕截图
    result = device.takeSnapshot()
    # 将截图保存至文件
    result.writeToFile(screenshot_dir + seprator + scr_dir + seprator + name, 'png')


def click(x, y):
    device.touch(x, y, MonkeyDevice.DOWN_AND_UP)


# 开始测试
start_update_test()



