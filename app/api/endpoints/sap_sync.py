from fastapi import APIRouter,HTTPException,status

from app.service.client import get_csrf_token, send_sap_post_request
from app.schemas.transactions import SapPayload

router= APIRouter()

@router.get('/csrf', status_code= status.HTTP_200_OK)
async def get_token():

    try:
        token= await get_csrf_token()
        return {"CSRF-Token:" : token}
    except Exception as e:

        raise HTTPException(status_code= status.HTTP_502_BAD_GATEWAY, detail= f"Cound not fetch token: {str(e)}")
    
@router.post('/post-transaction', status_code= status.HTTP_201_CREATED)
async def post_transaction(payload: SapPayload):

    try: 
        token= await get_csrf_token()
        sap_response= await send_sap_post_request(token, payload.RequestId, payload.ToItem)

        return {
            "status": "success",
            "message": "Transaction data posted successfully",
            "SAP_data": sap_response
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error posting to SAP: {str(e)}")
