# coding: utf-8

from .schema import ProductInfo

class Product(object):
    def __init__(self, pid: str, name: str, dsc:str):
        self.pid = pid
        self.name = name
        self.dsc = dsc

    def rename(self, new_name:str):
        self.name = new_name

    def to_info(self) -> ProductInfo:
        return {
            'pid': self.pid,
            'name': self.name,
            'dsc': self.dsc
        }
    