from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.chat import router as user_chat_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(users_router)
app.include_router(user_chat_router)

origins = [
       "http://localhost:4200"  # Angular development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Content-Type"],
    expose_headers=["Access-Control-Allow-Origin"]
)
