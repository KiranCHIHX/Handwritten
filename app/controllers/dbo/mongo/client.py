#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
import uuid
import json
from bson import json_util
from datetime import datetime, timezone

from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from fastapi import FastAPI, Body, HTTPException, status

import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from app.utils import exception as E 
from app.core.config import cfg

class MongoStore():
    def __init__(self):
        self.client = MongoClient(cfg.store.mongodb.MongoClient, connect=False)
        self.db = self.client[cfg.store.mongodb.db]
        
    def GetDocuments(self):
        pass
    
    def GetDocument(self):
        pass
    
    def InsertDocument(self):
        pass
    
    def UpdateDocument(self):
        pass