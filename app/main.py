from fastapi import FastAPI
from app.core import security, log_config
from app.routers import chat ,users
#from app.db.db_neo4j import async_neo4j_driver

logger = log_config.configure_logging()

app = FastAPI()
security.add_cors(app)
app.include_router(chat.router)
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)