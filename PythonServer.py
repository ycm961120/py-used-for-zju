# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:43:01 2020

@author: Chenming Yao

这是一个python服务器，
可以封装基于python的算法
并用于给java提供调用

与java的连接部分已经完成，你要做的只是将你想要通过python实现的算法，
重写62行的run方法即可。
"""

import socket
import sys
import threading
import arcpy
import os


def main():
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 获取本地主机名称
    host = socket.gethostname()
    # 设置一个端口
    port = 10005
    # 将套接字与本地主机和端口绑定
    serversocket.bind((host,port))
    # 设置监听最大连接数
    serversocket.listen(5)
    # 获取本地服务器的连接信息
    myaddr = serversocket.getsockname()
    print("服务器地址:%s"%str(myaddr))
    # 循环等待接受客户端信息
    while True:
        # 获取一个客户端连接
        clientsocket,addr = serversocket.accept()
        print("连接地址:%s" % str(addr))
        try:
            t = ServerThreading(clientsocket)#为每一个请求开启一个处理线程
            t.start()
            pass
        except Exception as identifier:
            print(identifier)
            pass
        pass
    serversocket.close()
    pass



class ServerThreading(threading.Thread):
    def __init__(self,clientsocket,recvsize=1024*1024,encoding="GBK"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def run(self):
        print("开启线程.....")
        try:
            #接受数据
            msg = ''
            while True:
                # 读取recvsize个字节
                rec = self._socket.recv(self._recvsize)
                # 解码
                msg += rec.decode(self._encoding)
                # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕，
                # 所以需要自定义协议标志数据接受完毕
                if msg.strip().endswith('over'):
                    msg=msg[:-4]
                    break
            way = msg.split(",")
            dataWay = way[1]
            saveWay = way[2] + "/trash"
            #os.mkdir(saveWay)

            #将dataWay下的栅格图像裁剪成5*10块，保存到saveWay下的trash文件夹中,顺便统计下有几个变量
            count = 0;
            for file in os.listdir(dataWay):
                count += 1
                way1 = dataWay+"/"+file

                #arcpy.arcpy.SplitRaster_management(way1,saveWay,\
                #                        file.split(".")[0], "NUMBER_OF_TILES", "TIFF", "NEAREST",\
                #                        "5 10", "#", "4", "PIXELS", "#", "#")

            for i in range(50):
                data = ""
                for file in os.listdir(saveWay):
                    if file.endswith(str(i) + ".TIF"):
                        if i < 10 and not ("0"<=file[-len(str(i))-5]<="9"):
                            data += saveWay+"/"+file+","
                        if i >=10:
                            data += saveWay + "/" + file + ","
                data = data[:-1]
                if len(data.split(",")) == count:
                    print(data)
                    self._socket.send(data.encode(self._encoding))
                    self._socket.send(";".encode(self._encoding))



            pass
        
        except Exception as identifier:
            self._socket.send("500".encode(self._encoding))
            print(identifier)
            pass
        
        finally:
            self._socket.close() 
        print("任务结束.....")
        
        pass

    def __del__(self):
        pass

if __name__ == "__main__":
    main()
