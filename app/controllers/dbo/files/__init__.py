#noqa
import os


_files_directory = os.path.join(os.getcwd(), "app/controllers/dbo/files")

def filedata_list(filepath):
    data = []
    file =  open(filepath, "r")
    data = list(file)
    return data

