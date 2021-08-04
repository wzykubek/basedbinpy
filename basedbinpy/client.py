from basedbinpy.config import ALLOWED_MEDIA_TYPES
from basedbinpy.exceptions import InvalidMimeType, PasteNotFound, InvalidObjectId
from mimetypes import MimeTypes
from bson import ObjectId
from requests import post, get
import json


class Client:
    def __init__(self, url: str):
        self.url = url[:-1] if url[-1] == "/" else url

    @staticmethod
    def __json_to_dict(json_str: str) -> dict:
        return json.loads(json_str)

    @staticmethod
    def __is_ObjectId_valid(id: str) -> bool:
        return ObjectId.is_valid(id)

    def get_paste(self, paste_id: str) -> dict:
        if not self.__is_ObjectId_valid(paste_id):
            raise InvalidObjectId("Specified paste_id parameter is not valid ObjectId")
        output = get(f"{self.url}/paste/{paste_id}")
        if output.status_code == 404:
            raise PasteNotFound()
        else:
            return self.__json_to_dict(output.text)

    def upload_file(self, filename: str) -> dict:
        mime_type = MimeTypes().guess_type(filename)[0]
        if mime_type.split("/")[0] in ALLOWED_MEDIA_TYPES:
            with open(filename, "rb") as file:
                response = post(
                    f"{self.url}/upload", files={"file": (filename, file, mime_type)}
                )
                return self.__json_to_dict(response.text)
        else:
            raise InvalidMimeType("File mime type is not accepted by server")
