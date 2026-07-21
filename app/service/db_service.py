from app.schemas.transactions import TransactionItem
from app.database.connections import get_db_connection

async def get_items_from_db(base_request_id: int = 0):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Transactions WHERE request_id = ?", (base_request_id,))
        rows = cursor.fetchall()

        items = [dict(row) for row in rows]
        
        validated_items = []
        for item in items:
            validated_item = TransactionItem(**item)
            validated_items.append(validated_item.model_dump())

        return validated_items
    except Exception as e:
        print(f"Database Error: {str(e)}")
        raise e
    finally:
        conn.close()


async def create_sap_sync_logs(start_id: int, end_id: int, total: int) -> int:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sap_sync_logs (status, start_record_id, end_record_id, total_records)
            VALUES (?, ?, ?, ?)
            """,
            ("PENDING", start_id, end_id, total)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


async def update_sync_log_status(request_id: int, status: str):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE sap_sync_logs 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE request_id = ?
            """,
            (status, request_id)
        )
        conn.commit()
    finally:
        conn.close()


async def update_transactions_request_id(start_id: int, end_id: int, request_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Transactions 
            SET request_id = ? 
            WHERE id BETWEEN ? AND ?
            """,
            (request_id, start_id, end_id)
        )
        conn.commit()
    finally:
        conn.close()