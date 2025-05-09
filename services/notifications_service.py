import httpx
from models.request_model import RequestCreate
from utils.logger import logger
import os

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL")
NOTIFICATIONS_URL = os.getenv("NOTIFICATIONS_URL")

async def notif_created_req(request_data: RequestCreate, token: str):
    try:
        async with httpx.AsyncClient() as client:
            # Obtener info del usuario solicitado
            
            if request_data.request_type == "internal":
                
                solicited_user = await client.get(
                    f"{USERS_SERVICE_URL}/get-em/{request_data.solicitant_user_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if solicited_user.status_code != 200:
                    logger.warning("No se pudo obtener la información del usuario solicitante (internal).")
                    return
                
                solicitant_user = await client.get(
                    f"{USERS_SERVICE_URL}/get-em/{request_data.solicited_user_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if solicitant_user.status_code != 200:
                    logger.warning("No se pudo obtener la información del usuario solicitante (internal).")
                    return
                solicited_user_data = solicited_user.json()
                solicitant_user_data = solicitant_user.json()

                payload = {
                    "solicitant_email": solicitant_user_data["email"],
                    "solicitant_name": solicitant_user_data["name"],

                    "solicited_email": solicited_user_data["email"],
                    "solicited_name": solicited_user_data["name"],

                    "documents": request_data.documents
                }
                print(payload)

            
                print(f"{NOTIFICATIONS_URL}/send_req_int")
                await client.post(
                    f"{NOTIFICATIONS_URL}/send_req_int",
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"}
                )


            elif request_data.request_type == "external":
                
                solicitant_user = await client.get(
                    f"{USERS_SERVICE_URL}/get-em/{request_data.solicitant_user_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if solicitant_user.status_code != 200:
                    logger.warning("No se pudo obtener la información del usuario solicitante (internal).")
                    return
                solicitant_user_data = solicitant_user.json()
                payload = {
                    "solicitant_email": solicitant_user_data["email"],
                    "solicitant_name": solicitant_user_data["name"],

                    "solicited_email": request_data.ext_data["email"],
                    "solicited_name": request_data.ext_data["name"],
                    "documents": request_data.documents
                }


                await client.post(
                    f"{NOTIFICATIONS_URL}/send_req_ext",
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"}
                )

    except Exception as e:
        logger.error(f"⛔ Error al enviar notificación interna: {e}")



async def notif_approved_req(token: str, doc, urls):
    try:
        async with httpx.AsyncClient() as client:
            
            if  doc["type"] == "internal":

                solicited_user = await client.get(
                    f"{USERS_SERVICE_URL}/get-em/{doc['solicitated_user_id']}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if solicited_user.status_code != 200:
                    logger.warning("No se pudo obtener la información del usuario solicitante (internal).")
                    return
                
                solicitant_user = await client.get(
                    f"{USERS_SERVICE_URL}/get-em/{doc['solicitant_user_id']}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if solicitant_user.status_code != 200:
                    logger.warning("No se pudo obtener la información del usuario solicitante (internal).")
                    return
                solicited_user_data = solicited_user.json()
                solicitant_user_data = solicitant_user.json()

                payload = {
                    "solicitant_email": solicitant_user_data["email"],
                    "solicitant_name": solicitant_user_data["email"],


                    "solicited_email": solicited_user_data["name"],
                    "solicited_name": solicited_user_data["name"],
 
                    "documents": urls
                }

                await client.post(
                    f"{NOTIFICATIONS_URL}/send_req_int",
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"}
                )
                


            elif doc["type"] == "external":

                solicitant_user = await client.get(
                    f"{USERS_SERVICE_URL}/get-em/{doc['solicitant_user_id']}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if solicitant_user.status_code != 200:
                    logger.warning("No se pudo obtener la información del usuario solicitante (internal).")
                    return
                solicitant_user_data = solicitant_user.json()

                payload = {
                    "solicitant_email": solicitant_user_data["email"],
                    "solicitant_name": solicitant_user_data["name"],
                    
                    "solicited_email": doc["ext_data"]["email"],
                    "solicited_name": doc["ext_data"]["name"],

                    "documents": urls
                }


                await client.post(
                    f"{NOTIFICATIONS_URL}/send_req_ext",
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"}
                )

    except Exception as e:
        logger.error(f"⛔ Error al enviar notificación interna: {e}")