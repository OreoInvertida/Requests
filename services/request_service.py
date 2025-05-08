from database.mongodb import mongo
from models.request_model import RequestCreate
from datetime import datetime
from fastapi import HTTPException
from uuid import uuid4
from bson import ObjectId
from services.notifications_service import notif_created_req, notif_approved_req


async def create_request(request_data: RequestCreate, token: str):
    collection = mongo.db["requests"]
    
    new_request = {
        "request_id": str(uuid4()),
        "date": datetime.utcnow(),
        "status": "pendiente",
        "description": request_data.description,
        "documents": request_data.documents,
        "solicitant_user_id": request_data.solicitant_user_id,
        "solicited_user_id": request_data.solicited_user_id,
        "ext_data": request_data.ext_data,
        "type": request_data.request_type
    }

    await collection.insert_one(new_request)

    await notif_created_req(request_data=request_data, token=token)
    
    return {"message": "Solicitud creada exitosamente", "request_id": new_request["request_id"]}


async def get_requests_for_user(user_id: str):
    if mongo.db is None:
        raise Exception("MongoDB no está conectado.")

    collection = mongo.db["requests"]
    user_id = int(user_id)

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
            "documents": r["documents"],
            "solicitant_user_id": r["solicitant_user_id"],
            "solicited_user_id": r["solicited_user_id"],
        }

    return {
        "as_requester": [serialize_request(r) for r in as_requester],
        "as_requested": [serialize_request(r) for r in as_requested]
    }


async def approve_request(request_id: str, token: str):
    if mongo.db is None:
        raise Exception("MongoDB no está conectado.")

    collection = mongo.db["requests"]
    doc = await collection.find_one({"request_id": request_id})


    result = await collection.update_one(
        {"request_id": request_id},
        {
            "$set": {
                "status": "aprobada",
                "fulfilled_at": datetime.utcnow(),
            }
        }
    )


    urls = ["doc1","doc2"] ###### GET BUCKET LINKS HERE

    await notif_approved_req( token=token, doc=doc, urls=urls)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    
    return {"message": "Solicitud actualizada exitosamente."}