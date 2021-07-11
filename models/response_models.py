from typing import List
from pydantic import BaseModel

from models.job import JobListModel


class ResponseBase(BaseModel):
    code: int
    message: str

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ResponseList(ResponseBase):
    jobs: list[JobListModel]
    def __init__(self, res: list):
        self.jobs = res
        super().__init__(200, '%s records found.' % len(res))
