from services.document_search.inference import DocumentSearchEngine
from schema.data import DocumentMatchedData

search_engine = DocumentSearchEngine()

async def get_search_documents(query: str) -> DocumentMatchedData:
    
    document_matched_data = search_engine.search(query)
    return document_matched_data