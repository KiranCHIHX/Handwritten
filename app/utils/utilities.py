#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
import os
import boto3
import botocore
import glob
import json

from datetime import datetime, timezone

def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)

def read_image_bin(img_path):
    """Reads an image and converts to binary format."""
    with open(img_path, "rb") as file:
        file_data = file.read()
    return file_data

def prepend_msg(txn_id: str):
    """Formats a string for logger."""
    return f"[TRX-Id:{txn_id}]"

def set_log_prefix(**kwargs):
    msg = ""
    for key, value in kwargs.items():
        msg = msg + f"[{key}: {value}]"
    return msg

def downloadDirectoryFromS3_V1(bucketName:str, remoteDirectoryName:str = "conf", localDirectoryRoot="app"):
    session = boto3.Session(
        aws_access_key_id = os.environ["CFG_KEY"],
        aws_secret_access_key =  os.environ["CFG_SECRET"],
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucketName) 
    print("=======Current Working Directory:",os.getcwd())
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        print("###### obj:", obj.key)
        dir_name = os.path.join(localDirectoryRoot, os.path.dirname(obj.key))
        os.makedirs(dir_name, exist_ok=True)
        bucket.download_file(obj.key, os.path.join(localDirectoryRoot, obj.key))
    return True

def downloadDirectoryFromS3(bucketName:str, remoteDirectoryName:str = "conf", localDirectoryRoot:str = "app"):
    session = boto3.Session(
        aws_access_key_id = os.getenv("CFG_KEY"),
        aws_secret_access_key =  os.getenv("CFG_SECRET"),
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucketName) 
    print("=======Directory:", remoteDirectoryName)
    print("Local directory", f"{os.getcwd()}/{localDirectoryRoot}/{remoteDirectoryName}")
    print("Local directry present:", os.path.isdir(f"{os.getcwd()}/{localDirectoryRoot}/{remoteDirectoryName}"))
    # Check for current version
    if os.path.isdir(f"{os.getcwd()}/{localDirectoryRoot}/{remoteDirectoryName}"):
        files = glob.glob(f"{os.getcwd()}/{localDirectoryRoot}/{remoteDirectoryName}/*.ver")
        print(f"---->Local version file [{len(files)}]:", files)
        if len(files) == 1:
            # get the current local version and check if S3 is matching
            print("---->Local version:", files[0].split("/")[-1])
            local_version = files[0].split("/")[-1]
            try:
                s3.Object(bucketName, f"{remoteDirectoryName}/{local_version}").load()
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print(f"---->Remote version Different From Local - Refresh required")
                    # The object does not exist hence assume new version.
                    # delete the local version file and let the new version take its place
                    os.remove(files[0])
                    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
                        print("###### obj:", obj.key)
                        dir_name = os.path.join(localDirectoryRoot, os.path.dirname(obj.key))
                        os.makedirs(dir_name, exist_ok=True)
                        bucket.download_file(obj.key, os.path.join(localDirectoryRoot, obj.key))
                else:
                    # Something else has gone wrong.
                    raise Exception(f"{remoteDirectoryName} Loading error...")
            # the version already is uptodate do nothing
            print(f"----->No new {remoteDirectoryName} update.")
        elif len(files) > 1:
            raise Exception(f"{remoteDirectoryName} corruption. More than 1 version file found...")
        else:
            print(f"---->New setup - Download required")
            for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
                print("###### obj:", obj.key)
                dir_name = os.path.join(localDirectoryRoot, os.path.dirname(obj.key))
                os.makedirs(dir_name, exist_ok=True)
                bucket.download_file(obj.key, os.path.join(localDirectoryRoot, obj.key))
    else:
        print(f"---->New setup no local folder - Download required")
        for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
            print("###### obj:", obj.key)
            dir_name = os.path.join(localDirectoryRoot, os.path.dirname(obj.key))
            os.makedirs(dir_name, exist_ok=True)
            bucket.download_file(obj.key, os.path.join(localDirectoryRoot, obj.key))
    return True