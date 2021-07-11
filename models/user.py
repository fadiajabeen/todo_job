import datetime

from database.database_access import Database
import base64
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from werkzeug.security import generate_password_hash, check_password_hash

db_obj = Database()
Key = "eriy457=-86grdf3ecr';/.,t322!@$@fsdfse3r%$"
Oauth2_Scheme = OAuth2PasswordBearer(tokenUrl="token")

class user:

    def _init__(self, name, username, password):
        self.fullname = name
        self.username = username.lower()
        self.password = generate_password_hash(password, method='sha256')

    def insert(self):
        query = "INSERT INTO public.user (fullname, username, password) Values(%s,%s,%s)"
        val = (self.fullname, self.username.lower(), self.password)
        return db_obj.insert(query, val)

    @staticmethod
    def insert_(name, username, password):
        query = "INSERT INTO public.user (fullname, username, password) Values(%s,%s,%s)"
        val = (name, username.lower(), generate_password_hash(password, method='sha256'))
        return db_obj.insert(query, val)

    @staticmethod
    def filter_by_(username=None):
        if username:
            query = "SELECT id, username, password, fullname FROM public.user WHERE username LIKE '%s'" % username.lower()
            return db_obj.select_one(query, None)
        else:
            return None

    @staticmethod
    def get_user_from_token(token: str):
        try:
            data = jwt.decode(token, Key)
            current_user = user.filter_by_(data['id']).first()
            return current_user
        except Exception as error:
            raise Exception(str(error))

    @staticmethod
    def get_id_from_token(token: str):
        try:
            data = jwt.decode(token.replace("Bearer ",""), Key, algorithms=["HS256"])
            return data['id']
        except Exception as error:
            raise Exception(str(error))

    @staticmethod
    def create_token_(id:int):
        return jwt.encode({'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180)}, Key)

    @staticmethod
    async def get_current_user_id(token: str = Depends(Oauth2_Scheme)):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Token Required.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = user.get_id_from_token(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id



if __name__ == "__main__":
    try:
        user_obj = user()
        user_obj.insert_("Keven John", "keven.john", "r3ekcfr6efve")
    except Exception as ex:
        print(str(ex))