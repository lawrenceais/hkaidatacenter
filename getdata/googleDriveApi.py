from __future__ import print_function
import pickle
import os.path
import os
import re
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from tabulate import tabulate
import requests
from tqdm import tqdm
import datetime

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.metadata']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)

def list_files(items):
    """given items returned by Google Drive API, prints them in a tabular way"""
    if not items:
        # empty drive
        print('No files found.')
    else:
        rows = []
        for item in items:
            # get the File ID
            id = item["id"]
            # get the name of file
            name = item["name"]
            try:
                # parent directory ID
                parents = item["parents"]
            except:
                # has no parrents
                parents = "N/A"
            try:
                # get the size in nice bytes format (KB, MB, etc.)
                size = get_size_format(int(item["size"]))
            except:
                # not a file, may be a folder
                size = "N/A"
            # get the Google Drive type of file
            mime_type = item["mimeType"]
            # get last modified date time
            modified_time = item["modifiedTime"]
            # append everything to the list
            rows.append((name, size, mime_type))
        print("Files:")
        # convert to a human readable table
        #table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
        table = tabulate(rows, headers=["Name", "Size", "Type"])
        # print the table
        print(table)
        
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
        

def upload_files():
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {
        "name": "TestFolder",
        "mimeType": "application/vnd.google-apps.folder"
    }
    # create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    # get the folder id
    folder_id = file.get("id")
    print("Folder ID:", folder_id)
    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": "aa4.txt",
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload("aa4.txt", resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File created, id:", file.get("id"))
    
def search(service, query):
    # search for the file
    result = ["result:"]
    page_token = None
    while True:
        response = service.files().list(q=query,
                                        spaces="drive",
                                        fields="nextPageToken, files(id, name, mimeType)",
                                        pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            result.append((file["id"], file["name"], file["mimeType"]))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None
    
    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        # get the file size from Content-length response header
        file_size = int(response.headers.get("Content-Length", 0))
        # extract Content disposition from response headers
        content_disposition = response.headers.get("content-disposition")
        # parse filename
        filename = re.findall("filename=\"(.+)\"", content_disposition)[0]
        print("[+] File size:", file_size)
        print("[+] File name:", filename)
        progress = tqdm(response.iter_content(CHUNK_SIZE), f"Downloading {filename}", total=file_size, unit="Byte", unit_scale=True, unit_divisor=1024)
        with open(destination, "wb") as f:
            for chunk in progress:
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # update the progress bar
                    progress.update(len(chunk))
        progress.close()
        
    # base URL for download
    #URL = "https://docs.google.com/uc?export=download"
    URL = "https://drive.google.com/drive/my-drive"
    # init a HTTP session
    session = requests.Session()
    # make a request
    response = session.get(URL, params = {'id': id}, stream=True)
    print("[+] Downloading", response.url)
    # get confirmation token
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm':token}
        response = session.get(URL, params=params, stream=True)
    # download to disk
    save_response_content(response, destination)  

def download():
    service = get_gdrive_service()
    # the name of the file you want to download from Google Drive 
    filename = "bbc.zip"
    # search for the file by name
    search_result = search(service, query=f"name='{filename}'")
    # get the GDrive ID of the file
    file_id = search_result[0][0]
    print(filename)
    print(file_id)
    # make it shareable
    service.permissions().create(body={"role": "reader", "type": "anyone"}, fileId=file_id).execute()
    # download file
    download_file_from_google_drive(file_id, filename)
    
def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 5 files the user has access to.
    """
    service = get_gdrive_service()
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
    # get the results
    items = results.get('files', [])
    # list all 20 files & folders
    list_files(items)

def main_search():
    # filter to text files
    #filetype = "text/plain"
    filetype = "text/html"
    # authenticate Google Drive API
    service = get_gdrive_service()
    # search for files that has type of text/plain
    search_result = search(service, query=f"mimeType='{filetype}'")
    # convert to table to print well
    table = tabulate(search_result, headers=["ID", "Name", "Type"])
    print(table)
    
def main_search_upload(foldername, filename):
    result=False
    filetype = "text/html"
    service = get_gdrive_service()
    
    # search for the file by name, [0] just store an "dummy", 
    search_result = search(service, query=f"name='{foldername}'")
    #print(len(search_result))
    
    if (len(search_result) > 1):
        # get the GDrive ID of the file
        folder_id = search_result[1][0]
        #print(foldername)
        #print(folder_id)
        
        # search for the file by name, [0] just store an "dummy", 
        search_result = search(service, query=f"name='{filename}'")
        if (len(search_result) > 1):
            print("File exist")
        else:        
            # upload a file 
            # first, define file metadata, such as the name and the parent folder ID
            file_metadata = {
                "name": filename,
                "parents": [folder_id]
                }
            localpathfilename = foldername+"/"+filename
            # upload
            try:
                media = MediaFileUpload(localpathfilename, resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print("File created, id:", file.get("id"))
                result = True  
            except:
                result = False
    else:
        print("Folder not found")
        result= False
        
            
    return result
   
def uploadStockFiles(foldername, sYear, sMonth):
    now = datetime.datetime.now()
    endDay = 32
    if (sYear == now.year):
        if (sMonth == now.month):
            endDay = now.day + 1
    for dd in range(1,endDay):
        datafilename = "d" + str(sYear-2000) + str(sMonth).zfill(2) + str(dd).zfill(2) + "e.htm"
        print(datafilename)
        main_search_upload(foldername, datafilename)
    
    
if __name__ == '__main__':
   #main()
   #main_search()
   #upload_files()
   #download()
   #main_search_upload("d200901e.htm")
   main_search_upload("dailyQuotations","d201001e.htm")
   #list_files()
   """
   for mm in range (1,13):
       uploadStockFiles("dailyQuotations",2020,mm)
   """
   