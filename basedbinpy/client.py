from basedbinpy.config import ALLOWED_MEDIA_TYPES
from basedbinpy.exceptions import InvalidMimeType, PasteNotFound, InvalidObjectId
from mimetypes import MimeTypes
from bson import ObjectId
from requests import post, get
from os import path
from _io import TextIOWrapper
from io import BytesIO
from typing import Optional
import json


class NamedBytesIO(BytesIO):
    def __init__(self, name: str) -> None:
        self.name = name


class Client:
    def __init__(self, url: str):
        self.url = url[:-1] if url[-1] == "/" else url

    @staticmethod
    def __json_to_dict(json_str: str) -> dict:
        return json.loads(json_str)

    @staticmethod
    def __is_ObjectId_valid(id: str) -> bool:
        return ObjectId.is_valid(id)

    @staticmethod
    def __file_exists(filename: str) -> bool:
        return path.exists(filename)

    def get_paste(self, paste_id: str) -> dict:
        if not self.__is_ObjectId_valid(paste_id):
            raise InvalidObjectId("Specified paste_id parameter is not valid ObjectId")
        output = get(f"{self.url}/paste/{paste_id}")
        if output.status_code == 404:
            raise PasteNotFound()
        else:
            return self.__json_to_dict(output.text)

    @staticmethod
    def __get_file_mime_type(filename: str) -> str:
        return MimeTypes().guess_type(filename)[0]

    def __get_file(self, filename: str) -> TextIOWrapper:
        if not self.__file_exists(filename):
            raise FileNotFoundError()
        return open(filename, "r")

    @staticmethod
    def __close_file(file_: TextIOWrapper):
        file_.close()

    def upload_file_obj(self, file_: TextIOWrapper, mime_type: Optional[str] = None) -> dict:
        file_name = file_.name
        if not mime_type:
            mime_type = self.__get_file_mime_type(file_name)
        if mime_type.split("/")[0] in ALLOWED_MEDIA_TYPES:
            response = post(
                f"{self.url}/upload", files={"file": (file_name, file_, mime_type)}
            )
            self.__close_file(file_)
            return self.__json_to_dict(response.text)
        else:
            raise InvalidMimeType(f"{mime_type} mime type is not accepted by server")

    def upload_file(self, filename: str) -> dict:
        file_ = self.__get_file(filename)
        return self.upload_file_obj(file_)

    def upload_text(self, text: str, file_name: str) -> dict:
        buffer = NamedBytesIO(file_name)
        wrapper = TextIOWrapper(buffer, encoding="cp1252", line_buffering=True)
        wrapper.write(text)
        wrapper.seek(0, 0)
        return self.upload_file_obj(wrapper, "text/plain")
