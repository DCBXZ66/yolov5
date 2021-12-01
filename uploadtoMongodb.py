import base64
import pymongo
import os

myclient = pymongo.MongoClient("mongodb://192.168.166.181:27017")  # Host以及port

db = myclient["myDatabase"]
coll = db["kongmanzai"]


def save_to_mongo():
    dirs = 'e:/output'
    files = os.listdir(dirs)  # 列出文件夹下所有的目录与文件
    files.sort(key=lambda x: int(x.split('.')[0]))  # 给文件排序
    for file in files:
        # 图片的全路径
        filefullname = dirs + '/' + file
        # 分割图片文件的格式和名称
        f = file.split('.')
        # 文件名
        fname = f[0]
        try:
            with open(filefullname, 'rb') as f:
                base64_data = base64.b64encode(f.read())
                s = base64_data.decode()
        except IOError:
            print('读取失败')
        dict = {"name": fname, "tu": s}
        coll.insert_one(dict)
        print("成功写入"+fname)


if __name__ == '__main__':
    save_to_mongo()
