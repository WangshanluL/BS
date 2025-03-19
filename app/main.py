from fastapi import FastAPI
from app.core import  log_config
from app.routers import chat
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import users, articles, comments, chats
from app.core.config import settings
logger = log_config.configure_logging()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
# app.include_router(articles.router, prefix=f"{settings.API_V1_STR}/articles", tags=["articles"])
# app.include_router(comments.router, prefix=f"{settings.API_V1_STR}/comments", tags=["comments"])
# app.include_router(chats.router, prefix=f"{settings.API_V1_STR}/chats", tags=["chats"])


app.include_router(chat.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)