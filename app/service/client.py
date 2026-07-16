import httpx
from app.core.config import settings
async def get_csrf_tokens() -> str:

    async with httpx.AsyncClient() as client:
        response= await client.get(
            settings.SAP_ODATA_URL,
            auth= (settings.SAP_USERNAME, settings.SAP_PASSWORD.get_secret_value()),
            headers= {settings.XSRF_HEADER_NAME: settings.XSRF_FETCH_VALUE}
        ) 

        if response.status_code!=200:
            raise Exception(f"Failed to fetch CSRF token. Status= {response.status_code}")
        
        token= response.headers.get(settings.XSRF_HEADER_NAME)

        if not token:
            raise Exception("CSRF token not found in response headers")
        
        return token
    
async def send_sap_post_request(token:str, request_id: str, items_batch: list):

    payload= {
        "request_id": request_id,
        "ToItem": items_batch
    }

    async with httpx.AsyncClient() as client:
        headers= {
            settings.XSRF_HEADER_NAME: token,
            "Content-type": "application/json",
            "Accept": "application/json"
        }

        response= await client.get(
            settings.SAP_ODATA_URL,
            auth= (settings.SAP_USERNAME, settings.SAP_PASSWORD.get_secret_value()),
            headers=headers,
            json= payload,
            timeout=60.0
        )

        if response.status_code not in [200,201]:
            raise Exception(f"Failed to post transaction data, status={response.status_code}, message= {response.text}") 

        return response.json()