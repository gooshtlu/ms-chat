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

