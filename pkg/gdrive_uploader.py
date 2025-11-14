from pathlib import Path
import os.path
import json, logging

logging.basicConfig(
    filename="log.txt", filemode="w", level=logging.DEBUG, format="%(message)s"
)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def main(file_list):
    try:
        service = auth_service()
        folder_id = folder(service)
        file_uploader(service, folder_id, file_list)
        print("upload successful!")
        return

        # logging.debug("Following Files in Drive")
        # files = test_call(service)
        # logging.debug(json.dumps(files, indent=2))

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def auth_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as fileobj:
            fileobj.write(creds.to_json())
    service = build(
        "drive", "v3", credentials=creds
    )  # returns discovery resource object
    return service


def test_call(service):
    # Call the Drive v3 API
    results = (  # returns dict
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")  # endpoint
        .execute()  # makes the actual request on http request object
    )

    items = results.get("files", [])  # filters out results
    return items


# retrieves the phorger folder
def folder(service):
    results = (  # checking for exisiting folder
        service.files()
        .list(
            q="mimeType='application/vnd.google-apps.folder'", fields="files(id, name)"
        )  # filters out folder
        .execute()
    )
    folder = results.get("files", [])
    if folder:
        for file in folder:
            if file["name"] == "phorger":
                print("phorger folder found!")
                logging.debug(f"phorger folder found under id: {file['id']}")
                return file["id"]

    print("phorger folder not found, creating...")
    file_metadata = {
        "name": "phorger",
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=file_metadata, fields="id").execute()
    logging.debug(f"Phorger folder ID: {folder.get('id')}.")
    print("...success!")
    return folder.get("id")


# gets the id of the album folder?
def album_folder(service, phorger_folder_id, album_name):
    # checking for exisiting folder
    q = f"'{phorger_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = (
        service.files()
        .list(q=q, fields="files(id, name)")  # filters out folder
        .execute()
    )
    folder = results.get("files", [])
    if folder:
        for file in folder:
            if file["name"] == album_name:
                logging.debug(f"album folder found under id: {file['id']}")
                album_id = file["id"]
                return album_id

    # if album folder not found #

    file_metadata = {
        "name": album_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [phorger_folder_id],
    }
    folder = service.files().create(body=file_metadata, fields="id").execute()
    logging.debug(f"album folder created, id: {folder.get('id')}.")

    album_id = folder.get("id")
    return album_id


def file_uploader(service, folder_id, file_list):
    counter = 0
    phorger_folder_id = folder_id
    for path_object in file_list:
        album_id = album_folder(service, phorger_folder_id, path_object.name)
        output_file_path = path_object / "output"
        for file in output_file_path.glob(
            "*.jpg"
        ):  # uploading only jpgs found in output folder
            print(f"uploading {file}")
            logging.debug(f"output file: {file}")

            file_metadata = {"name": file.name, "parents": [album_id]}
            media = MediaFileUpload(
                str(file), mimetype="image/jpeg"
            )  # converting path object to string

            file = (
                service.files()
                .create(
                    body=file_metadata,
                    media_body=media,
                    fields="id",
                    uploadType="multipart",
                )
                .execute()
            )
            counter += 1
            logging.debug(f"File ID: {file.get('id')}")

        return file.get("id"), print(f"files uploaded: {counter}"), album_id


def link_share(service, file):
    # TODO
    pass


if __name__ == "__main__":
    pass
