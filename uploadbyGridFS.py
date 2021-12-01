import gridfs
from pymongo import MongoClient
from gridfs import *
import os
from io import BytesIO
from pymongo import MongoClient
import os
import matplotlib.pyplot as plt
import matplotlib.image as iming
import bson.binary


def test1():
    # 链接mongodb
    client = MongoClient('192.168.166.181', 27017)
    # 取得对应的collection
    db = client.myDatabase
    # 本地硬盘上的图片目录
    dirs = 'e:/output'
    # 列出目录下的所有图片
    files = os.listdir(dirs)
    # 遍历图片目录集合
    for file in files:
        # 图片的全路径
        filesname = dirs + '/' + file
        # 分割，为了存储图片文件的格式和名称
        f = file.split('.')
        # 类似于创建文件
        datatmp = open(filesname, 'rb')
        # 创建写入流
        imgput = GridFS(db, collection="originDataAndResult")
        # 将数据写入，文件类型和名称通过前面的分割得到
        insertimg = imgput.put(datatmp, contentType=f[1], filename=f[0])
        datatmp.close()
    print("成功！！！！")


def test2():
    connect = MongoClient('192.168.166.181', 27017)  # 创建连接点
    db = connect.myDatabase
    print(db.collection_names())
    imgput = gridfs.GridFS(db)
    dirs = '/home/yf/PycharmProjects/yolov5/inference/output'
    files = os.listdir(dirs)
    for file in files:
        filesname = dirs + '/' + file
        print(filesname)
        imgfile = iming.imread(filesname)
        # iming.imsave('s.jpg',imgfile)
        # print type(imgfile),imgfile
        # imgfile.shape()
        plt.imshow(imgfile)
        plt.axis('off')
        plt.show()
        f = file.split('.')
        print(f)
        datatmp = open(filesname, 'rb')
        data = BytesIO(datatmp.read())
        content = bson.binary.Binary(data.getvalue())
        # print content
        # 创建写入流
        imgput = GridFS(db, collection="dyftest")
        insertimg = imgput.put(data, content_type=f[1], filename=f[0])


if __name__ == '__main__':
    test2()
