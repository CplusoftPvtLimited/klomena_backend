import logging
import traceback
from fastapi import status

from api.web_chat_bot_management.models import user_details
from constants import EXCEPTION_MSG, SUCCESS_MSG


def get_user_chat(db, number):
    try:
        user_obj = db.query(user_details).filter(user_details.number == number).first()
        if user_obj:
            chat_data = {
                "id": user_obj.id,
                "number": user_obj.number,
                "creation_at": user_obj.creation_at,
                "conversation": user_obj.user_meta["conversation"]
            }
            message = SUCCESS_MSG
            status_code = status.HTTP_200_OK
        else:
            chat_data = []
            message = SUCCESS_MSG
            status_code = status.HTTP_200_OK
    except Exception as exc:
        logging.exception(str(exc))
        traceback.print_exc()
        message = EXCEPTION_MSG
        status_code = status.HTTP_400_BAD_REQUEST
        chat_data = []
    return message, status_code, chat_data
