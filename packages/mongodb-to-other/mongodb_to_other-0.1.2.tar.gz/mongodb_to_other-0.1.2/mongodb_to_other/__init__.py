import pymongo
import xlwt
import json

def mongodb_to_xls(db_name,set_name,xls_path,port=27017,ip="127.0.0.1",name=None,password=None):
    #初始化变量
    key_list=[]
    l,i=-1,0
    #初始化输入参数
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('json',cell_overwrite_ok=True)
    #初始化数据库
    #myclient = pymongo.MongoClient(f'mongodb://{ip}:{port}/')
    if name==None and password==None:
        myclient = pymongo.MongoClient(host= ip, port=port)
    else:
        myclient==pymongo.MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = myclient[db_name] #testdb可按需求改动
    coll = db.get_collection(set_name)
    #开始写入
    for i in coll.find():
        for x in i.items(): 
            db_item={x[0]:x[1]}
            #的出一个数据库项
            for key,value in db_item.items():
                key_list.clear()
                key_list.extend((key, value))
                #位置设置
                i,l=1,l+1
                #写入
                #i 列，l 行
                for y in range(len(key_list)):
                    if isinstance(key_list[y],list):
                        z=y
                        for u in key_list[y]:
                            sheet.write(l,z,str(u))
                            z+=1
                    else:
                        sheet.write(l,y,str(key_list[y]))
    book.save(xls_path)

#示例
#mongodb_to_xls("testdb","userdb","D:\\test12345678.xls")
def mongodb_to_json(db_name,set_name,json_path,port=27017,ip="127.0.0.1",name=None,password=None):
    if name==None and password==None:
        client = pymongo.MongoClient(host= ip, port=port)
    else:
        client==pymongo.MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = client[db_name]
    coll = db.get_collection(set_name)
    coll=list(coll.find())
    l=len(coll)
    with open(json_path,"w+",encoding="utf-8") as f:
        f.write("[")
    n=0
    for i in coll:
        n+=1   
        with open(json_path,"a+",encoding="utf-8") as f:
            del i["_id"]
            f.write("   ")
            if coll.index(i)==l-1:
                json.dump(i, f,ensure_ascii=False)
            else:
                json.dump(i, f,ensure_ascii=False)
                f.write(",")
            f.write("\n")
            f.close
    with open(json_path,"a+",encoding="utf-8") as f:
        f.write("]")