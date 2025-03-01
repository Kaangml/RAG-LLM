import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

class FileUploader:
    @staticmethod
    def select_files():
        root = Tk()  # Ana pencereyi oluştur
        root.withdraw()  # Ana pencereyi gizle
        file_paths = askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
        root.destroy()  # Ana pencereyi yok et
        return list(file_paths)

    @staticmethod
    def validate_files(file_paths):
        valid_files = [f for f in file_paths if os.path.isfile(f) and f.lower().endswith('.pdf')]
        return valid_files
