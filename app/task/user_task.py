from app.common import constants
from app.db import CouchDB

user_db_instance = CouchDB(constants.COUCHDB_USERS_DATABASE_NAME)


def check_email(email):
    selector = {
        "selector": {
            "email_id": {
                "$eq": str(email)
            }
        }
    }
    result = user_db_instance.find(selector)
    return result


def check_user_id(user_id):
    selector = {
        "selector": {
            "_id": {
                "$eq": str(user_id)
            }
        }
    }
    result = user_db_instance.find(selector)
    return result
