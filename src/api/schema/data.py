from pydantic import BaseModel, Field

class DocumentMatched(BaseModel):
    doc_name: str
    doc_location: str
    score: float

class DocumentMatchedData(BaseModel):
    query: str
    doc_matched: list[DocumentMatched] = Field(
        ..., description="List of documents matched with their Scores."
    )
    total_matched: int = Field(
        default=0, description="Total number of documents matched."
    )
    
class DocumentMatchedResponse(BaseModel):
    data: DocumentMatchedData = Field(
        ...,
        description="Document Matched Data, containing the List of documents matched with their Scores.",
    )
    respTime: float = Field(
        ..., description="Response Time in seconds.", examples=[1.332]
    )
    message: str = Field(
        ..., description="Response Message.", examples=["Document matched Completed"]
    )