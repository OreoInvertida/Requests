from fastapi import APIRouter, HTTPException, Depends
from models.request_model import RequestCreate, ApprovalReq
from services.request_service import create_request, get_requests_for_user, approve_request
from services.token_service import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()
security = HTTPBearer()

@router.post("/create-req")
async def create_document_request(request: RequestCreate, token: dict = Depends(verify_token)):
    return await create_request(request, token)

@router.get("/user-req/{user_id}")
async def get_user_requests(user_id: str, payload: dict = Depends(verify_token)):
    try:
        return await get_requests_for_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/approve/{request_id}")
async def approve_request_route(request_id: str, request: ApprovalReq, authorized: bool = Depends(verify_token)):
    try:
        return await approve_request(request_id=request_id, request=request, token=authorized)
    except HTTPException as e:
        raise e
    
