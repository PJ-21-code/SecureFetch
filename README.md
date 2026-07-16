readme_content = """# SAP OData Integration Service

This project is a high-performance, asynchronous backend service built with **FastAPI** to facilitate data synchronization between a local database and an SAP OData-based enterprise system.

## Project Overview
The service bridges the gap between local transaction management and SAP’s OData requirements. It handles CSRF token negotiation, data chunking (batching) for optimized SAP ingestion, and robust error logging.

## Key Features
- **Async Processing:** Built on `httpx` and `FastAPI` for high-concurrency performance.
- **Resilient Batching:** Automatically splits large database records into manageable chunks (default: 50 records) to prevent SAP connection timeouts.
- **CSRF Protection:** Implements an automated handshake protocol to fetch and manage security tokens required by SAP.
- **Transactional Integrity:** Maintains an audit trail by preserving `request_id` linkages while ensuring unique submission IDs.

## Tech Stack
- **Framework:** FastAPI
- **Database Interaction:** SQLite (via standard Python driver)
- **HTTP Client:** `httpx` (Asynchronous)
- **Data Validation:** Pydantic

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd sap-integration-service