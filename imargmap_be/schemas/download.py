from pydantic import BaseModel
from typing import Dict


class DownloadRequest(BaseModel):
    geometry: Dict
    format: str