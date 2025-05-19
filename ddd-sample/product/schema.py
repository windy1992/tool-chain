# coding: utf-8
from pydantic import BaseModel


class ProductInfo(BaseModel):
    pid: str
    name: str
    dsc: str
