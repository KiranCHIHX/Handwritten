#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
import json
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone, timedelta

from app.schema.pyobject import PyObjectId
from app.schema.transaction import TransactionInfo, OperationStatus
from app.utils import utilities as U

class ClassiferRequest(BaseModel):
    Field1: str
    OptionalField2: Optional[str] = None
    Field3: str
    ListField: List[str]
    
    # Validation and json convertor for pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
        
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "Field1": "1234",
                "OptionalField2": "1234",
                "Field3": "1234",
                "ListField": [
                    "Some text value",
                    "Some more text value"
                ]
            }
        }
        
class RequestInfo(BaseModel):
    Claim_ID: Optional[str]
    Client_ID: Optional[str]
    Hospital_ID: Optional[str]
    Total_Lines: int
    
class IRDALabels(BaseModel):
    L1: str
    L2: str
    L3: str
    
class ClientLables(BaseModel):
    L1: Optional[str]
    L2: Optional[str]
    L3: Optional[str]
    
    
class ClassiferInfo(BaseModel):
    Line_IDX: int
    Text: str
    Classifer_Status: OperationStatus
    IRDA_Labels: IRDALabels
    Client_Labels: ClientLables
    NME: bool
    NHI: bool
    
class ClassiferResponse(BaseModel):
    Transaction_Info: TransactionInfo
    Request_Info: RequestInfo
    Classifers: List[ClassiferInfo]
    # Validation and json convertor for pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
        
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "Transaction_Info": {
                        "Transaction_ID": "1234",
                        "Received_TS" : "",
                        "Processed_TS" : ""
                    },
                "Request_Info": {
                        "Claim_ID": "1234",
                        "Client_ID": "1234",
                        "Total_Lines": 1,
                    },
                "Classifers": [
                    {
                        "Line_IDX": 0,
                        "Text": "ssome text value",
                        "Classifer_Status": "Success",
                        "IRDA_Labels": {
                                "L1": "label",
                                "L2": "label",
                                "L3": "label",
                            },
                        "Client_Labels": {
                                "L1": "label",
                                "L2": "label",
                                "L3": "label",
                            },
                        "NME": True,
                        "NHI": False
                    }
                ]
            }
        }
    