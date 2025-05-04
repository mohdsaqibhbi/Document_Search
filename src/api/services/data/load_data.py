import os
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
from exceptions.data import DataBaseException

class DocumentLoader:
    def __init__(self, file_list, doc_type=[".txt"]):
        
        if file_list:
        
            self.file_list = file_list
            self.doc_type = doc_type
            self.reader_map = {
                ".txt": self.load_txt_or_csv_doc,
                ".csv": self.load_txt_or_csv_doc,
                ".pdf": self.load_pdf_doc,
                ".png": self.load_png_doc
            }
        else:
            raise DataBaseException(
                "Documents are not found in the specified location."
            )
    
    def load_txt_or_csv_doc(self, file_path):

        with open(file_path, 'r', encoding='utf-8') as f:
           content = f.read()
           return content
       
    def load_pdf_doc(self, file_path):
        
        reader = PdfReader(file_path)
        content = str("\n".join([page.extract_text() for page in reader.pages if page.extract_text()]))
        return content
    
    def load_png_doc(self, file_path):
        content = pytesseract.image_to_string(Image.open(file_path))
        return content
            
    def load_documents(self):
        
        docs = {}
        for doc_id, file_path in enumerate(self.file_list):
            filename = os.path.basename(file_path)
            _, ext = os.path.splitext(filename)
            if ext in self.doc_type:
                content = self.reader_map.get(ext)(file_path)
                docs[doc_id] = {
                    "filename": filename,
                    "location": file_path, 
                    "content": content
                }
                
        return docs