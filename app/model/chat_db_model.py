from couchdb import ResourceNotFound
from pydantic import BaseModel, validator
from datetime import datetime as dt

from app.common import constants
from app.db import CouchDB


class UsersChatSchema(BaseModel):
    from_user_uuid: str
    message_content: str
    created_date: str = dt.now().strftime("%Y-%m-%d %H:%M")

    @validator('from_user_uuid')
    def check_user_exists(cls, from_user_uuid):
        user_db_instance = CouchDB(constants.COUCHDB_USERS_DATABASE_NAME)

        result = user_db_instance.get_document(from_user_uuid)
        if result is None:
            raise ValueError("This user does not exist")

        return from_user_uuid


def check_if_email_exists(email_ids: list):
    user_db_instance = CouchDB(constants.COUCHDB_USERS_DATABASE_NAME)

    for email in email_ids:
        selector = {
            "selector": {
                "email_id": {
                    "$eq": str(email)
                }
            }
        }

        result = user_db_instance.find(selector)
        if len(result) == 0:
            return False, email

    return True, email_ids


class GroupSchema(BaseModel):
    admins: list
    managers: list
    writers: list
    readers: list
    group_name: str

    @validator('admins', 'managers', 'writers', 'readers', pre=True)
    def check_admins_exist(cls, values):
        exists, mail = check_if_email_exists(values)
        if not exists:
            raise ValueError(f"This email_id {mail} does not exist")
        return values


class SendGroupMessage(BaseModel):
    from_email_id: str
    message_content: str
    created_date: str = dt.now().strftime("%Y-%m-%d %H:%M")


class ChangeRoleSchema(BaseModel):
    user: str
    change_user_role: str
    role: str


class AddUserToGroup(BaseModel):
    email_id: str


class UpdateChatMessages(BaseModel):
    user_id: str
    to_user_uuid: str
    from_user_uuid: str
    message_content: str
    created_date: str = dt.now().strftime("%Y-%m-%d %H:%M")
