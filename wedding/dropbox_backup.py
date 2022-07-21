import dropbox
import io
from datetime import date

from kumpfeiffer.settings import DROPBOX


def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox(DROPBOX["auth_token"])
    except Exception as e:
        print("Error connecting to Dropbox with access token: " + str(e))
        raise e
    return dbx


def dropbox_upload_file(content, dropbox_file_path):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        content (bytes): The content of the new file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file(b"{'hello': 'world'}", "/stuff/test.json")

    Returns:
        meta: The Dropbox file metadata.
    """

    try:
        dbx = dropbox_connect()

        temp_file = io.BytesIO(content)

        meta = dbx.files_upload(
            temp_file.read(),
            dropbox_file_path,
            mode=dropbox.files.WriteMode("overwrite"),
        )

        return meta
    except Exception as e:
        print("Error uploading file to Dropbox: " + str(e))
        raise e


def backup_files(files_data: list[dict]):

    folder_name = f"{date.today().isoformat()}-backup"

    for file in files_data:
        dropbox_path = f"/{folder_name}/{file['name']}"
        meta = dropbox_upload_file(file["data"], dropbox_path)
        print(f"Uploaded: {meta.name}")
