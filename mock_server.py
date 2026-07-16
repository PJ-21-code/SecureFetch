# mock_sap_server.py
from fastapi import FastAPI, Header, Response
import uuid
app = FastAPI()

@app.get("/mock-sap-service")
async def get_token():
    # Return a dummy CSRF token in the headers
    random_token = str(uuid.uuid4())
    response = Response(content='{"message": "Token fetched"}')
    response.headers["x-csrf-token"] = random_token
    return response

@app.post("/mock-sap-service")
async def post_transaction(request: dict):
    # Simulate a successful SAP response
    return {"status": "success", "SAP_data": {"id": "12345", "status": "posted"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)