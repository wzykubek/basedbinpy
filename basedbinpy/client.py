from basedbinpy.config import allowed_media_types
from basedbinpy.exceptions import InvalidMimeType
from collections import namedtuple
from mimetypes import MimeTypes
from requests import post, get
import json


class Client:
    def __init__(self, url: str):
        self.url = url[:-1] if url[-1] == "/" else url

    def __convert_json_to_dict(self, json_bytes: bytes) -> dict:
        return json.loads(json_bytes)

    def __convert_dict_to_obj(self, name: str, dict_: dict) -> object:
        dict_ = self.__convert_json_to_dict(dict_)
        return namedtuple(name, dict_.keys())(*dict_.values())

    def get_paste(self, paste_id: str) -> object:
        output = get(f"{self.url}/paste/{paste_id}").text
        return self.__convert_dict_to_obj("Paste", output)

    def upload_file(self, filename: str) -> object:
        mime_type = MimeTypes().guess_type(filename)[0]
        if mime_type in allowed_media_types:
            with open(filename, "rb") as file:
                response = post(
                    f"{self.url}/upload", files={"file": (filename, file, mime_type)}
                )
                return response.text
        else:
            raise InvalidMimeType("File mime type is not accepted by server")
