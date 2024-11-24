from enum import Enum
from typing import Union
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

# 正常トークン
correct_token = "correct_token"

# 模擬ユーザーデータ
dummy_user_db = {
    "abcde12345": {"id": "abcde12345", "name": "Yamada", "email_address": "yamada@example.com"},
    "fghij67890": {"id": "fghij67890", "name": "Tanaka", "email_address": "tanaka@example.com"},
}

# クラスサンプル
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    
# ユーザ
class User(BaseModel):
    id: str
    name: str
    email_address: str

# 列挙サンプル
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# FastAPIインスタンス生成
app = FastAPI()

# 基本
@app.get("/")
async def root():
    return {"message": "Hello World"}

# パスパラメーター1（数値）
# http://127.0.0.1:8000/items/3
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# パスパラメーター2（列挙型）
# http://127.0.0.1:8000/models/alexnet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# パスパラメーター3（ファイルパス）
# http://127.0.0.1:8000/files/home/johndoe/myfile.txt
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# クエリパラメーター（スキップ＋上限 デフォルト値あり）
# http://127.0.0.1:8000/querys/?skip=0&limit=10
@app.get("/querys/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# パスパラメーターとクエリパラメーター（オプショナルあり デフォルトあり）
# http://127.0.0.1:8000/users/taro/items/1001?q=hoge&short=true
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# リクエストボディ（内容解析含む）
@app.post("/sample_items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# パスパラメーターとリクエストボディとクエリパラメーター（内容解析含む）
@app.put("/dummy_items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

# ユーザー情報取得API
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, token: str = Header(...)):
    # トークン不正時
    if token != correct_token:
        raise HTTPException(
            status_code=400, detail="token_verification_failed")
    # ユーザー非存在時
    if user_id not in dummy_user_db:
        raise HTTPException(status_code=404, detail="user_not_found")
    return dummy_user_db[user_id]


# ユーザー情報登録API
@app.post("/users/", response_model=User)
async def create_user(user: User, token: str = Header(...)):
    # トークン不正時
    if token != correct_token:
        raise HTTPException(
            status_code=400, detail="token_verification_failed")
    # ユーザーID重複時
    if user.id in dummy_user_db:
        raise HTTPException(status_code=400, detail="user_id_duplicated")
    dummy_user_db[user.id] = user
    return user