from basedbinpy.config import allowed_media_types
from basedbinpy.exceptions import InvalidMimeType, PasteNotFound
from mimetypes import MimeTypes
from requests import post, get
import json


class Client:
    def __init__(self, url: str):
        self.url = url[:-1] if url[-1] == "/" else url

    @staticmethod
    def __json_to_dict(json_str: str) -> dict:
        return json.loads(json_str)

    def get_paste(self, paste_id: str) -> dict:
        output = get(f"{self.url}/paste/{paste_id}")
        if output.status_code == 404:
            raise PasteNotFound()
        else:
            return self.__json_to_dict(output.text)

    def upload_file(self, filename: str) -> dict:
        mime_type = MimeTypes().guess_type(filename)[0]
        if mime_type in allowed_media_types:
            with open(filename, "rb") as file:
                response = post(
                    f"{self.url}/upload", files={"file": (filename, file, mime_type)}
                )
                return self.__json_to_dict(response.text)
        else:
            raise InvalidMimeType("File mime type is not accepted by server")
