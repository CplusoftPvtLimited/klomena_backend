import logging
import traceback

import humps
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi import APIRouter, Response, status, Depends, Request
from sqlalchemy.orm import Session

from constants import response_body, EXCEPTION_MSG, SUCCESS_MSG
from models import get_db
from whatsapp_chat_bot_management.utils import twilio_receive_message, ask_question_to_chat_bot
from whatsapp_chat_bot_management.whatsapp_chat_bot_schema import *

router = APIRouter()


@router.post('/api/v2/whatsapp-chat-bot/ask-question', tags=['Whatsapp Chat Bot'])
def ask_question(response: Response, as_question_schema: AskQuestionSchema, db: Session = Depends(get_db)):

    message, status_code, chat_data = ask_question_to_chat_bot(db=db,
                                                               question=as_question_schema.question,
                                                               number=as_question_schema.number)
    response_body['message'] = message
    response_body['data'] = humps.camelize(jsonable_encoder(chat_data))
    response.status_code = status.HTTP_200_OK
    return JSONResponse(content=response_body, status_code=response.status_code)


@router.post('/api/v2/whatsapp-chat-bot/twilio/receive-message', tags=['Whatsapp Chat Bot'])
async def receive_message(response: Response, request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    try:
        # Extract incomng parameters from Twilio
        message = form_data['Body']
        number = form_data['From']

        twilio_receive_message(db=db, message=message, number=number)
        message = SUCCESS_MSG
        status_code = status.HTTP_200_OK
    except Exception as exc:
        logging.exception(str(exc))
        traceback.print_exc()
        message = EXCEPTION_MSG
        status_code = status.HTTP_400_BAD_REQUEST
    response_body['message'] = message
    response_body['data'] = []
    response.status_code = status_code
    return JSONResponse(content=response_body, status_code=response.status_code)