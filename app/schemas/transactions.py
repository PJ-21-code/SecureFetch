from pydantic import BaseModel
from typing import List, Optional

class TransactionItem(BaseModel):

    nid: str
    nlineNo: str
    docNo: str
    itemNumber: str
    transactionDate: str
    polholdName: str
    dC: str
    accntCode: str
    amount: float
    product: str
    channel: str
    location: str
    assignment: str
    transactionReference: str
    chequeNo: str
    sourceSystem: str
    strPolCostStr: Optional[str]= None
    strUtrNbr: str
    strAgentCd: str
    strPyNum: Optional[str]= None
    strDtlUinCode: str
    sapBatchNo: str
    sapRecord: str
    sapRecordDt: str
    dtCreated: str
    strCreatedBy: str
    transactionDateEod: str

class SapPayload(BaseModel):
    RequestId: int
    ToItem: List[TransactionItem]    