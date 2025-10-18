import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

class FileUploader:
    @staticmethod
    def select_files(file_types="all"):
        """
        Dosya seçme dialogu açar
        
        Args:
            file_types: "pdf", "csv", veya "all"
        """
        root = Tk()  # Ana pencereyi oluştur
        root.withdraw()  # Ana pencereyi gizle
        
        if file_types == "pdf":
            filetypes = [("PDF Files", "*.pdf")]
            title = "Select PDF files"
        elif file_types == "csv":
            filetypes = [("CSV Files", "*.csv")]
            title = "Select CSV files"
        else:  # all
            filetypes = [("PDF and CSV Files", "*.pdf *.csv"), ("PDF Files", "*.pdf"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
            title = "Select files (PDF or CSV)"
        
        file_paths = askopenfilenames(title=title, filetypes=filetypes)
        root.destroy()  # Ana pencereyi yok et
        return list(file_paths)

    @staticmethod
    def validate_files(file_paths):
        """PDF ve CSV dosyalarını doğrular"""
        valid_files = [f for f in file_paths if os.path.isfile(f) and f.lower().endswith(('.pdf', '.csv'))]
        return valid_files
