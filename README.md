# SecureFetch Backend

This backend serves as the core orchestration engine, acting as a secure bridge between your local transaction storage and the SAP OData service[cite: 1].

## Backend Responsibilities

1 **Request Lifecycle Management**: The backend manages the end-to-end synchronization process, initiating actions the moment a request is triggered[cite: 1].
2 **Intelligent Batching**: To maintain system stability, the backend automatically partitions large datasets into smaller, manageable chunks for transmission[cite: 1].
3 **Dynamic Tracking**: It generates unique identifiers for every batch (e.g., REQ_B1, REQ_B2), ensuring an accurate audit trail of which records were processed[cite: 1].
4 **Strict Data Validation**: The system utilizes Pydantic to validate every transaction against the required schema before transmission, catching potential formatting errors early[cite: 1].
5 **Secure API Communication**: The backend functions as a secure client that handles authentication and transmits validated JSON payloads to SAP via standard POST requests[cite: 1].
6 **Synchronization Confirmation**: It monitors SAP's responses; upon receiving a successful status (200 or 201), it confirms the upload and marks records as processed to prevent duplicate transmissions[cite: 1].

## Getting Started

1 **Installation**: Clone the repository and install the dependencies listed in `requirements.txt`[cite: 1].
2 **Execution**: Start the FastAPI server using `uvicorn main:app --reload`[cite: 1].
3 **Operation**: The system will automatically begin orchestrating the validation, batching, and transmission of records to your configured SAP OData endpoint[cite: 1].