import json
import os
from typing import Any

from pydantic import BaseModel

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
        
class AzureBlobConfig(BaseModel):
    connection_string: str = ""
    container_name: str = ""

    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        
        env_config = {}
        env_config_path = os.path.join(os.getcwd(), "env_config.json")
        if os.path.exists(env_config_path):
            with open(env_config_path, "r") as f:
                env_config = json.load(f)
        super().__init__(*args, **{**kwargs, **env_config})