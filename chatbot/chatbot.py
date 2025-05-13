import google.generativeai as genai
from .config import get_api_key, get_system_prompt
from query_docs.result_displayer import to_markdown

class ChatBot:
    def __init__(self, system_instruction=None):
        """
        ChatBot sınıfının constructor'ı.
        API anahtarını alır ve genai modülünü yapılandırır.
        """
        self.api_key = get_api_key()
        genai.configure(api_key=self.api_key)
        
        # Sistem promptunu config'den al
        self.system_instruction = system_instruction or get_system_prompt()
        
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=self.system_instruction)
        self.chat = self.model.start_chat(history=[])

    def generate_answer(self, prompt, context):
        context = str(context)  # context bir liste ya da sözlükse str'e dönüştür
        response = self.chat.send_message(prompt + context)
        return response

    def history_chat(self):
        """
        Mevcut sohbet geçmişi.
        """
        return self.history