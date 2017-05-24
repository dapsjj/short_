# -*- coding: UTF-8 -*-
import tkFileDialog
import cv2
from Tkinter import *
import os
import time
import tkMessageBox
import re
import sys
#上传一个超市货架视频文件，检测是否有空的货架
reload(sys)
sys.setdefaultencoding('utf-8')
#分类存放图片，缺货的货架图片放在short_supply_pictures文件夹，不缺货图片放在normal_supply_pictures文件夹

def get_file():
    today_path = time.strftime('%Y-%m-%d')
    filename = tkFileDialog.askopenfilename(title="选择视频",filetypes = [('视频', 'MPEG'),('视频', 'AVI'),('视频', 'FLV'),('视频', 'RMVB'),('视频', 'MP4')])
    right_count = 0
    wrong_cont = 0
    CN_Pattern = re.compile(u'[\u4E00-\u9FBF]+')
    JP_Pattern = re.compile(u'[\u3040-\u31fe]+')
    if filename:
        newFile = filename.split('/')[-1].split('.')[0]
        if not os.path.exists('D:\\short_supply_pictures\\' + today_path+'\\'+ newFile):
            os.makedirs('D:\\short_supply_pictures\\' + today_path+'\\'+ newFile)
        if not os.path.exists('D:\\normal_supply_pictures\\' + today_path+'\\'+ newFile):
            os.makedirs('D:\\normal_supply_pictures\\' + today_path+'\\'+ newFile)
        CN_Match = CN_Pattern.search(filename)
        JP_Match = JP_Pattern.search(filename)
        if CN_Match:
            # print u'有中文：%s' % (CN_Match.group(0),)
            tkMessageBox.showinfo("提示", "文件路径或文件名不能含有中文,请修改!")
            return
        elif JP_Match:
            # print u'有日文：%s' % (JP_Match.group(0),)
            tkMessageBox.showinfo("提示", "文件路径或文件名不能含有日文,请修改!")
            return

        vc = cv2.VideoCapture(filename)  # 读入视频文件
        pic = 1
        c = 1
        if vc.isOpened():  # 判断是否正常打开
            rval, frame = vc.read()
        else:
            rval = False
        timeF = 10  # 视频帧计数间隔频率
        while rval:  # 循环读取视频帧
            rval, frame = vc.read()
            if (pic % timeF == 5):
                body_cascade = cv2.CascadeClassifier('D:\\OpenCV2.4.9\\opencv\\sources\\data\\haarcascades\\test_short_supply.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bodys = body_cascade.detectMultiScale(gray,1.1,20,cv2.CASCADE_SCALE_IMAGE, (55, 55))
                flag = False
                for (x, y, w, h) in bodys:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    flag = True
                if flag == True:
                    cv2.imwrite('D:\\short_supply_pictures\\' + today_path+'\\'+ newFile+'\\' + str(c) + '.jpg', frame)  # 保存
                    right_count += 1
                else:
                    cv2.imwrite('D:\\normal_supply_pictures\\' + today_path + '\\'+ newFile + '\\' + str(c) + '.jpg',frame)  # 保存
                    wrong_cont += 1
                c += 1
            pic = pic + 1
            cv2.waitKey(1)
        vc.release()
    else:
        return

    if right_count>0:
        tkMessageBox.showinfo("提示","视频"+str(filename)+"中存在缺货的货架!\r\n"
                              +"截图所在路径D:\\short_supply_pictures\\"+ today_path+"\\"+newFile+"\r\n")
    else:
        tkMessageBox.showinfo("提示", "视频"+str(filename) + "中未发现缺货的货架!\r\n"
                              +"截图所在路径D:\\normal_supply_pictures\\" + today_path+"\\"+newFile+"\r\n")
root = Tk()
root.title('缺货监测')
button2 = Button(root, text="点此上传视频", command=get_file,width=20,height=10)
button2.pack()
root.geometry('300x200+500+300')
root.mainloop()
