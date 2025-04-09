
from src.config import MODEL
from openai import OpenAI
import openai
from dotenv import load_dotenv
import os 
import logging
os.getenv("OPENAI_API_KEY")

load_dotenv()



logging.basicConfig(
    filename="logs/check_ai.log",
    filemode='w',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class AISummary:
    def __init__(
            self, 
            client, 
            model: str = "gpt-4o"
            ) -> None:
        """
        Initialises the AISummary instance.

        Args:
            client (openai.Client): The OpenAI API client.
            model (str, optional): The AI model to use. Defaults to "gpt-4o".
        """
        logging.info("Instantiated")
        self.client = client 
        self.model = model 

    def get_response(
            self,
            user_message:str,
            system_prompt:str,
            temperature:float=0.8,
            ) -> None:
        self.user_message = user_message
        self.system_prompt = system_prompt
        self.temperature = temperature

        response = self.client.chat.completions.create(
            model= self.model,
            temperature= self.temperature,
            messages=[
                {
                    "role":"system",
                    "content":self.system_prompt
                },
                {
                    "role": "user",
                    "content": self.user_message
                }
            ]
        )
        logging.info(response)
        return response.choices[0].message.content

