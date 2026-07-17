import sqlite3
import os

DB_NAME= "sap_data.db"

def init_db():

    if not os.path.exists(DB_NAME):
        conn= sqlite3.connect(DB_NAME)
        cursor= conn.cursor()

        cursor.execute("""
        CREATE TABLE Transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER DEFAULT NULL,           
            nid TEXT,
            nlineNo TEXT,
            docNo TEXT,
            itemNumber TEXT,
            transactionDate TEXT,
            polholdName TEXT,
            dC TEXT,
            accntCode TEXT,
            amount REAL,
            product TEXT,
            channel TEXT,
            location TEXT,
            assignment TEXT,
            transactionReference TEXT,
            chequeNo TEXT,
            sourceSystem TEXT,
            strPolCostStr TEXT,
            strUtrNbr TEXT,
            strAgentCd TEXT,
            strPyNum TEXT,
            strDtlUinCode TEXT,
            sapBatchNo TEXT,
            sapRecord TEXT,
            sapRecordDt TEXT,
            dtCreated TEXT,
            strCreatedBy TEXT,
            transactionDateEod TEXT           
            );

        """)

        conn.commit()
        conn.close()
        print(f"Database {DB_NAME} created succesfully")


def get_db_connection():

    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn    