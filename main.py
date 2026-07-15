from fastapi import FastAPI, HTTPException
from app.api.endpoints import sap_sync

app= FastAPI(
    title= "SAP Integration Service",
    description= "API for posting CAMS transaction record to SAP Odata Service",
    version= "1.0.0"
)
app.include_router(sap_sync.router, prefix="/api", tags=["SAP Sync"])

@app.get('/')
async def root():

    return {
        "status": "online",
        "message": "SAP integeration service active"
    }





