import os
import shutil

class ChromaDBDelete:
    def __init__(self, chromaDB_path):
        self.chromaDB_path = chromaDB_path

    def delete_all_files_and_folders(self):
        if os.path.exists(self.chromaDB_path):
            print(f"The directory '{self.chromaDB_path}' already exists.")
            permission = input("Do you want to delete all the files and folders in this directory? (y/n): ")
            if permission.lower() == "y":
                shutil.rmtree(self.chromaDB_path)
                print(f"All files and folders in '{self.chromaDB_path}' have been deleted.")
            else:
                print("No action taken.")
        else:
            print(f"The directory '{self.chromaDB_path}' does not exist.")
