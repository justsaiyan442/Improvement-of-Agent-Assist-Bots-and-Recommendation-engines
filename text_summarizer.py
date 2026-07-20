import os
from mistralai import Mistral

class TextSum:
    def __init__(self, speech):
        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.model = "mistral-large-latest"
        self.text = speech

    def text_summarization(self):
        try:
            client = Mistral(api_key=self.api_key)
            chat_response = client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the given text into a 5 line paragraph maximum: {self.text}",
                    },
                ]
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            print("API not connected",e)

