from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime



class RequestCreate(BaseModel):
    description: str = ""
    documents: List[str]
    solicitant_user_id: int
    solicited_user_id: int
    request_type: str
    ext_data: Dict[str,str]

class RequestInDB(RequestCreate):
    request_id: str
    date: datetime
    status: str  # pendiente, aprobada, rechazada


class ApprovalReq(BaseModel):
    documents_path: list[str]