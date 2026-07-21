import sqlite3
import os
from contextlib import contextmanager

DB_NAME= "sap_data.db"

def init_db():

        conn= sqlite3.connect(DB_NAME)
        cursor= conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions(
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

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sap_sync_logs(
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT DEFAULT 'PENDING',
            start_record_id INTEGER NOT NULL,
            end_record_id INTEGER NOT NULL,
            total_records INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        conn.commit()
        conn.close()
        print(f"Database {DB_NAME} and sync logs table created successfully")


def get_db_connection():

    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn       