from app.schemas.transactions import TransactionItem
from app.database.connections import get_db_connection
async def get_items_from_db(request_id: str):
    conn = get_db_connection()
    try:
      cursor = conn.cursor()

      cursor.execute("SELECT * FROM Transaction WHERE request_id= ?", (request_id,))

      rows= cursor.fetchall()

      items= [dict(row) for row in rows]

      validate_items=[]
      for item in items:
          validate_item= TransactionItem(**item)
          validate_items.append(validate_item.model_dump())

      return validate_items

    except Exception as e:
       print(f"Database Error: {str(e)}")
       raise e

    conn.close()    