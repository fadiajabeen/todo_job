import datetime
from typing import Optional, List, Set
import jwt
from fastapi import FastAPI, Query, status, Response, HTTPException
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash, check_password_hash

from models.response_models import ResponseBase, ResponseList
from models.job import job, JobInsertModel
from models.user import user



app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK, response_model=ResponseList)
def get_all_jobs(user_id: int = Depends(user.get_current_user_id)):
    try:
        result = job.all_()
        if result:
            return JSONResponse(status_code=200, content={"code": 200, "message": '%s records found.' % len(result) ,"jobs":result})
        else:
            raise HTTPException(status_code=204, detail='No jobs found. Please insert few.')
            #return JSONResponse(status_code=204, content={"code": 204, "message": 'No jobs found. Please insert few.'})
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/add_job/{job}", status_code=status.HTTP_201_CREATED, response_model=ResponseBase)
def add_job(job_obj: JobInsertModel, user_id: int = Depends(user.get_current_user_id)):  # , response: Response
    try:
        result = job.insert_(job_obj.title, job_obj.description, user_id)
        if result and result>0:
            return JSONResponse(status_code=201, content={"code": 201, "message": "Job added successfully."})
        else:
            raise HTTPException(status_code=500, detail='Unable to add the job right now. Please try again later')
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.put("/edit_job", status_code=status.HTTP_200_OK, response_model=ResponseBase)
def edit_job(id: int, title: Optional[str] = Query(None, min_length=3, max_length=64), description: Optional[str] = None, user_id: int = Depends(user.get_current_user_id)):
    try:
        result = job.update_(id, title, description, user_id)
        if result and result > 0:
            return JSONResponse(status_code=200, content={"code": 200, "message": 'Job with Id %s updated successfully.'%id})
        else:
            raise HTTPException(status_code=500, detail='Unable to update the job right now. Job may not exist.')
    except Exception as error:
        if not str(error) or len(str(error)) == 0:
            error = "Job doesn't exist. Please enter valid job id."
        #return JSONResponse(status_code=400, content={"code": 400, "message": str(error)})
        raise HTTPException(status_code=400, detail=str(error))


@app.delete("/delete_job/{id}", status_code=status.HTTP_200_OK, response_model=ResponseBase)
def delete_job(id: int, user_id: int = Depends(user.get_current_user_id)):
    try:
        result = job.delete_(id)
        if result and result > 0:
            return JSONResponse(status_code=200, content={"code": 200, "message": 'Job with Id %s deleted successfully.' % id})
        else:
            return JSONResponse(status_code=200, content={"code": 200, "message": "Either job doesn't exist or it is already deleted."})
    except Exception as error:
        if not str(error) or len(str(error))==0:
            error = "Job doesn't exist. Please enter valid job id."
        raise HTTPException(status_code=400, detail=str(error))

# uvicorn main:app --reload


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_obj = user.filter_by_(form_data.username)
        if not user_obj:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        if check_password_hash(user_obj[2], form_data.password):
            token = user.create_token_(user_obj[0])
            return JSONResponse(status_code=200, content={"code": 200, "message": 'Login successful.', "access_token": token, "token_type": "bearer"})
        else:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))