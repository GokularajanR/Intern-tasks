from fastapi import APIRouter
from models.stock_models import create_stock, read_all_stocks, buy_stock, sell_stock, Stock

router = APIRouter()
@router.post("/stocks/")
def create_stock_endpoint(stock: Stock):
    return create_stock(stock)

@router.get("/stocks/")
def read_all_stocks_endpoint():
    return read_all_stocks()

@router.post("/stocks/{stock_id}/buy/")
def buy_stock_endpoint(stock_id: str, quantity: int):
    return buy_stock(stock_id, quantity)

@router.post("/stocks/{stock_id}/sell/")
def sell_stock_endpoint(stock_id: str, quantity: int):
    return sell_stock(stock_id, quantity)