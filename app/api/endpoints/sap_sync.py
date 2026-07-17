from fastapi import APIRouter,HTTPException,status

from app.service.client import get_csrf_tokens, send_sap_post_request
from app.service.db_service import get_items_from_db
from app.schemas.transactions import TransactionItem,SapPayload

router= APIRouter()

@router.get('/csrf', status_code= status.HTTP_200_OK)
async def get_token():

    try:
        token= await get_csrf_tokens()
        return {"CSRF-Token:" : token}
    except Exception as e:

        raise HTTPException(status_code= status.HTTP_502_BAD_GATEWAY, detail= f"Cound not fetch token: {str(e)}")
    
@router.post('/post-transaction', status_code= status.HTTP_201_CREATED)
async def post_transaction(base_requestid: str="REQ"):

    try: 

        items= await get_items_from_db(base_requestid)
        if not items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Transaction items not found!")
        
        chunk_size = 1000 # no of records that will go in one time

        token= await get_csrf_tokens()
        result=[]


        for i in range(0, len(items), chunk_size):
            chunk = items[i : i+chunk_size]
            items_as_models = [TransactionItem(**item) for item in chunk]

            batch_num = (i // chunk_size) + 1
            dynamic_request_id = f"{base_requestid}_B{batch_num}"

            payload = SapPayload(
                RequestId= dynamic_request_id, 
                ToItem= items_as_models
            )

            sap_response= await send_sap_post_request(token, payload.model_dump())
            result.append(sap_response)

        return {
            "status": "success",
            "message": "Transaction data posted successfully",
            "Request-ID": dynamic_request_id,
            "SAP_data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error posting to SAP: {str(e)}")
