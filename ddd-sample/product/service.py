# coding: utf-8
from typing import Protocol, List, Optional

from .schema import ProductInfo
from .product import Product
from .repository import ProductRepository, create_product_repository

class ProductService(Protocol):

    def create(self, pid: str, name: str, dsc:str):...
    def rename(self, pid: str, new_name:str):...
    def query(self, pid: str) -> Optional[ProductInfo]:...
    def query_all(self) -> List[ProductInfo]:...


class LocalProductService(ProductService):
    def __init__(self, respository: ProductRepository):
        self.respository = respository

    def create(self, pid: str, name: str, dsc:str):
        p = self.respository.query(pid)
        if p:
            raise ValueError(f"product {pid} has existed!")
        p = Product(pid, name, dsc)
        self.respository.save(p)
        
    def rename(self, pid: str, new_name:str):
        p = self.respository.query(pid)
        if not p:
            raise ValueError(f"product {pid} not existed!")
        p.rename(new_name)
        self.respository.save(p)

    def query(self, pid: str) -> Optional[ProductInfo]:
        p = self.respository.query(pid)
        if not p:
            return None
        return p.to_info()
        
    def query_all(self) -> List[ProductInfo]:
        return [p.to_info for p in self.respository.query_all()]
        

def create_product_service()->ProductService:
    return LocalProductService(create_product_repository())
