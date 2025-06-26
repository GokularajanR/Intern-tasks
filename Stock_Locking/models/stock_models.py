from bson import ObjectId
from pymongo import MongoClient
from pydantic import BaseModel
from lock import acquire_lock, release_lock

class Stock(BaseModel):
    name: str
    price: float
    quantity: int

URL = "mongodb+srv://gokul26092004:gulgul@gul.wmd0umx.mongodb.net/?retryWrites=true&w=majority&appName=gul"

client = MongoClient(URL)
db = client['Stock']
collection = db['stocks']

def create_stock(stock: Stock):
    try:
        res = collection.insert_one(stock.dict())
        return {"id": str(res.inserted_id)}
    except Exception as e:
        return {"error": str(e)}

def read_all_stocks():
    def transform_id(doc):
        doc["_id"] = str(doc["_id"])
        return doc
    return [transform_id(doc) for doc in collection.find()]

def buy_stock(stock_id: str, quantity: int):
    stock_lock = acquire_lock(stock_id)

    if not stock_lock:
        return {"error": "stock currently being updated. Please try again later."}
    
    try:
        stock = collection.find_one({"_id": ObjectId(stock_id)})
        if stock and stock['quantity'] >= quantity:
            new_quantity = stock['quantity'] - quantity
            collection.update_one( 
                {"_id": ObjectId(stock_id)},
                {"$set": {"quantity": new_quantity}}
            )
            return {"new quantity" : new_quantity}
        else:
            return {"error": "Insufficient stock quantity or stock not found."}
        
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        release_lock(stock_id, stock_lock)

    

def sell_stock(stock_id: str, quantity: int):
    try:
        stock = collection.find_one({"_id": ObjectId(stock_id)})
        if stock:
            new_quantity = stock['quantity'] + quantity
            collection.update_one(
                {"_id": ObjectId(stock_id)},
                {"$set": {"quantity": new_quantity}}
            )
            return {"new quantity": new_quantity}
        
        return {"error": "Stock not found."}
    
    except Exception as e:
        return {"error": str(e)}