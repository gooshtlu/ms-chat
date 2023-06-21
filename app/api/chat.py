import uuid

from fastapi import APIRouter

from app.common import constants
from app.db import CouchDB
from app.model.chat_db_model import UsersChatSchema, GroupSchema, SendGroupMessage, ChangeRoleSchema, AddUserToGroup, \
    UpdateChatMessages
from app.task.chat_task import check_message, type_of_user, change_user_role
from app.task.user_task import check_user_id, check_email

router = APIRouter()
chat_db_instance = CouchDB(constants.COUCHDB_CHAT_DB_DATABASE_NAME)
group_chat_db_instance = CouchDB(constants.COUCHDB_GROUP_CHAT_DB_DATABASE_NAME)


@router.post("/users-chat/{from_user_uuid}/{to_user_uuid}/{user_chat_id}")
async def send_chat_message(user_chat_schema: UsersChatSchema, to_user_uuid, from_user_uuid, user_chat_id: str = None):
    user_chat_schema = user_chat_schema.dict()

    users_chat_content = {
        'to_user_uuid': to_user_uuid,
        'from_user_uuid': from_user_uuid,
        "chat_history": {}
    }

    message = user_chat_schema
    users_chat_content["chat_history"][str(uuid.uuid4())] = message

    result = check_user_id(to_user_uuid)  # checking user is exist in users db or not
    if result:
        chat_history_result = check_message(from_user_uuid, to_user_uuid)
        if chat_history_result and result and user_chat_id == chat_history_result[0]['_id']:
            chat_history_result[0]['chat_history'][str(uuid.uuid4())] = user_chat_schema
            chat_db_instance.update_document(chat_history_result[0]['_id'], chat_history_result[0])
            return "Successfully sent message"
        elif result:
            chat_db_instance.create_document(users_chat_content)
            return "Successfully sent message"
    else:
        return "User is not exists"


@router.put("/update-chat/{user_chat_id}")
async def update_chat(user_chat_schema: UpdateChatMessages, user_chat_id):
    user_chat_schema = user_chat_schema.dict()
    f_user_id = user_chat_schema['user_id']
    t_user_id = user_chat_schema['to_user_uuid']
    del user_chat_schema["user_id"]
    del user_chat_schema["to_user_uuid"]

    result = check_user_id(t_user_id)
    if result:
        chat_history_result = check_message(f_user_id, t_user_id)
        if result and chat_history_result and user_chat_id == chat_history_result[0]['_id']:
            chat_history_result[0]['chat_history'][str(uuid.uuid4())] = user_chat_schema
            result = chat_db_instance.update_document(chat_history_result[0]['_id'], chat_history_result[0])
            print(result)
            return "Successfully sent message"
        else:
            return "This Group is not Exists"

    else:
        return "This is user is not exists"


@router.post("/create-group")
async def create_chat_group(group_schema: GroupSchema):
    dict_data = group_schema.dict()
    dict_data['chat_history'] = {}  # Adding this line to initialize chat_history dictionary
    group_chat_db_instance.create_document(dict_data)
    return "A New Group is Created"


@router.post("/send-group-messages/{to_group_id}")
async def send_group_messages(group_message_schema: SendGroupMessage, to_group_id):
    group_message_schema = group_message_schema.dict()
    result = group_chat_db_instance.get_document(to_group_id)

    if result:
        user_type = group_message_schema['from_email_id']
        result_type = type_of_user(result, user_type)
        if result_type == "admin" or result_type == "manager" or result_type == "writer":
            result["chat_history"][str(uuid.uuid4())] = group_message_schema
            group_chat_db_instance.update_document(result['_id'], result)
            return " Message sent Successfully"
        else:
            return " You don't have to access to sent a message in this group"
    else:
        return "This is Group is not Exit"


@router.put("/edit-messages/{group_id}/{message_id}")
async def edit_message(update_group_massage: SendGroupMessage, message_id, group_id):
    result = group_chat_db_instance.get_document(group_id)
    chat_history = result.get('chat_history')
    if message_id in chat_history:
        update_group_massage_dict = update_group_massage.dict()
        user_type = update_group_massage_dict['from_email_id']
        result_type = type_of_user(result, user_type)
        if result_type == "admin" or result_type == "manager":
            result['chat_history'][message_id] = update_group_massage_dict
            group_chat_db_instance.update_document(group_id, result)
            return "Successfully updated the message"
        else:
            return "You don't have access to edit this message"

    else:
        return "This message does not exist"


@router.post("/change-role/{group_id}")
async def change_role(change_role_schema: ChangeRoleSchema, group_id):
    result = group_chat_db_instance.get_document(group_id)
    change_role_schema_dict = change_role_schema.dict()
    user_type = change_role_schema_dict['user']
    result_type = type_of_user(result, user_type)
    if result_type == "admin":
        result = change_user_role(group_id, result, change_role_schema_dict)
        if result:
            return "successfully changed the role...."
        else:
            return "This user does not exist in this group"
    elif result_type == "manager":
        if change_role_schema_dict['role'] == 'admin':
            return "Sorry you don't have access to changed the role"
        else:
            result = change_user_role(group_id, result, change_role_schema_dict)
            return "Successfully changed the role"


@router.post("/add-user-to-group/{group_id}")
async def add_user_to_group(add_user: AddUserToGroup, group_id):
    add_user_dict = add_user.dict()
    check_email_id = add_user_dict['email_id']
    result = check_email(check_email_id)
    if result:
        group_result = group_chat_db_instance.get_document(group_id)
        group_result['writers'].append(add_user_dict['email_id'])
        group_chat_db_instance.update_document(group_id, group_result)
        return "A New user is added to this group"
    else:
        return "UnKnown User "


@router.get("/flack-chat/{from_uuid}")
async def get_flack_chat(from_uuid):
    selector = {
        "selector": {
            "$or": [
                {"from_user_uuid": {"$eq": str(from_uuid)}},
                {"to_user_uuid": {"$eq": str(from_uuid)}}
            ]
        }
    }
    result = chat_db_instance.find(selector)
    return result


@router.get("/particular-user-chat/{from_uuid}/{to_uuid}")
async def get_particular_user_chat(from_uuid, to_uuid):
    selector = {
        "selector": {
            "$or": [
                {"from_user_uuid": {"$eq": str(from_uuid)}, "to_user_uuid": {"$eq": str(to_uuid)}},
                {"from_user_uuid": {"$eq": str(to_uuid)}, "to_user_uuid": {"$eq": str(from_uuid)}}
            ]
        }
    }
    result = chat_db_instance.find(selector)
    return result


@router.get("/group-messages/{group_name}")
async def get_group_messages(group_name):
    selector = {
        "selector": {
            "group_name": {
                "$eq": str(group_name)
            }
        }
    }
    result = group_chat_db_instance.find(selector)
    return result


@router.get("/all-groups")
async def get_all_flack_groups():
    result = group_chat_db_instance.get_all_users()
    return result
