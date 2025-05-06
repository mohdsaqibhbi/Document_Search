from globals import cfg
from services.data.load_data import DocumentLoader
from services.data.preprocess import TextPreprocessor
from services.document_search.search_engine import BM25
from schema.data import DocumentMatched, DocumentMatchedData
from exceptions.data import DataBaseException

class DocumentSearchEngine:
    def __init__(self):
            
        self.documents = DocumentLoader(
                cfg.documents.location, 
                cfg.documents.doc_type,
                cfg.documents.location_type
                ).load_documents()
        
        if not self.documents:
            raise DataBaseException(
                    "Documents are not found in the specified location."
                )
        
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