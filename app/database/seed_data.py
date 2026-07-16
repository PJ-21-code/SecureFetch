import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'sap_data.db')

def seed_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    record = (
        "REQ123",           
        "NID001",          
        "L001",             
        "DOC001",          
        "ITEM99",           
        "2026-07-16",       
        "John Doe",         
        "Debit",            
        "ACC555",           
        1500.50,            
        "ProductA",         
        "Web",              
        "Delhi",            
        "Assign01",         
        "Ref888",           
        "CHQ12345",         
        "SAP_SYS",          
        "CC_01",            
        "UTR999",           
        "AGT01",            
        "PV01",             
        "UIN123",           
        "BATCH01",          
        "REC01",            
        "2026-07-16",       
        "2026-07-16",       
        "Admin",            
        "2026-07-16"        
    )

    cursor.execute('''
        INSERT INTO transactions (
            request_id, nid, nlineNo, docNo, itemNumber, transactionDate, 
            polholdName, dC, accntCode, amount, product, channel, location, 
            assignment, transactionReference, chequeNo, sourceSystem, 
            strPolCostCtr, strUtrNbr, strAgentCd, strPvNum, strDtlUinCode, 
            sapBatchNo, sapRecord, sapRecordDt, dtCreated, strCreatedBy, 
            transactionDateEod
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', record)

    conn.commit()
    conn.close()
    print("Successfully seeded one record into sap_data.db!")

if __name__ == "__main__":
    seed_data()