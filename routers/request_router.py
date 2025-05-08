from fastapi import APIRouter, HTTPException, Depends
from models.request_model import RequestCreate
from services.request_service import create_request, get_requests_for_user
from services.token_service import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()
security = HTTPBearer()

@router.post("/create")
async def create_document_request(request: RequestCreate, payload: dict = Depends(verify_token)):
    return await create_request(request)

@router.get("/user-req/{user_id}")
async def get_user_requests(user_id: str, payload: dict = Depends(verify_token)):
    try:
        return await get_requests_for_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
