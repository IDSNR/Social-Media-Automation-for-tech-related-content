from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import webbrowser

# Path to the JSON key file
SERVICE_ACCOUNT_FILE = 'new_acc.json'

# Define the scopes required by the API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Authenticate using the service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API service
service = build('drive', 'v3', credentials=credentials)

def upload():
    results = service.files().list(
        q="'1cOuGgAkuYmdby2hjYu2etxhob9G09QXA' in parents",
        pageSize=10,
        fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print('No files found in the shared folder.')
    else:
        print('Files in shared folder:')
        for item in items:
            service.files().delete(fileId=item["id"]).execute()
            print(f'File Name: {item["name"]}, File ID: {item["id"]}')

    # File to be uploaded
    file_metadata = {'name': 'Video.mp4', 'parents': ['1cOuGgAkuYmdby2hjYu2etxhob9G09QXA']}
    media = MediaFileUpload('Videos/Done/Video_nosubs.mp4', mimetype='text/plain')

    # Upload the file
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

if __name__ == '__main__':
    upload()
