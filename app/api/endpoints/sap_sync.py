from fastapi import APIRouter,HTTPException,status

from app.service.client import get_csrf_tokens, send_sap_post_request
from app.service.db_service import get_items_from_db

router= APIRouter()

@router.get('/csrf', status_code= status.HTTP_200_OK)
async def get_token():

    try:
        token= await get_csrf_tokens()
        return {"CSRF-Token:" : token}
    except Exception as e:

        raise HTTPException(status_code= status.HTTP_502_BAD_GATEWAY, detail= f"Cound not fetch token: {str(e)}")
    
@router.post('/post-transaction', status_code= status.HTTP_201_CREATED)
async def post_transaction(requestid: str):

    try: 

        items= await get_items_from_db(requestid: str)
        if not items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Transaction items not found!")
        token= await get_csrf_tokens()
        sap_response= await send_sap_post_request(token, requestid, items)

        return {
            "status": "success",
            "message": "Transaction data posted successfully",
            "SAP_data": sap_response
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error posting to SAP: {str(e)}")
