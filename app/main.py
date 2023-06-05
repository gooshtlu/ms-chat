from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.chat import router as user_chat_router
app = FastAPI()

app.include_router(users_router)
app.include_router(user_chat_router)