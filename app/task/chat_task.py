from app.common import constants
from app.db import CouchDB
import uuid

chat_db_instance = CouchDB(constants.COUCHDB_CHAT_DB_DATABASE_NAME)


def check_message(user_chat_schema):
    selector = {
        "selector": {
            "to_user_uuid": {
                "$eq": str(user_chat_schema['to_user_uuid'])
            }
        }
    }

    result = chat_db_instance.find(selector)

    if result:
        if result[0]['from_user_uuid'] == user_chat_schema['from_user_uuid'] and result[0]['to_user_uuid'] \
                == user_chat_schema['to_user_uuid']:
            return result
    else:
        return False
