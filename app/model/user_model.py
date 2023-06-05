from pydantic import BaseModel, Field, EmailStr


class UsersSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email_id: EmailStr = Field()
