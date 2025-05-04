from azure.storage.blob import BlobServiceClient, ContainerClient
from typing import List, Optional

class AzureBlobReader:
    def __init__(self, connection_string: str, container_name: str, base_path: str):
        """
        Initialize the BlobReader with the Azure storage credentials and container details.
        
        :param connection_string: Azure Blob Storage connection string
        :param container_name: Name of the container in Azure Blob Storage
        :param base_path: Path to the base folder (e.g., "Document_Search/data")
        """
        self.connection_string = connection_string
        self.container_name = container_name
        self.base_path = base_path
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def _list_blobs(self, prefix: str) -> List[str]:
        """
        List all blobs within a specific prefix (folder or sub-folder).

        :param prefix: Folder path to list files from
        :return: List of blob names (paths)
        """
        blob_list = self.container_client.list_blobs(name_starts_with=prefix)
        return [blob.name for blob in blob_list]

    def get_file_paths_from_folder(self, folder_path: Optional[str] = None) -> List[str]:
        """
        Get all file paths in a folder (and subfolders) in the Blob Storage.

        :param folder_path: The path to the folder within the container (optional, defaults to base_path)
        :return: List of file paths (blob names)
        """
        if folder_path is None:
            folder_path = self.base_path
        
        # List all blobs in the folder (and its subfolders)
        blobs = self._list_blobs(folder_path)

        return blobs
