from typing import Dict

from pydantic import BaseModel


class CreateAOIRequest(BaseModel):
    name: str
    geometry: Dict


class ValidateAOIRequest(BaseModel):
    geometry: Dict


class AOIResponse(BaseModel):
    id: int
    name: str