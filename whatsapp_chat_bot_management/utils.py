import logging
import os
import traceback

from fastapi import status

from api.web_chat_bot_management.models import user_details
from connector_providers.twilio.twilio_integration import twilio_send_message
from constants import EXCEPTION_MSG, SUCCESS_MSG
from utilities import BOT

bot = BOT()


def twilio_receive_message(db, message, number):
    encoded_number = bot.encode_user(number)

    # Get response from Openai
    result = bot.ask_question(message)

    user_obj = db.query(user_details).filter(user_details.number == encoded_number).first()
    if user_obj:
        count = len(user_obj.user_meta['conversation']['messages'])
        print("count", count)
        if count >= 3:
            gui_url = f" For further queries visit this site: {os.getenv('GUI_LINK')}"
            result = result + '\n' + gui_url + f'/{encoded_number}'
    twilio_send_message(number, result)

    bot.save_whatsapp_identity(db, message, result, encoded_number)


def ask_question_to_chat_bot(db, question, number):
    try:

        # Get response from Openai
        result = bot.ask_question(question)

        bot.save_whatsapp_identity(db, question, result, number)

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
