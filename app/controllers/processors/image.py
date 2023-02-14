#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
"""File Controller specific methods.

This provides a suite of methods to control the flow of logic
for files received for processing.

  Typical usage example:
  
  result = file._specif_Function(parameters)
"""
import os
import time
from datetime import datetime
from app.core import logger
from typing import List
from joblib import Parallel, delayed, parallel_backend

from app.controllers.AI import G_Model

from app.utils import constants as C
from app.utils import exceptions as E
from app.utils import utilities as U
from app.core import cfg


async def process_image(trxId: str, image_path: str):
    """Process each file provided during request.

    Process each file for page extractions.

    Args
    ----
        trxId: The request transaction ID. Used for logging purpose.
        image_path: Uploaded image

    Returns
    -------
        The classes for each image.
        example:

    Raises
    ------

    """
    # 1. Start Processing
    start_ts = datetime.now()
    logger.info(f"{U.set_log_prefix(trxid = trxId)} - Begin processing image -> {start_ts}")
    # 2. Get model and preprocess data
    model = G_Model["model"]
    # 3. predict response
    resp = model.predict(trxId=trxId, image_path=image_path)
    return resp
