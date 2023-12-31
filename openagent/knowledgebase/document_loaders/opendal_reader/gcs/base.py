"""Gcs file and directory reader.

A loader that fetches a file or iterates through a directory on Gcs.

"""

from typing import Dict, List, Optional, Union

from openagent import download_loader
from openagent.knowledgebase.document_loaders.basereader import BaseReader
from openagent.schema import DocumentNode


class OpendalGcsReader(BaseReader):
    """General reader for any Gcs file or directory."""

    def __init__(
        self,
        bucket: str,
        path: str = "/",
        endpoint: str = "",
        credentials: str = "",
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
    ) -> None:
        """Initialize Gcs container, along with credentials if needed.

        If key is not set, the entire bucket (filtered by prefix) is parsed.

        Args:
        bucket (str): the name of your gcs bucket
        path (str): the path of the data. If none is provided,
            this loader will iterate through the entire bucket. If path is endswith `/`, this loader will iterate through the entire dir. Otherwise, this loeader will load the file.
        endpoint Optional[str]: the endpoint of the azblob service.
        credentials (Optional[str]): provide credential string for GCS OAuth2 directly.
        file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text. See `SimpleDirectoryReader` for more details.

        """
        super().__init__()

        self.path = path
        self.file_extractor = file_extractor

        # opendal service related config.
        self.options = {
            "bucket": bucket,
            "endpoint": endpoint,
            "credentials": credentials,
        }

    def load_data(self) -> List[DocumentNode]:
        """Load file(s) from OpenDAL."""

        try:
            from openagent.knowledgebase.document_loaders.utils import import_loader

            OpendalReader = import_loader("OpendalReader")
        except ImportError:
            OpendalReader = download_loader("OpendalReader")
        loader = OpendalReader(
            scheme="gcs",
            path=self.path,
            file_extractor=self.file_extractor,
            **self.options,
        )

        return loader.load_data()
