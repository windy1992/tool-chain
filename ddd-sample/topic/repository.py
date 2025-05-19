# coding: utf-8
from typing import Protocol, Optional
from .topic import Topic

db = {
    '1': {
        'pid': '1',
        'tid': '1',
        'content': {
            'x': 'x_1',
            'y': 'y_1'
        }

    },
    '2': {
        'pid': '1',
        'tid': '2',
        'content': {
            'x': 'x_2',
            'y': 'y_2'
        }

    },
}

class TopicRepository(Protocol):
    def query(self, tid:str) -> Optional[Topic]:...
    def save(self, t: Topic):...


class LocalTopicRepository(TopicRepository):
    def query(self, tid: str)->Optional[Topic]:
        info = db.get(tid, None)
        if info is None:
            return None
        return Topic(info['pid'], info['tid'], info['content'])

    def save(self, t: Topic):
        db[t.tid] = {
            'pid': t.pid,
            'tid': t.tid,
            'content': t.content
        }

def create_topic_repository()-> TopicRepository:
    return LocalTopicRepository()
