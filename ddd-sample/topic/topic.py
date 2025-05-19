# coding: utf-8

from .value_object import TopicContent

class Topic(object):
    def __init__(self, pid: str, tid: str, content: TopicContent):
        self.pid = pid
        self.tid = tid
        self.content = content

    def update_x(self, x: str):
        self.content = self.content.update_x(x)
