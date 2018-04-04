import os
import sys
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload
import httplib2
import io
from googleapiclient import discovery
import ConfigParser

SCOPES = 'https://www.googleapis.com/auth/drive'

APPLICATION_NAME = 'Master KPI'



def get_credentials(clientSecretKeyPath):

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(clientSecretKeyPath, SCOPES)
        flow.user_agent = APPLICATION_NAME
        import argparse
        flags = argparse.Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR',noauth_local_webserver=True)
        credentials = tools.run_flow(flow, store, flags)
    return credentials



def downloadFromGdrive(clientSecretKeyPath,spreadSheetId,fileName,filePath,mimeType):

    clientSecretKeyPath = clientSecretKeyPath
    credentials = get_credentials(clientSecretKeyPath)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    file_id = spreadSheetId

    request = service.files().export_media(fileId=file_id,mimeType=mimeType)

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    response = request.execute()
    with open(os.path.join(filePath, fileName), "wb") as wer:
        wer.write(response)

if __name__ == '__main__':

    config_file = sys.argv[1]
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    clientSecretKeyPath = config.get("fileDownloadFromDrive", "clientsecretkeypath")
    spreadSheetId = config.get("fileDownloadFromDrive","spreadsheetid")
    fileName = config.get("fileDownloadFromDrive","filename")
    filePath = config.get("fileDownloadFromDrive","filepath")
    mimeType = config.get("fileDownloadFromDrive", "mimetype")


    downloadFromGdrive(clientSecretKeyPath,spreadSheetId,fileName,filePath,mimeType)
