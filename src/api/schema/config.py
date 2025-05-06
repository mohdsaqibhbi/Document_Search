import json
import os
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class Document(BaseModel):
    location: str
    doc_type: list[str]
    location_type: str = "local"

class BM25(BaseModel):
    k: float
    b: float
    delta: float
    
class TextPreprocessor(BaseModel):
    pattern: str

class AppConfig(BaseModel):
    documents: Document
    bm25: BM25
    text_preprocessor: TextPreprocessor

    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        with open(os.path.join(os.getcwd(), "config.json"), "r") as f:
            config = json.load(f)
        super().__init__(*args, **{**kwargs, **config})

class AzureBlobConfig(BaseSettings):
    connection_str: str = Field(
        ..., alias="BLOB_CONNECTION_STR", description="Blob connection string"
    )
    container_name: str = Field(
        ..., alias="CONTAINER_NAME", description="Blob container name"
    )