import base64
from datetime import datetime
from typing import Optional

from database.database_access import Database
from pydantic import BaseModel, PrivateAttr
from fastapi import Body


db_obj = Database()

class JobListModel(BaseModel):
    id: int
    title: str
    description: str
    created_by: str
    updated_by: str
    created_date: datetime
    updated_date: datetime

class JobInsertModel(BaseModel):
    title: str = Body(..., title="Title of Job",min_length=3, max_length=64)
    description: Optional[str] = Body(None, Description="Description of the Job post.")

    class Config:
        schema_extra = {
            "example": {
                "title": "Technical Team Lead",
                "description": "A Lead with an experience of at least 2 years with diverse software development background.",
            }
        }



class job:

    def __init__(self, title: str, description: str, created_by: Optional[int]=None, updated_by: Optional[int]=None):
        self.title = title
        self.description = description
        self._updated_by = updated_by
        self._updated_date = datetime.today()
        self._created_date = datetime.today()
        self._created_by = created_by

    def insert(self):
        query = "INSERT INTO public.job (title, description, created_by, updated_by, created_date, updated_date) Values(%s,%s,%s,%s,%s,%s)"
        val = (self.title, self.description, self._created_by, self._updated_by, self._created_date, self._updated_date)
        return db_obj.insert(query, val)

    @staticmethod
    def insert_(title: str, description: Optional[str]= None, created_by: Optional[int]=None):
        try:
            query = "INSERT INTO public.job (title, description, created_by, updated_by, created_date, updated_date) Values(%s,%s,%s,%s,%s,%s)"
            val = (title, description, created_by, created_by, datetime.today(), datetime.today())
            return db_obj.insert(query, val)
        except Exception as ex:
           raise Exception(str(ex))

    @staticmethod
    def update_(id: int, title: Optional[str]=None, description: Optional[str]=None, updated_by: Optional[int]=None):
        try:
            query = None
            if id and title and description:
                query = "UPDATE public.job SET title='%s', description='%s', updated_by='%s', updated_date='%s' WHERE id=%s"\
                        % (title, description, updated_by, datetime.today(), id)
            elif id and title:
                query = "UPDATE public.job SET title='%s', updated_by='%s', updated_date='%s' WHERE id=%s"\
                        % (title, updated_by, datetime.today(), id)
            elif id and description:
                query = "UPDATE public.job SET description='%s', updated_by='%s', updated_date='%s' WHERE id=%s"\
                        % (description, updated_by, datetime.today(), id)
            if query:
                return db_obj.update(query, None)
            else:
                raise Exception("Please enter atleast one value to be updated Title/description.")
        except Exception as ex:
             #print(str(ex))   return None
             raise Exception(ex)


    @staticmethod
    def delete_(id:int):
        try:
            if id:
                query = "DELETE FROM public.job WHERE id=%s" % id
                return db_obj.delete(query, None)
            return 0
        except Exception as ex:
            #print('delete', str(ex))
            raise Exception(str(ex))


    @staticmethod
    def all_():
        query = "SELECT j.id AS \"Id\", title AS \"Title\", description AS \"Description\", cuser.fullname AS \"Created By\", uuser.fullname AS \"Modified By\", TO_CHAR(created_date, 'dd/mm/yyyy hh:mm:ss') AS \"Created Date\", TO_CHAR(updated_date, 'dd/mm/yyyy hh:mm:ss') AS \"Updated Date\" FROM public.job AS j LEFT JOIN public.user AS cuser ON " \
                "j.created_by=cuser.id LEFT JOIN public.user AS uuser ON j.updated_by=uuser.id ORDER BY j.id"
        return db_obj.select_all(query)


if __name__ == "__main__":
    try:
        result = job.update_(200, None, None, 3)
        print(result)
    except Exception as ex:
        print(str(ex))

