# coding: utf-8
from fastapi import FastAPI
from pydantic import BaseModel
from product.service import create_product_service
app = FastAPI()



class ProductCreateRq(BaseModel):
    pid: str
    name: str
    dsc: str

@app.post("/product/create")
def create_product(rq: ProductCreateRq):
    create_product_service().create(rq.pid, rq.name, rq.dsc)
    return {}


class ProductQueryRq(BaseModel):
    pid: str

@app.post("/product/query")
def query_product(rq: ProductQueryRq):
    return create_product_service().query(rq.pid)


    