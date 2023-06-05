from pydantic import BaseModel
from datetime import datetime as dt


class UsersChatSchema(BaseModel):
    from_user_uuid: str
    message_content: str
    created_date: str = dt.now().strftime("%Y-%m-%d %H:%M")
