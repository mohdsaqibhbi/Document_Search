import os
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
from pathlib import Path
from io import BytesIO
from utils.storage import get_list_of_blobs, read_file_from_blob

class DocumentLoader:
    def __init__(self, location, doc_type=[".txt"], location_type="local"):
        
        self.location = location
        self.doc_type = doc_type
        self.location_type = location_type
    
    def load_txt_or_csv_doc(self, file_path):

        with open(file_path, 'r', encoding='utf-8') as f:
           content = f.read()
           return content
       
    def load_pdf_doc(self, data):
        reader = PdfReader(data)
        content = str("\n".join([page.extract_text() for page in reader.pages if page.extract_text()]))
        return content
    
    def load_png_doc(self, data):
        image = Image.open(data)
        content = pytesseract.image_to_string(image)
        return content
            
    def load_docs_from_file_paths(self):
        
        docs = {}
        for doc_id, filename in enumerate(os.listdir(self.location)):
            _, ext = os.path.splitext(filename)
            if ext in self.doc_type:
                file_path = os.path.join(self.location, filename)
                
                if ext == ".png":
                    content = self.load_png_doc(file_path)
                elif ext == ".pdf":
                    content = self.load_pdf_doc(file_path)
                elif ext in [".txt", ".csv"]:
                    content = self.load_txt_or_csv_doc(file_path)
                
                docs[doc_id] = {
                    "filename": filename,
                    "location": file_path, 
                    "content": content
                }
                
        return docs
    
    def load_docs_from_blob(self):
        
        blob_list = get_list_of_blobs(self.location)
        
        docs = {}
        for doc_id, blob_name in enumerate(blob_list):
            ext = Path(blob_name).suffix
            if ext in self.doc_type:
                blob_data = read_file_from_blob(blob_name)
            
                if ext == ".png":
                    blob_data = BytesIO(blob_data)
                    content = self.load_png_doc(blob_data)
                elif ext == ".pdf":
                    blob_data = BytesIO(blob_data)
                    content = self.load_pdf_doc(blob_data)
                elif ext in [".txt", ".csv"]:
                    content = blob_data.decode("utf-8")
                    
                docs[doc_id] = {
                    "filename": blob_name,
                    "location": blob_name, 
                    "content": content
                }
                
        return docs
    
    def load_documents(self):
        if self.location_type == "local":
            return self.load_docs_from_file_paths()
        elif self.location_type == "azure":
            return self.load_docs_from_blob()