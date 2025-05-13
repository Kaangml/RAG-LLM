import ollama
from .config import get_system_prompt
from query_docs.result_displayer import to_markdown

class ChatBotOllama:
    def __init__(self, model_name='my-model-name', system_instruction=None):
        """
        Yerel Ollama modelini kullanan ChatBot sınıfı.
        """
        # Model adı ve sistem promptunu al
        self.model_name = model_name
        self.system_instruction = system_instruction or get_system_prompt()
        self.history = []

    def generate_answer(self, prompt, context):
        """
        Soruyu ve bağlamı kullanarak yanıt üretir.
        """
        # context'i string'e dönüştür
        context = str(context)
        full_prompt = f"{self.system_instruction}\n\n{prompt}\n\nContext:\n{context}"

        # Ollama chat fonksiyonunu kullanarak yanıt al
        response = ollama.chat(model=self.model_name, messages=[
            {'role': 'system', 'content': self.system_instruction},
            {'role': 'user', 'content': full_prompt}
        ])

        # Yanıtı al ve geçmişe ekle
        answer = response['message']['content']
        self.history.append({"prompt": prompt, "response": answer})
        return answer

    def history_chat(self):
        """
        Mevcut sohbet geçmişini döndürür.
        """
        return self.history