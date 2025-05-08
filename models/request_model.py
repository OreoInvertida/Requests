from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class DocumentRequest(BaseModel):
    document_name: str

class RequestCreate(BaseModel):
    description: str = ""
    documents: List[DocumentRequest]
    solicitant_user_id: str
    solicited_user_id: str

class RequestInDB(RequestCreate):
    id: str
    date: datetime
    status: str  # pendiente, aprobada, rechazada
