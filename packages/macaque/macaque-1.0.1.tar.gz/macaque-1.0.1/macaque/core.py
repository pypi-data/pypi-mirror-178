#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2022/11/26 4:15 下午
@Desc    :  core line.
"""
import os

from airtest.core.android.adb import ADB
from airtest.core.api import device, connect_device, stop_app, install
from airtest.core.helper import log

STATIC_PATH = os.path.dirname(os.path.realpath(__file__))
jar = os.path.join(STATIC_PATH, 'jar')
libs = os.path.join(STATIC_PATH, 'libs')


def prepare(udid, duration, package, whitelist=None):
    """

    :param whitelist:
    :param udid:
    :param duration:
    :param package:
    :return:
    """
    connect_device(f'Android:///{udid}?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MAXTOUCH')

    install(filepath='./ADBKeyBoard.apk', install_options='-g')

    serialno = device().serialno
    adb = ADB(serialno=serialno)
    # 静音
    adb.shell('media volume --set 0')
    # 推送 macaque 文件
    for j in os.listdir(jar):
        adb.push(os.path.join(jar, j), '/sdcard')

    # 推送 libs 文件
    for lib in os.listdir(libs):
        adb.push(os.path.join(libs, lib), '/data/local/tmp/')

    # 运行 duration
    # --act-whitelist-file /sdcard/awl.strings
    if whitelist and not '':
        with open(file='./awl.strings', mode='w', encoding='utf-8') as f:
            f.write(whitelist)
        # 推送 whitelist 到设备上
        adb.push(os.path.join(STATIC_PATH, 'awl.strings'), '/sdcard/awl.strings')
        cmd = f'CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/macaque-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p {package} --agent reuseq --running-minutes {duration} --throttle 800 -v -v --act-whitelist-file /sdcard/awl.strings --bugreport'
    else:
        cmd = f'CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/macaque-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p {package} --agent reuseq --running-minutes {duration} --throttle 800 -v -v --bugreport'

    os.system(f'{ADB.builtin_adb_path()} -s {udid} shell {cmd}')

    oom = '/sdcard/oom-traces.log'
    crash = '/sdcard/crash-dump.log'
    for files in [oom, crash]:
        if adb.exists_file(files):
            adb.pull(files, STATIC_PATH)
            adb.shell(f'rm {files}')
        else:
            log(f"不存在异常：{files}")

    # teardown
    if whitelist and not '':
        adb.shell(f'rm /sdcard/awl.strings')
    stop_app(package)
