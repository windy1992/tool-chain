# coding: utf-8
from typing import Protocol, Optional, List
from .product import Product

db = {
    '1': {
        'pid': '1',
        'name': 'douyin',
        'dsc': 'wuhoo'
    },
        '2': {
        'pid': '2',
        'name': 'kuaishou',
        'dsc': 'hahah'
    },
}

class ProductRepository(Protocol):
    def query(self, pid:str) -> Optional[Product]:...
    def query_all(self) -> List[Product]:...
    def save(self, p: Product):...
    def remove(self, p:Product):...


class LocalProductRepository(ProductRepository):
    def query(self, pid: str)->Optional[Product]:
        info = db.get(pid, None)
        if info is None:
            return None
        return Product(info['pid'], info['name'], info['dsc'])
    
    def query_all(self)->List[Product]:
        return [Product(info['pid'], info['name'], info['dsc']) for info in db.values()]

    def save(self, p: Product):
        db[p.pid] = {
            'pid': p.pid,
            'name': p.name,
            'dsc': p.dsc
        }

    def remove(self, p: Product):
        db.pop(p.pid, None)

def create_product_repository()-> ProductRepository:
    return LocalProductRepository()
