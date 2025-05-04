import time

from fastapi import APIRouter
from globals import api_root_path, log
from interfaces.services import get_search_documents
from schema.data import DocumentMatchedResponse

router = APIRouter()


@router.get(
    "/search",
    description="""
        Provides document search capability for given queries. Returns the most relevant documents
        along with their scores based on the query.
    """,
)
async def search_documents(query: str) -> DocumentMatchedResponse:
    
    start = time.time()
    log.info_print("\n\nDocument Search Request Received")

    document_matched_data = await get_search_documents(query)
    
    message = "Document Search Completed"
    inference_time = round(time.time() - start, 3)
    log.info_print(
        f"Document Search API SUCCESS, Inference Time: {inference_time}",
        custom_dimensions={"method": f"{api_root_path}/search"},
    )
    
    return DocumentMatchedResponse(
        data=document_matched_data,
        respTime=inference_time,
        message=message,
    )