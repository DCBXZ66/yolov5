import pymysql as mdb
import sys
import pymysql
import os
import traceback
import cv2
from PIL import Image
import numpy
import types
#from rec import img_to_rec
import types


# 存入指定图片到数据库
def write_mysql(path, config):
    """
    读取图片写入数据库
    :param path: 读取的图片的路径
    :param config: 数据库连接配置信息
    :return: None
    """
    filename = path.split('/')[-1]
    try:
        with open(path, 'rb') as f:
            img = f.read()
    except:
        print('读取失败')
        # sys.exit(1)
        return
    try:
        conn = pymysql.connect(host=config['host'],
                               port=config['port'],
                               user=config['user'],
                               passwd=config['password'],
                               db=config['db'],
                               charset='utf8',
                               use_unicode=True)
        cursor = conn.cursor()
        # sql = "INSERT INTO ocr (content, category) VALUES (%s, '{0}')".format(filename)
        sql = "INSERT INTO ocr (content) VALUES (%s)"
        cursor.execute(sql, img)
        conn.commit()
        cursor.close()
        conn.close()
        print('写入 {} 成功'.format(filename))

    except Exception as e:
        print(e)
        print('写入失败')


# 遍历文件夹所有图片，存入数据库
def write_mysql2(config):
    """
    读取图片写入数据库
    :param path: 读取的图片的路径
    :param config: 数据库连接配置信息
    :return: None
    """
    rootdir = 'e:/output'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            filename = path.split('/')[-1]
            try:
                with open(path, 'rb') as f:
                    img = f.read()
            except:
                print('读取失败')
                # sys.exit(1)
                return
            try:
                conn = pymysql.connect(host=config['host'],
                                       port=config['port'],
                                       user=config['user'],
                                       passwd=config['password'],
                                       db=config['db'],
                                       charset='utf8',
                                       use_unicode=True)
                cursor = conn.cursor()
                # 注意一下这里的 {0} 的引号，可以试一下去掉引号会提醒没有者找到该字段
                # sql = "INSERT INTO ocr (content, category) VALUES (%s, '{0}')".format(filename)
                sql = "INSERT INTO kongmanzai (tu,`type`) VALUES (%s, 'jpg')"
                cursor.execute(sql, img)
                conn.commit()
                cursor.close()
                conn.close()
                print('写入 {} 成功'.format(filename))

            except Exception as e:
                print(e)
                print('写入失败')


# 读取数据库文件
def read_mysql(path, filename, config):
    """
    从数据库中读取图片
    :param path: 你要保存的图片的路径
    :param filename:你要从数据库读取的名字，在本例子相当于数据库中的name字段
    :param config: 数据库连接配置信息
    :return: None
    """
    try:
        conn = pymysql.connect(host=config['host'],
                               port=config['port'],
                               user=config['user'],
                               passwd=config['password'],
                               db=config['db'],
                               charset='utf8',
                               use_unicode=True)
        cursor = conn.cursor()
        cursor.execute("select content from ocr where category = '{}'".format(filename))
        res = cursor.fetchone()[0]
        # PIL.Image转换成OpenCV格式
        # fout = open("convert/pic.jpg", 'wb')
        # fout.write(res)
        # fout.close()
        # image = Image.open("convert/pic.jpg")
        # image = Image.open(res)
        img = cv2.cvtColor(numpy.asarray(res), cv2.COLOR_RGB2BGR)
        cv2.imshow("OpenCV", img)
        cv2.waitKey()
        print('opencv格式转化成功')
        # 将获取图片存入文件夹
        with open(path, 'wb') as f:
            f.write(res)
        print('从数据库中读取 {} 成功'.format(filename))
    except Exception as e:
        print(e)
        print('读取数据库中的图片失败')

# 查询所有weight为null的数据，返回数据id
def select_null(config):
    conn = pymysql.connect(host=config['host'],
                           port=config['port'],
                           user=config['user'],
                           passwd=config['password'],
                           db=config['db'],
                           charset='utf8',
                           use_unicode=True)
    cursor = conn.cursor()
    cursor.execute("select id from ocr where weight is Null")
    res = cursor.fetchall()
    res_list = []
    for i in res:
        res_list.append(list(i))  # 将fetchall方法返回的元组转换为list类型。
    cursor.close()
    conn.close()
    # print('返回结果:', res_list)
    # print(len(res_list))
    return res_list


def test(config):
    conn = pymysql.connect(host=config['host'],
                           port=config['port'],
                           user=config['user'],
                           passwd=config['password'],
                           db=config['db'],
                           charset='utf8',
                           use_unicode=True)
    cursor = conn.cursor()
    i = 167
    cursor.execute("select content from ocr where id = {}".format(i))
    pic = cursor.fetchone()[0]
    # PIL.Image转换成OpenCV格式
    f = open("img_to_rec_loca/{}.jpg".format(i), 'wb')
    f.write(pic)
    f.close()
    cursor.execute("select `type` from ocr where id = {}".format(i))
    t = cursor.fetchone()
    type = t[0]
    # print(type)
    # image = Image.open("img_to_rec_loca/{}.jpg".format(i))
    image = cv2.imread("img_to_rec_loca/{}.jpg".format(i))
    # img = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
    # # cv2.imshow("OpenCV", img)
    # cv2.imshow("111", image)
    result = img_to_rec(image, type)
    # update_weight(config, result, i)


# 根据id查询content和type
def select_img(config, res_list):
    """
        :param config: 数据库连接配置信息
        :param res: 一个装有所有id的列表
    """
    for item in res_list:
        for i in item:
            conn = pymysql.connect(host=config['host'],
                                   port=config['port'],
                                   user=config['user'],
                                   passwd=config['password'],
                                   db=config['db'],
                                   charset='utf8',
                                   use_unicode=True)
            cursor = conn.cursor()
            cursor.execute("select content from ocr where id = {}".format(i))
            content = cursor.fetchone()[0]
            # PIL.Image转换成OpenCV格式
            f = open("img_to_rec_loca/{}.jpg".format(i), 'wb')
            f.write(content)
            f.close()
            image = Image.open("img_to_rec_loca/{}.jpg".format(i))
            img = cv2.cvtColor(numpy.asarray(content), cv2.COLOR_RGB2BGR)
            cv2.imshow("OpenCV", img)
            cursor.execute("select `type` from ocr where id = {}".format(i))
            t = cursor.fetchone()
            type = t[0]


# 根据识别结果更新数据库中的weight
def update_weight(config, weight, id):
    conn = pymysql.connect(host=config['host'],
                           port=config['port'],
                           user=config['user'],
                           passwd=config['password'],
                           db=config['db'],
                           charset='utf8',
                           use_unicode=True)
    cursor = conn.cursor()
    cursor.execute("UPDATE ocr SET weight = {}  where id = {}".format(weight, id))
    conn.commit()
    print("id{}数据更新成功".format(id))
    conn.close()
    cursor.close()


# 删除数据库数据
def delete_weight(config):
    conn = pymysql.connect(host=config['host'],
                           port=config['port'],
                           user=config['user'],
                           passwd=config['password'],
                           db=config['db'],
                           charset='utf8',
                           use_unicode=True)
    cursor = conn.cursor()
    for i in range(98, 198):
        temp = ''
        cursor.execute("UPDATE ocr SET weight = %s where id = {}".format(i), temp)
        print("id{}数据删除成功".format(i))
        conn.commit()
    conn.close()
    cursor.close()

if __name__ == '__main__':
    my_config = {'host': '222.74.94.190', 'port': 3310, 'user': 'root',
                 'password': '996007', 'db': 'gps_web'}
    # select_null(my_config)
    # write_mysql('files/jindna_model.jpg', my_config)
    write_mysql2(my_config)
    # print(' 写入成功 '.center(50, '*'))
    # print(' 写入后再读取 '.center(50, '*'))
    # read_mysql('files_result/result_pic.jpg', 'jindna_model.jpg', my_config)
    # test(my_config)
    # delete_weight(my_config)
    # update_weight(my_config, 42, 98)