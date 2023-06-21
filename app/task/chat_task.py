from app.common import constants
from app.db import CouchDB
import uuid

chat_db_instance = CouchDB(constants.COUCHDB_CHAT_DB_DATABASE_NAME)
group_chat_db_instance = CouchDB(constants.COUCHDB_GROUP_CHAT_DB_DATABASE_NAME)


def check_message(from_user_uuid, to_user_uuid):
    selector = {
        "selector": {
            "to_user_uuid": {
                "$eq": str(to_user_uuid)
            },
            "from_user_uuid": {
                "$eq": str(from_user_uuid)
            }

        }
    }

    result = chat_db_instance.find(selector)

    if result:
        if result[0]['from_user_uuid'] == from_user_uuid and result[0]['to_user_uuid'] \
                == to_user_uuid:
            return result
    else:
        return False


def type_of_user(result, user_type):
    admins = result['admins']
    managers = result['managers']
    writers = result['writers']
    readers = result['readers']

    if user_type in admins:
        return "admin"
    elif user_type in managers:
        return "manager"
    elif user_type in writers:
        return "writer"
    elif user_type in readers:
        return "reader"


def change_user_role(group_id, result, change_role_schema):
    my_keys = ['admins', 'managers', 'writers', 'readers']
    change_user_role_value = str(change_role_schema['change_user_role'])
    for key in my_keys:
        if key in result and change_user_role_value in result[key]:
            result[key].remove(change_user_role_value)
            key_values = {
                'admin': 'admins',
                'manager': 'managers',
                'writer': 'writers',
                'reader': 'readers'
            }
            try:
                result[key_values[change_role_schema['role']]].append(change_role_schema['change_user_role'])
                group_chat_db_instance.update_document(group_id, result)
                return result
            except Exception as e:
                print("An unexpected role was provided", e)
                return False
        else:
            return False