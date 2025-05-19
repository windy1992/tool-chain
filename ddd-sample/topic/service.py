# coding: utf-8
from typing import Protocol, Optional

from ..product.service import create_product_service, ProductService
from .topic import Topic
from .value_object import TopicContent
from .repository import TopicRepository, create_topic_repository


class TopicService(Protocol):

    def create(self, pid: str, tid: str, content:TopicContent):...
    def query(self, tid: str) -> Optional[TopicContent]:...


class LocalTopicService(TopicService):
    def __init__(self, respository: TopicRepository, product_srv: ProductService):
        self.respository = respository
        self.product_srv = product_srv

    def create(self, pid: str, tid: str, content:TopicContent):
        p = self.product_srv.query(pid)
        if not p:
            raise ValueError(f"product {pid} not existed!")
        t = Topic(pid, tid, content)
        self.respository.save(t)
        
    def query(self, tid: str) -> Optional[TopicContent]:
        t = self.respository.query(tid)
        if not t:
            return None
        return t.content
        

def create_topic_service()->TopicService:
    return LocalTopicService(create_topic_repository(), create_product_service())
