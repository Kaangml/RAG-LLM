import google.generativeai as genai
from .config import get_api_key
from query_docs.result_displayer import to_markdown

class ChatBot:
    def __init__(self, system_instruction=None):
        """
        ChatBot sınıfının constructor'ı.
        API anahtarını alır ve genai modülünü yapılandırır.
        
        Eğer system_instruction sağlanmazsa, varsayılan bir prompt kullanılır.
        """
        self.api_key = get_api_key()
        genai.configure(api_key=self.api_key)
        
        # Varsayılan system_instruction'ı tanımla
        self.default_system_prompt = """ You are an attentive and supportive academic assistant.
        Your role is to provide assistance based solely on the provided context.

        Here’s how we’ll proceed:
        1. I will provide you with a question and related text excerpt.
        2. Your task is to answer the question using only the provided partial texts.
        3. If the answer isn’t explicitly found within the given context,
        respond with 'I don't know'.
        4. After each response, please provide a detailed explanation.
        Break down your answer step by step and relate it directly to the provided context.
        5. Sometimes, I will ask questions about the chat session, such as summarize
        the chat or list the question etc. For this kind of questions do not try
        to use the provided partial texts.
        6. Generate the answer in the same language of the given question.

        If you're ready, I'll provide you with the question and the context.
        """
        
        # Eğer system_instruction verilmemişse, varsayılanı kullan
        self.system_instruction = system_instruction or self.default_system_prompt
        
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=self.system_instruction)
        self.chat = self.model.start_chat(history=[])

    def generate_answer(self, prompt, context):

        context = str(context)  # context bir liste ya da sözlükse str'e dönüştür ****
        response = self.chat.send_message(prompt + context)
        return response

    def history_chat(self):
        """
        Mevcut sohbet geçmişi.
        """
        return self.history
