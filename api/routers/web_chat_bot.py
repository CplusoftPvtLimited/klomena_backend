import humps
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.orm import Session

from api.web_chat_bot_management.utils import get_user_chat
from api.web_chat_bot_management.web_chat_bot_schema import WebChatBotSchema
from constants import response_body
from models import get_db

router = APIRouter()


@router.post('/api/v2/web-chat-bot/fetch-history', tags=['Web Chat Bot'])
def fetch_history(response: Response, web_chat: WebChatBotSchema, db: Session = Depends(get_db)):
    message, status_code, chat_data = get_user_chat(db, number=web_chat.number)

    response_body['message'] = message
    response_body['data'] = humps.camelize(jsonable_encoder(chat_data))
    response.status_code = status.HTTP_200_OK
    return JSONResponse(content=response_body, status_code=response.status_code)
