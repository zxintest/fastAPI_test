from fastapi import FastAPI
from enum import Enum
from typing import Union

class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

"""
===============================路径参数==================================================
"""
@app.get('/')
async def root():
    return {'message':"hello world"}

# @app.get('/items/{item_id}')
# async def read_item(item_id:int):       # 定义参数类型：int、str、float、bool
#     return {'item_id':item_id}

# 由于路径操作是按顺序依次运行的，你需要确保路径 /users/me 声明在路径 /users/{user_id}
@app.get('/user/me')
async  def read_user_me():
    return {"username":"me"}

@app.get('/user/{user_id}')
async  def read_user(user_id:int):
    return {"username":user_id}

# 从定义的枚举中取值
@app.get('/models/{model_name}')
async def get_model(model_name:ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name":model_name,"message":"欢迎{alexnet}"}
    if model_name.value == "lenet":
        return {"model_name":model_name,"message":"果然是你lenet"}
    else:
        return {"model_name":model_name,"message":f"不认识你{model_name}"}

@app.get("/files/{file_path:path}")
async def read_file(file_path:str):
    return {"file_path":file_path}

"""
=======================查询参数===============================
"""

fake_items_db = [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}] #定义伪数据库

# @app.get("/items/")
# async def read_item(skip:int=0,limit:int = 10):
#     return fake_items_db[skip:skip+limit]

# @app.get("/items/{item_id}")
# async def read_item1(item_id:str,q:Union[str,None] = None,short : bool = False): # 定义了q参数，可以有两种类型str和None，默认不传取None
#     item = {"item_id":item_id}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update({"结论":"是False则返回这个"})
#     return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id:int,item_id:str,q:Union[str,None] = None,short:bool = False): # 无需声明顺序，会按照名称检索
    item = {"item_id":item_id,"user_id":user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({"short":short})
    return item

@app.get("/items/{item_id}")
async def read_user_item1(item_id:str,needy:str): # 这两参数为必填
    item = {"item_id":item_id,"needy":needy}
    return item

"""
===============================请求体==================================
"""
from pydantic import BaseModel

class Item(BaseModel):
    name:str
    description:Union[str,None] = None
    price:float
    tax:Union[float,None] = None

@app.post('/items/')
async def create_item(item:Item):
    item_dict = item.dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"实付价":price_with_tax})
    return item_dict

@app.put("/items/{item_id}/")
async def put_item(item_id:int,item:Item()):
    return {"item_id":item_id,**item.dict()}
# """通过使用  **  语法，将这些键值对作为关键字参数传递给  return  语句，以便将它们作为函数返回的字典的一部分。
# 这样做的效果是，将  item_id  和  Item  对象的属性值合并到一个字典中，并作为函数的返回结果
# """

"""
查询参数和字符串校验
"""