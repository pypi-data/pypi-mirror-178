from json import *
from pymongo import *


#导入不同项

def Import_different_items(db_name,set_name,json_path,port=27017,ip="127.0.0.1",name=None,password=None):
    #init
    #导入数据库
    if name==None and password==None:

        client = MongoClient(host= ip, port=port)
    else:
        #使用用户
        client==MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = client[db_name]
    coll = db.get_collection(set_name)

    #import 

    #标准json格式:
    # [
    # {"name":"142857","password":"142857"},
    # {"name":"123456","password":"123456"}
    # ]

    num=0

    items=[]

    for i in coll.find():
        del i["_id"]
        items.append(i)


    with open(json_path, 'r',encoding="utf-8") as f:
        #获取json
        data = list(load(f))

    for i in data:
        #判断相同
        if i in items:
            pass
            num+=1
        else:
            #导入不同
            coll.insert_one(i)




#只保留不同
def Import_retain_different_items(db_name,set_name,json_path,port=27017,ip="127.0.0.1",name=None,password=None):
    #init
    #导入数据库
    if name==None and password==None:

        client = MongoClient(host= ip, port=port)
    else:
        #使用用户
        client==MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = client[db_name]
    coll = db.get_collection(set_name)

    #import 

    #标准json格式:
    # [
    # {"name":"142857","password":"142857"},
    # {"name":"123456","password":"123456"}
    # ]

    items=[]

    for i in coll.find():
        del i["_id"]
        items.append(i)

    num=0
    different=[]
    with open(json_path, 'r',encoding="utf-8") as f:
        #获取json
        data = list(load(f))

    for i in data:
        #判断相同
        if i in items:
            pass
            num+=1
        else:
            #添加不同
            # coll.insert_one(i)
            different.append(i)

    for i in coll.find():
        #删除所有
        coll.delete_one(i)

    for i in different:
        #添加不同
        coll.insert_one(i)



#覆盖且导入所有
def Import_cover_new_items(db_name,set_name,json_path,port=27017,ip="127.0.0.1",name=None,password=None):
    #init
    #导入数据库
    if name==None and password==None:

        client = MongoClient(host= ip, port=port)
    else:
        #使用用户
        client==MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = client[db_name]
    coll = db.get_collection(set_name)

    #import 

    #标准json格式:
    # [
    # {"name":"142857","password":"142857"},
    # {"name":"123456","password":"123456"}
    # ]


    items=[]

    for i in coll.find():
        del i["_id"]
        items.append(i)

    with open(json_path, 'r',encoding="utf-8") as f:
        #获取json
        data = list(load(f))

    for i in coll.find():
        #删除所有
        coll.delete_one(i)

    for i in data:
        #添加不同
        coll.insert_one(i)


#追加所有
def append_new_items(db_name,set_name,json_path,port=27017,ip="127.0.0.1",name=None,password=None):
    #init
    #导入数据库
    if name==None and password==None:

        client = MongoClient(host= ip, port=port)
    else:
        #使用用户
        client==MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = client[db_name]
    coll = db.get_collection(set_name)

    #import 

    #标准json格式:
    # [
    # {"name":"142857","password":"142857"},
    # {"name":"123456","password":"123456"}
    # ]
    with open(json_path, 'r',encoding="utf-8") as f:
        #获取json
        data = list(load(f))
        
    for i in data:
        #添加all
        coll.insert_one(i)
 



