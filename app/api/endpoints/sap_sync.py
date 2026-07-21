from fastapi import APIRouter,HTTPException,status

from app.service.client import get_csrf_tokens, send_sap_post_request
from app.service.db_service import get_items_from_db, create_sap_sync_logs,update_sync_log_status,update_transactions_request_id
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
async def post_transaction(base_requestid: int= 0):

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

            start_record= chunk[0].get("id", i+1)
            end_record= chunk[-1].get("id", i+len(chunk))

            request_id= await create_sap_sync_logs(start_id=start_record, end_id= end_record,total= len(chunk))
            payload = SapPayload(
                RequestId= request_id, 
                ToItem= items_as_models
            )

            try:

               sap_response= await send_sap_post_request(token, payload.model_dump())

               await update_sync_log_status(request_id= request_id, status= "SUCCESS")
               await update_transactions_request_id(start_id= start_record, end_id=end_record, request_id=request_id)

               result.append({
                   "request_id": request_id,
                   "status": "SUCCESS",
                   "start_record": start_record,
                   "end_record": end_record,
                   "sap_response": sap_response
                })

            except Exception as batch_error:
               await update_sync_log_status(request_id=request_id,status="FAILED")
               raise RuntimeError(f"Failed at Request-ID {request_id} (Records {start_record}-{end_record}): {str(batch_error)}")

        return {
            "status": "success",
            "message": "Transaction data posted successfully",
            "details": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error posting to SAP: {str(e)}")
