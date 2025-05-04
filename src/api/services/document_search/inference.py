import os
from globals import cfg, azure_cfg
from services.data.azure_blob import AzureBlobReader
from services.data.load_data import DocumentLoader
from services.data.preprocess import TextPreprocessor
from services.document_search.search_engine import BM25
from schema.data import DocumentMatched, DocumentMatchedData

class DocumentSearchEngine:
    def __init__(self):
        
        if cfg.documents.location_type == "local":
            file_list = [os.path.join(cfg.documents.location, file) for file in os.listdir(cfg.documents.location)]
        else:
            blob_reader = AzureBlobReader(
            azure_cfg.connection_string, 
            azure_cfg.container_name, 
            cfg.documents.location)
        
            file_list = blob_reader.get_file_paths_from_folder()
            
        self.documents = DocumentLoader(
                file_list, 
                cfg.documents.doc_type).load_documents()
        
        preprocessor = TextPreprocessor(cfg.text_preprocessor.pattern)
        
        self.bm25 = BM25(
            self.documents, 
            preprocessor, 
            cfg.bm25.k, 
            cfg.bm25.b,
            cfg.bm25.delta
            )

    def search(self, query) -> DocumentMatchedData:
        
        results = self.bm25.score(query)
        document_matched: list[DocumentMatched] = [
            DocumentMatched(
                doc_name=self.documents[doc_id]["filename"], 
                doc_location=self.documents[doc_id]["location"], 
                score=round(score, 2)
            ) for doc_id, score in results
        ]
        document_matched_data = DocumentMatchedData(
            query=query, 
            doc_matched=document_matched,
            total_matched=len(results)
        )
        
        return document_matched_data