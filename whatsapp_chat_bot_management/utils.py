import logging
import os
import traceback

from fastapi import status

from api.web_chat_bot_management.models import user_details
from connector_providers.twilio.twilio_integration import twilio_send_message
from constants import EXCEPTION_MSG, SUCCESS_MSG
from utilities import BOT
from dotenv import load_dotenv

load_dotenv()

bot = BOT()

# Session dictionary to track user message counts
session = {}


def twilio_receive_message(db, message, number):
    encoded_number = bot.encode_user(number)
    user_obj = db.query(user_details).filter(user_details.number == encoded_number).first()
    if user_obj is None:
        system_prompt = os.getenv("SYSTEM_PROMPT")
        user_meta = {
            "conversation": {
                "messages": [  # Change the prompt parameter to messages parameter
                    {"role": "system", "content": system_prompt}
                ]
            }
        }
        user_detail = user_details(number=encoded_number, user_meta=user_meta)
        db.add(user_detail)
        db.commit()
    user_obj = db.query(user_details).filter(user_details.number == encoded_number).first()
    if number not in session:
        session[number] = 1
    else:
        session[number] += 1

    # Handle user sessions based on message count
    if session[number] == 1:
        receive_message_logic(db=db, content=message, number=number, user_obj=user_obj)
    elif session[number] == 2:
        receive_message_logic(db=db, content=message, number=number, user_obj=user_obj)
    elif session[number] == 3:
        # Send GUI link after the third message
        messages = update_chat(db, role="user", content=message,
                               number=encoded_number, user_obj=user_obj)
        # Get response from Openai
        question_result = bot.ask_question(messages)

        gui_url = f" For further queries visit this site: {os.getenv('GUI_LINK')}"
        result = question_result + '\n' + gui_url + f'/{encoded_number}'
        twilio_send_message(number, result)
        user_obj = db.query(user_details).filter(user_details.number == encoded_number).first()
        messages = update_chat(db, role="assistant", content=result,
                               number=encoded_number, user_obj=user_obj)
        session[number] = 0
    else:
        receive_message_logic(db=db, content=message, number=number, user_obj=user_obj)


def receive_message_logic(db, content, number, user_obj):
    encoded_number = bot.encode_user(number)
    messages = update_chat(db, role="user", content=content,
                           number=encoded_number, user_obj=user_obj)
    # Get response from Openai
    result = bot.ask_question(messages)

    twilio_send_message(number, result)

    user_obj = db.query(user_details).filter(user_details.number == encoded_number).first()
    messages = update_chat(db, role="assistant", content=result,
                           number=encoded_number, user_obj=user_obj)


# Function to update messages in the conversation
def update_chat(db, role, content, number, user_obj):
    existing_json = user_obj.user_meta

    # New message to be added
    new_message = {"role": role, "content": content}

    # Append the new message to the existing messages
    existing_json['conversation']['messages'].append(new_message)

    db.query(user_details).filter(user_details.number == number).update({"user_meta": existing_json})
    db.commit()
    user_obj = db.query(user_details).filter(user_details.number == number).first()

    if user_obj:
        return user_obj.user_meta["conversation"]["messages"]


def ask_question_to_chat_bot(db, question, number):
    try:
        user_obj = db.query(user_details).filter(user_details.number == number).first()
        if user_obj:
            messages = update_chat(db, role="user", content=question,
                                   number=number, user_obj=user_obj)
            # Get response from Openai
            result = bot.ask_question(messages)
            user_obj = db.query(user_details).filter(user_details.number == number).first()
            messages = update_chat(db, role="assistant", content=result,
                                   number=number, user_obj=user_obj)

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
