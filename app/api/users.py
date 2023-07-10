from fastapi import APIRouter
from app.common import constants
from app.db import CouchDB

from app.model.user_model import UsersSchema
from app.task.user_task import check_email

router = APIRouter()
db_instance = CouchDB(constants.COUCHDB_USERS_DATABASE_NAME)


@router.post("/users")
async def add_users(user: UsersSchema):
    result = check_email(user.email_id)
    if result:
        return "This is email is already exist, Please Enter Unique Email_id"
    else:
        result = db_instance.create_document(user.dict())
        return "A New User is created"


@router.get("/getuser/{user_id}")
async def get_user_by_id(user_id):
    result = db_instance.get_document(user_id)
    return result


@router.get("/check_email/{email_id}")
async def check_email_id(email_id):
    selector = {
        "selector": {
            "email_id": {
                "$eq": str(email_id)
            }
        }
    }
    result = db_instance.find(selector)
    return result


@router.get("/get-user-by-id/{user_id}")
async def get_user_by_id(user_id):
    selector = {
        "selector": {
            "_id": {
                "$eq": str(user_id)
            }
        }
    }
    result = db_instance.find(selector)
    return result


@router.get("/get-user-by-name/{username}")
async def get_user_by_name(username):
    selector = {
        "selector": {
            "username": {
                "$eq": str(username)
            }
        }
    }
    result = db_instance.find(selector)
    return result


@router.get("/get-all-users")
async def get_all_users():
    result = db_instance.get_all_users()
    return result
