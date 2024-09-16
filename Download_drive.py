from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Path to the JSON key file
SERVICE_ACCOUNT_FILE = 'new_acc.json'

# Define the scopes required by the API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Authenticate using the service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API service
service = build('drive', 'v3', credentials=credentials)

def main():
    results = service.files().list(
        q="'1cOuGgAkuYmdby2hjYu2etxhob9G09QXA' in parents",
        pageSize=10,
        fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])

    file_path = "Videos/Done/Video.mp4"

    if not items:
        print('No files found in the shared folder.')
    else:
        print('Files in shared folder:')
        for item in items:
            print(f"File name: {item["name"]}, file id: {item["id"]}")
            if item["name"] == "output.mp4":
                request = service.files().get_media(fileId=item["id"])

                # Create a file-like object to receive the file contents
                fh = io.FileIO(file_path, 'wb')

                # Download the file
                downloader = MediaIoBaseDownload(fh, request)

                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}%.")
                fh.close()
                print(f'File downloaded to {file_path}')
            service.files().delete(fileId=item["id"]).execute()

if __name__ == '__main__':
    main()


