# coding: utf-8

from typing import Self
from pydantic import BaseModel

class TopicContent(BaseModel):
    x: str
    y: str

    def update_x(self, x: str) -> Self:
        return {
            'x': x,
            'y': self.y
        }
