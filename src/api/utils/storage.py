from azure.storage.blob import BlobClient, BlobServiceClient
from globals import blob_config
from io import BytesIO
        
        
def download_data_blob(blob_name: str) -> bytes:

    blob_client = BlobClient.from_connection_string(
        blob_config.connection_str, blob_config.container_name, blob_name
    )
    
    with BytesIO() as data_stream:
        blob_client.download_blob().readinto(data_stream)
        return data_stream.getvalue()
    
def read_file_from_blob(blob_name: str) -> str:

    data = download_data_blob(blob_name)
    return data

def get_list_of_blobs(location) -> list[str]:

    blob_service_client = BlobServiceClient.from_connection_string(blob_config.connection_str)
    container_client = blob_service_client.get_container_client(blob_config.container_name)
    
    blobs = [blob.name for blob in container_client.list_blobs(location)]
    return blobs    