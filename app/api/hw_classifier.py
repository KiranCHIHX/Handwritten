#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
from dataclasses import dataclass
import os
import sys
import time
from datetime import datetime
import tempfile
import shutil
import json
from fastapi import APIRouter, HTTPException, UploadFile, Response
from app.controllers.processors import image as PI

from app.core import logger
from app.utils import utilities as U
from app.utils import constants as C


router = APIRouter(prefix="/document")
# logger = logger.log_setup(cfg, "app")
# create a temporary directory for processing
temp_dirpath = tempfile.mkdtemp()


@router.post("/classify")
async def Classifer(file: UploadFile):
    """API route to Classifer Claims."""
    _response = {
        "Transaction_Info": {"Transaction_ID": "1234", "Received_TS": "", "Processed_TS": ""},
        "prob": 0.0,
        "is_hw": False,
    }
    # 1. Get the line items
    start_time = time.time()
    start_dt = datetime.now()
    trxId = start_dt.strftime(r"%Y%m%d%H%M%S%f")
    logger.info(f"{U.prepend_msg(trxId)}{C.HEADER_10} Received Request {C.HEADER_10}")
    try:
        # Begin process

        logger.info(f"{U.prepend_msg(trxId)} - Begin Processing Request -> {start_time}")

        file_data = await file.read()
        # write the file to temperory directory for processing
        upload_dir = os.path.join(temp_dirpath, trxId)
        os.makedirs(upload_dir, exist_ok=True)
        upload_filepath = os.path.join(upload_dir, file.filename)  # f'./uploads/{txn_id}_{file.filename}'

        with open(upload_filepath, "wb") as upload_file:
            upload_file.write(file_data)
        logger.debug(f"{U.set_log_prefix(trxid = trxId)} - File saved upload_filepath.")

        result = await PI.process_image(trxId=trxId, image_path=upload_filepath)
        end_time = time.time()
        logger.info(
            f"{U.prepend_msg(trxId)} - End Processing Request -> {end_time} - Time Taken -> {end_time - start_time}"
        )
        end_dt = datetime.now()
        _response["Transaction_Info"]["Transaction_ID"] = trxId
        _response["Transaction_Info"]["Received_TS"] = start_dt
        _response["Transaction_Info"]["Processed_TS"] = end_dt
        _response["Model_Version"] = result["Model_Version"]
        _response["prob"] = result["prob"]
        _response["is_hw"] = result["is_hw"]
    except Exception as e:
        logger.error(
            f"{U.prepend_msg(trxId)} - there's an error uploading file. Please try again!!!",
            exc_info=True,
        )
        error_message = {
            "Status": C.ERROR,
            "Error": "Error while Uploading file. TRY AGAIN!!",
            "Error-Message": str(e),
        }
        raise HTTPException(status_code=418, detail=f"Error - there's an error uploading file. Please try again!!!")
    logger.info(f"{U.prepend_msg(trxId)} - Response Request -> {_response}")
    # remove the temporary directory
    shutil.rmtree(temp_dirpath, ignore_errors=True)
    return Response(
        content=json.dumps(_response, indent=4, sort_keys=True, default=str),
        media_type="application/json",
    )
