#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
_INVALID_FILETYPE = "Invalid File Type, expected pdf, jpeg, jpg"
_AZURE_JOB_SUBMIT_FAILURE = "Failed to submit azure ocr job for page."
_AZURE_JOB_FAILURE = "Azure OCR job failed for page."
_CLASSIFIER_JOB_FAILURE = "Failed to classifiy page."
_OCR_ERROR = "Failed to perform OCR."
_REF_DATA_FIND_ERROR = "Item not found in refrence data store."


class OCRError(Exception):
    """IHX LRD DEfined Custom Exceptions.

    This provides a suite of custom exceptions.

    Typical usage example:

    result = exceptions._specif_Exception(parameters)
    """

    def __init__(self, trxid, fileId, filename, pageId, message=_INVALID_FILETYPE):
        """Initialises the class."""
        self.trxid = trxid
        self.fileId = fileId
        self.filename = filename
        self.pageId = pageId
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Print or string formatter."""
        return f"[{self.trxid}] [Filename/Fileid/PageId: {self.filename}/{self.fileId}/{self.pageId}] -> {self.message}"


class InvalidFileType(Exception):
    """IHX LRD DEfined Custom Exceptions.

    This provides a suite of custom exceptions.

    Typical usage example:

    result = exceptions._specif_Exception(parameters)
    """

    def __init__(self, trxid, fileId, filename, message=_INVALID_FILETYPE):
        """Initialises the class."""
        self.trxid = trxid
        self.fileId = fileId
        self.filename = filename
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Print or string formatter."""
        return f"[{self.trxid}] [Filename/Fileid: {self.filename}/{self.fileId}] -> {self.message}"


class AzureJobSubmissionFailure(Exception):
    """IHX LRD DEfined Custom Exceptions.

    This provides a suite of custom exceptions.

    Typical usage example:

    result = exceptions._specif_Exception(parameters)
    """

    def __init__(self, trxid, pageid, api_response, message=_AZURE_JOB_SUBMIT_FAILURE):
        """Initialises the class."""
        self.trxid = trxid
        self.pageid = pageid
        self.message = message
        self.api_response = api_response
        super().__init__(self.message)

    def __str__(self):
        """Print or string formatter."""
        return f"[{self.trxid}] {self.pageid} -> {self.message} => {self.api_response}"


class AzureJobFailure(Exception):
    """IHX LRD Defined Custom Exceptions.

    This provides a suite of custom exceptions.

    Typical usage example:

    result = exceptions._specif_Exception(parameters)
    """

    def __init__(
        self, trxid, fileIdx, pageid, api_response, message=_AZURE_JOB_FAILURE
    ):
        """Initialises the class."""
        self.trxid = trxid
        self.fileId = fileIdx
        self.pageid = pageid
        self.message = message
        self.api_response = api_response
        super().__init__(self.message)

    def __str__(self):
        """Print or string formatter."""
        return f"[TrxID: {self.trxid}] [File/Page: {self.fileId}/{self.pageid}] -> Msg: {self.message} => API Response: {self.api_response}"


class ModelJobFailure(Exception):
    """IHX LRD DEfined Custom Exceptions.

    This provides a suite of custom exceptions.

    Typical usage example:

    result = exceptions._specif_Exception(parameters)
    """

    def __init__(
        self, trxid, fileIdx, pageid, api_response, message=_CLASSIFIER_JOB_FAILURE
    ):
        """Initialises the class."""
        self.trxid = trxid
        self.fileId = fileIdx
        self.pageid = pageid
        self.message = message
        self.api_response = api_response
        super().__init__(self.message)

    def __str__(self):
        """Print or string formatter."""
        return f"[TrxID: {self.trxid}] [File/Page: {self.fileId}/{self.pageid}] -> Msg: {self.message} => API Response: {self.api_response}"

class ReferenceDataNotFound(Exception):
    """IHX LRD DEfined Custom Exceptions.

    This provides a suite of custom exceptions.

    Typical usage example:

    result = exceptions._specif_Exception(parameters)
    """

    def __init__(
        self, find_key, message=_REF_DATA_FIND_ERROR
    ):
        """Initialises the class."""
        self.message = message
        self.find_key = find_key
        super().__init__(self.message)

    def __str__(self):
        """Print or string formatter."""
        return f"Msg: {self.message} => Key: {self.find_key}"
