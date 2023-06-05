import uuid

from fastapi import APIRouter

from app.common import constants
from app.db import CouchDB
from app.model.chat_db_model import UsersChatSchema
from app.task.chat_task import check_message
from app.task.user_task import check_user_id

router = APIRouter()
chat_db_instance = CouchDB(constants.COUCHDB_CHAT_DB_DATABASE_NAME)


@router.post("/users-chat/{to_user_uuid}")
async def send_chat_message(user_chat_schema: UsersChatSchema, to_user_uuid):
    user_chat_schema = user_chat_schema.dict()

    users_chat_content = {
        'to_user_uuid': to_user_uuid,
        'from_user_uuid': user_chat_schema['from_user_uuid'],
        "chat_history": {}
    }

    message = user_chat_schema
    users_chat_content["chat_history"][str(uuid.uuid4())] = message

    result = check_user_id(to_user_uuid)  # checking user is exist in users db or not
    if result:
        chat_history_result = check_message(users_chat_content)
        if chat_history_result and result:
            chat_history_result[0]['chat_history'][str(uuid.uuid4())] = user_chat_schema
            chat_db_instance.update_document(chat_history_result[0]['_id'], chat_history_result[0])
            return "Successfully sent message"
        elif result:
            chat_db_instance.create_document(users_chat_content)
            return "Successfully sent message"
    else:
        return "User is not exists"
