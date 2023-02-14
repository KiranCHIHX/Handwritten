# noqa
import os
from app.utils.datastore import downloadDirectoryFromS3
from dotenv import load_dotenv

os.makedirs("logs", exist_ok=True)
load_dotenv()
print(
    f"Environment Variables [{os.getenv('MODE')}]: {os.getenv('APP_ACRONYM')}/{os.getenv('CFG_KEY')}/{os.getenv('CFG_SECRET')}"
)
downloadDirectoryFromS3(bucketName="ihx-" + os.getenv("APP_ACRONYM").lower(), remoteDirectoryName="conf")
downloadDirectoryFromS3(
    bucketName="ihx-" + os.getenv("APP_ACRONYM").lower(), remoteDirectoryName="models"
)  # localDirectoryRoot
downloadDirectoryFromS3(
    bucketName="ihx-" + os.getenv("APP_ACRONYM").lower(),
    remoteDirectoryName="files",
    localDirectoryRoot="app/controllers/dbo",
)
print("^^^^^^^ Download Config + Model ^^^^^^^^^^^^")
