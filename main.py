import secrets

import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api.routers import web_chat_bot, whatsapp_chat_bot
from database import DATABASE_URL

logging.basicConfig(filename='error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

tags_metadata = [
    {
        "name": "Web Chat Bot",
        "description": "Web Chat Bot Integration Api's",
    },
    {
        "name": "Whatsapp Chat Bot",
        "description": "Whatsapp Chat Bot Integration Api's",
    }
]
sys.dont_write_bytecode = True

description = """
Klomena API helps you do awesome stuff
"""
app = FastAPI(
    openapi_tags=tags_metadata,
    title="Klomena",
    description=description,
    version="0.0.2",
    docs_url=None
)

origins = [
    "http://localhost:4200",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(web_chat_bot.router)
app.include_router(whatsapp_chat_bot.router)

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "$$test.com1122!!")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/docs")
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/api-docs")
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/api.json", title="docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)