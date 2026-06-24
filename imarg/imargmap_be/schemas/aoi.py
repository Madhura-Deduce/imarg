from pydantic import BaseModel
from typing import Dict


class CreateAOIRequest(BaseModel):
    name: str
    geometry: Dict


class AOIResponse(BaseModel):
    id: int
    name: str

class ValidateAOIRequest(BaseModel):
    geometry: Dict