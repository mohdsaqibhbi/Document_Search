import os

from schema.config import AppConfig, AzureBlobConfig
from utils.logging import create_logger

APP_NAME = os.environ.get("APPLICATION", "DocumentSearchAPI")
log = create_logger(application=APP_NAME)

api_version = "1.0"
api_root_path = "/api/documentSearch"
api_summary = "Document Search API"
api_description = """
Document Search API provides the capability to perform intelligent search across a collection of documents using natural 
language queries.
The goal of the Document Search API is to retrieve the most relevant documents that match the user's query.
The API offers search endpoint to support various document retrieval.
"""

cfg = AppConfig()
azure_cfg = AzureBlobConfig()

log.info_print(f"Starting {APP_NAME}")