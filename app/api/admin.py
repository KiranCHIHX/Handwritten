#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
from fastapi import APIRouter
from app.core.config import cfg

router = APIRouter(prefix="/admin")

@router.get("/healthz")
async def healthz():
    return {"Status": "OK"}

@router.get("/version")
async def version():
    return {"Version": cfg.VERSION}

@router.get("/info")
async def info():
    return {"Version": cfg.VERSION}

# add checks for downstream APIs in microservice