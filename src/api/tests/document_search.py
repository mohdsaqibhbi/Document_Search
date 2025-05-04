from tests.load_env import load_env_vars

load_env_vars()

import time
from services.document_search.inference import DocumentSearchEngine
from schema.data import DocumentMatchedResponse

if __name__ == "__main__":
    
    search_engine = DocumentSearchEngine()
    
    start = time.time()
    
    query = "Snake"
    document_matched_data = search_engine.search(query)
    
    message = "Document Search Completed"
    inference_time = round(time.time() - start, 3)
    
    document_matched_response = DocumentMatchedResponse(
        data=document_matched_data,
        respTime=inference_time,
        message=message,
    )
    
    print("Response:")
    print(document_matched_response.json())
    print("Done")