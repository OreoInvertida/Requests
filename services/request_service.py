from database.mongodb import mongo
from models.request_model import RequestCreate
from datetime import datetime
from fastapi import HTTPException
from uuid import uuid4
from bson import ObjectId

async def create_request(request_data: RequestCreate):
    collection = mongo.db["requests"]
    
    new_request = {
        "id": str(uuid4()),
        "date": datetime.utcnow(),
        "status": "pendiente",
        "description": request_data.description,
        "documents": [doc.dict() for doc in request_data.documents],
        "solicitant_user_id": request_data.solicitant_user_id,
        "solicited_user_id": request_data.solicited_user_id
    }

    await collection.insert_one(new_request)
    return {"message": "Solicitud creada exitosamente", "request_id": new_request["id"]}



async def get_requests_for_user(user_id: str):
    if mongo.db is None:
        raise Exception("MongoDB no está conectado.")

    collection = mongo.db["requests"]

    # Consultar solicitudes como solicitante
    as_requester = await collection.find({"solicitant_user_id": user_id}).to_list(length=None)

    # Consultar solicitudes como solicitado
    as_requested = await collection.find({"solicited_user_id": user_id}).to_list(length=None)

    def serialize_request(r):
        r["_id"] = str(r["_id"])
        return {
            "id": r["_id"],
            "date": r["date"],
            "status": r["status"],
            "description": r.get("description", ""),
            "files": r["files"],
            "solicitant_user_id": r["solicitant_user_id"],
            "solicited_user_id": r["solicited_user_id"],
        }

    return {
        "as_requester": [serialize_request(r) for r in as_requester],
        "as_requested": [serialize_request(r) for r in as_requested]
    }
