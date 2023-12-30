import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import json
import jwt

load_dotenv()


class BOT:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_AI_KEY")
        self.client = OpenAI()

        OpenAI.api_key = os.getenv("OPEN_AI_KEY")

    def update_model_name(self, new_model):
        os.environ["MODEL"] = new_model
        # variable_name = 'MODEL'
        # file_path = '.env'
        # env_vars = dotenv_values(file_path)
        # env_vars[variable_name] = new_model
        # # Write the updated environment variables back to the .env file
        # set_key(file_path, variable_name, new_model)

    def get_job_status(self, job_id):
        return self.client.fine_tuning.jobs.retrieve(job_id).status

    def get_fine_tuned_model(self, job_id):
        return self.client.fine_tuning.jobs.retrieve(job_id).fine_tuned_model

    def update_tokens_file(self, tokens):
        current_date = datetime.now().strftime("%Y-%m-%d")

        file_name = os.path.join(os.getenv("RESOURCES_FOLDER"), current_date + ".txt")
        if os.path.exists(file_name):
            # Read the existing token count from the file
            with open(file_name, "r") as file:
                existing_tokens = int(file.read().split("=")[-1])
            # Update the token count
            tokens += existing_tokens
            # Write the updated token count back to the file
            with open(file_name, "w") as file:
                file.write(f"total_tokens={tokens}\n")
        else:
            # Create a new file and write the token count
            with open(file_name, "w") as file:
                file.write(f"total_tokens={tokens}\n")

    def ask_question(self, query):

        model = os.getenv("MODEL")
        temperature = int(os.getenv("TEMPERATURE"))
        system_prompt = os.getenv("SYSTEM_PROMPT")
        completion = self.client.chat.completions.create(  # Change the method name
            model=model,
            messages=[  # Change the prompt parameter to messages parameter
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=temperature,
        )
        response = completion.choices[0].message.content

        self.update_tokens_file(int(completion.usage.total_tokens))
        return response

    def chatbot(self, input_text, conversation_history=[]):
        response_text = self.ask_question(input_text)
        conversation_history.append((input_text, response_text))
        return conversation_history, conversation_history

    def save_whatsapp_identity(self, db, question, answer, encoded_number):

        from api.web_chat_bot_management.models import user_details
        user_obj = db.query(user_details).filter(user_details.number == encoded_number).first()
        if user_obj:

            existing_json = user_obj.user_meta

            # New message to be added
            new_message = {"role": "user", "content": question}

            # Append the new message to the existing messages
            existing_json['conversation']['messages'].append(new_message)

            # New message to be added
            new_answer = {"role": "assistant", "content": answer}
            # Append the new message to the existing messages
            existing_json['conversation']['messages'].append(new_answer)

            db.query(user_details).filter(user_details.number == encoded_number).update({"user_meta": existing_json})
            db.commit()
        else:
            user_meta = {
                "conversation": {
                    "messages": [  # Change the prompt parameter to messages parameter
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": answer},
                    ]
                }
            }
            user_detail = user_details(number=encoded_number, user_meta=user_meta)
            db.add(user_detail)
            db.commit()
        return True

     # encode the messages

    def encode_user(self, sender_id):
        """
        encode user payload as a jwt
        :param user:
        :return:
        """
        encoded_data = jwt.encode(
            payload={"wa_number": sender_id},
            key="encode_decode_wa_number",
            algorithm="HS256",
        )

        return encoded_data

    # decode the messages
    def decode_user(self, token: str):
        """
        :param token: jwt token
        :return:
        """
        decoded_data = jwt.decode(
            jwt=token, key="encode_decode_wa_number", algorithms=["HS256"]
        )

        return decoded_data
