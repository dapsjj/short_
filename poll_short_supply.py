# -*- coding: UTF-8 -*-
import os
import tkMessageBox
import datetime
import time
import shutil
import schedule
import mp3play

#每5秒调用一次函数check_null_dir,发现指定文件夹有图片则播放提示音
#轮询检测缺货的货架

# today_path = datetime.datetime.now().strftime('%Y-%m-%d')
today_path =time.strftime('%Y-%m-%d')
disk_short_supply_path = 'C:\\short_supply_pictures'
disk_normal_supply_path = 'C:\\normal_supply_pictures'
work_path = 'C:\\short_supply_pictures\\' + today_path
def check_null_dir(dirr):
    if not os.path.exists(work_path):
        # print '今天还没有可用的目录!',time.strftime('%Y-%m-%d %H:%M:%S')
        pass
    else:
        if os.path.isdir(dirr):
            for p in os.listdir(dirr):
                d  = os.path.join(dirr,p)
                if (os.path.isdir(d) == True):
                    check_null_dir(d)
        if  os.listdir(dirr):
            if dirr.count('\\')!=2:
                # print '非空目录:', dirr + '缺货', time.strftime('%Y-%m-%d %H:%M:%S')
                filename = 'C:\\message.mp3'
                mp3 = mp3play.load(filename)
                mp3.play()
                len = mp3.seconds()
                time.sleep(len)
                mp3.stop()
                tkMessageBox.showwarning("提示", "路径"+dirr+"货架缺货,请及时确认!")


#功能：删除指定目录dir中当前日期前3天的所有文件夹
def remove_threedaysago_files():
    today = datetime.date.today()
    threedaysago = today - datetime.timedelta(days=3)
    for file in os.listdir(disk_short_supply_path):
        if os.path.isdir(os.path.join(disk_short_supply_path,file)):
            if file <= str(threedaysago):
                shutil.rmtree(os.path.join(disk_short_supply_path,file))
    for file in os.listdir(disk_normal_supply_path):
        if os.path.isdir(os.path.join(disk_normal_supply_path,file)):
            if file <= str(threedaysago):
                shutil.rmtree(os.path.join(disk_normal_supply_path,file))

schedule.every().day.at("12:00").do(remove_threedaysago_files)

while True:
    check_null_dir(work_path)
    schedule.run_pending()
    time.sleep(2)
