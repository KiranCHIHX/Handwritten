#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
"""Local Pytesseract Implementation of the abastract class - AbstractOCRExtractor.

This class implements the pytesseract OCR, through a python API call.

  Typical usage example:
  
  ocrObj = pyTesseractOCR(cfg:OmeagaConf)
"""

import json
import os
import re
import ast
import numpy as np
import pytesseract
import time

from requests import get, post
from pytesseract import Output
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

from app.core import logger
from app.utils import exceptions as E
from app.utils import utilities as U 
from app.core.config import cfg
from app.controllers.OCR.abstract_ocr import AbstractOCRExtractor

# Local Constants

class AzureLayoutOCR(AbstractOCRExtractor):
    def __init__(self, cfg):
        """Initialises the class."""
        self.cfg = cfg
        self.client = None
        self.form_path = None
        self.text = None
        self._config()

    def _config(self) -> None:
        """Configuration Values."""
        endpoint = cfg.models.OCR.Azure_Layout.endpoint
        key = cfg.models.OCR.Azure_Layout.AZURE_KEY
        self.client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        return None
    
    def extract(
        self,
        trxId: str,
        pageIdx: str,
        fileIdx: str,
        image_path: str,
        postprocess: bool = True,
        outfilepath: str = None,
        json_response_path = None
    ):
        """Main function call to perform OCR.

        This function call is used to call the OCR functionality.

        Args
        ----
            trxId: The request transaction ID. Used for logging purpose.
            pageIdx: To keep track of the page in multiprocessign scenario.
            fileIdx: To keep track of the file in multiprocessign scenario.
            images_folder: Full path to the images folder to perform OCR.
            postprocess: Boolean value to run postprocess. Default False.
            outfilepath: Full path in case the OCR output needs to be saved.

        Returns
        -------
            The JSON response for the OCR API call.

        Raises
        ------
            AzureJobFailure: In case the OCR job failed.
            AzureJobSubmissionFailure: In case  the job could not be submitted.

        """
        try:
            ocr_start = time.time()
            self.image_name = image_path.split("/")[-1]
            self.ext = self.image_name.split(".")[-1]
            logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> Begin OCR for page {self.image_name}: {ocr_start}"
            )
            # 1. send the documents for OCR
            with open(image_path, "rb") as f:
                poller = self.client.begin_recognize_content(form=f)
            
            # 2. Poll the results
            form_pages = poller.result()
            ocr_end = time.time()
            logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> Completed OCR for page {self.image_name}: Time taken : {ocr_end - ocr_start}"
            )
            if outfilepath:
                # Writing to sample.json
                json_path = os.path.join(outfilepath, self.image_name.replace(self.ext, "json"))
                with open(json_path, "w") as outfile:
                    outfile.write(json.dumps(form_pages, indent=4))
            # postprocess the response to extract only text
            if postprocess:
                self.text = self.postprocess(trxId = trxId, fileId = fileIdx, page_no = pageIdx, extract_response = form_pages)
            else:
                self.text = form_pages
            ocr_preproc_end = time.time()
            logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> Completed OCR Preprocessing for page {self.image_name}: Time taken : {ocr_preproc_end - ocr_end}"
            )
        except Exception as e:
            raise E.OCRError(trxId, fileIdx, image_path.split("/")[-1], pageIdx, e)
        return self.text

    def postprocess(self, trxId, fileId, page_no, extract_response) -> str:
        """Extracts all text portion from OCR data.

        The post processing specific logic extracts all the text and returns it
        as a string tot he calling program.

        Args
        ----
            extract_response: The JSON Response from the OCR API call.

        Returns
        -------
            DataFrame: Azure detected tables as pandas dataframe.

        Raises
        ------
            None

        """
        # 1. Get the content for all pages within the document.
        #   - code is written for multiple pages to be generic but in the cbd flow
        #     only one page is sent at a time.
        start_preproc = time.time()
        logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileId}/{page_no} -> Start OCR Preprocessing : {start_preproc}"
            )
        logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileId}/{page_no} -> Completed OCR Preprocessing : {time.time() - start_preproc}"
            )
        return None

class AzureInvoiceOCR(AbstractOCRExtractor):
    def __init__(self, cfg):
        """Initialises the class."""
        self.cfg = cfg
        self.client = None
        self.form_path = None
        self.text = None
        self._config()

    def _config(self) -> None:
        """Configuration Values."""
        self.endpoint = cfg.models.OCR.Azure_Layout.endpoint + cfg.models.OCR.Azure_Invoice.endpoint
        self.key = cfg.models.OCR.Azure_Invoice.AZURE_KEY
        self.headers = {
                # Request headers
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': self.key,
            }

        self.params = {
            "includeTextDetails": True
        }
        return True
    
    def _azure_request(self, filepath):
        """Responsible for making the actual request to Azure"""
        with open(filepath, "rb") as f:
            data_bytes = f.read()
        try:
            resp = post(url = self.endpoint, data = data_bytes, headers = self.headers, params = self.params)
            if resp.status_code != 202:
                return None
            get_url = resp.headers["operation-location"]
        except Exception as e:
            raise E.OCRError(self.trxId, self.fileIdx, self.image_path.split("/")[-1], self.pageIdx, e)
        return get_url

    def _pole_azure_request(self, req_url):
        """Poles the Azure endpoint for the job status"""
        key = os.environ['AZURE_KEY']
        n_tries = cfg.models.OCR.Azure_Invoice.pole_tries
        wait_sec = cfg.models.OCR.Azure_Invoice.pole_wait_secs
        current_tries = 0
        # 1. Try multiple times until we get response - pole
        for i in range(n_tries):
            try:
                resp = get(url = req_url, headers = {"Ocp-Apim-Subscription-Key": key})
                resp_json = json.loads(resp.text)
                if resp.status_code != 200:
                    return None
                status = resp_json["status"]
                if status == "succeeded":
                    return resp_json
                if status == "failed":
                    return None
                time.sleep(wait_sec)
            except Exception as e:
                raise Exception(e)
        return None
    
    def extract(
        self,
        trxId: str,
        pageIdx: str,
        fileIdx: str,
        image_path: str,
        postprocess: bool = True,
        outfilepath: str = None,
        json_response_path = None
    ):
        """Main function call to perform OCR.

        This function call is used to call the OCR functionality.

        Args
        ----
            trxId: The request transaction ID. Used for logging purpose.
            pageIdx: To keep track of the page in multiprocessign scenario.
            fileIdx: To keep track of the file in multiprocessign scenario.
            images_folder: Full path to the images folder to perform OCR.
            postprocess: Boolean value to run postprocess. Default False.
            outfilepath: Full path in case the OCR output needs to be saved.

        Returns
        -------
            The JSON response for the OCR API call.

        Raises
        ------
            AzureJobFailure: In case the OCR job failed.
            AzureJobSubmissionFailure: In case  the job could not be submitted.

        """
        self.trxId = trxId
        self.fileIdx = fileIdx
        self.pageIdx = pageIdx
        self.image_path = image_path
        try:
            ocr_start = time.time()
            image_name = image_path.split("/")[-1]
            logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> Begin OCR for page {image_name}: {ocr_start}"
            )
            # 1. send the documents for OCR
            pole_url = self._azure_request(filepath = image_path)
            logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> OCR pole URL {pole_url}: {ocr_start}"
            )
            if pole_url is None:
                raise  E.OCRError(trxId, fileIdx, image_path.split("/")[-1], pageIdx, "Pole URL is None.")
            # 2. Poll the results
            invoice_json = self._pole_azure_request(pole_url)
            ocr_end = time.time()
            logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> Completed OCR for page {image_name}: Time taken : {ocr_end - ocr_start}"
            )
            # postprocess the response to extract only text
            if postprocess:
                self.result = self.postprocess(trxId = trxId, fileId = fileIdx, page_no = pageIdx, extract_response = invoice_json)
                # save output of tables
                tables, parent_dfs = self.result
            else:
                self.result = invoice_json
            ocr_preproc_end = time.time()
            logger.info(
                f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> Completed OCR Preprocessing for page {image_name}: Time taken : {ocr_preproc_end - ocr_end}"
            )
            if outfilepath:
                # Writing to sample.json
                ext = image_name.split(".")[-1]
                json_path = os.path.join(outfilepath, image_name.replace(ext, "json"))
                logger.info(
                    f"{U.prepend_msg(trxId)} - File/Page: {fileIdx}/{pageIdx} -> Writing page to path {json_path}"
                )
                with open(json_path, "w") as outfile:
                    outfile.write(json.dumps(invoice_json, indent=4))
                table_path = json_path.replace(".json", "_ocr_final.csv")
                tables.to_csv(table_path, index=False)
        except Exception as e:
            raise E.OCRError(trxId, fileIdx, image_path.split("/")[-1], pageIdx, e)
        return self.result
    
    def postprocess(self, trxId, fileId, page_no, extract_response, outfilepath=None) -> str:
        """Extracts all text portion from OCR data.

        The post processing specific logic extracts all the text and returns it
        as a string tot he calling program.

        Args
        ----
            extract_response: The JSON Response from the OCR API call.

        Returns
        -------
            DataFrame: Azure detected tables as pandas dataframe.

        Raises
        ------
            None

        """
        # 1. Get the content for all pages within the document.
        #   - code is written for multiple pages to be generic but in the cbd flow
        #     only one page is sent at a time.
        start_preproc = time.time()
        logger.info(
            f"{U.prepend_msg(trxId)} - File/Page: {fileId}/{page_no} -> Start OCR Preprocessing : {start_preproc}"
        )
        logger.info(
            f"{U.prepend_msg(trxId)} - File/Page: {fileId}/{page_no} -> Completed OCR Preprocessing : {time.time() - start_preproc}"
        )
        return None

