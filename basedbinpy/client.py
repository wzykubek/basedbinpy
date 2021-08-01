from basedbinpy.config import allowed_media_types
from collections import namedtuple
from typing import Optional, Any
from mimetypes import MimeTypes
from requests import post, get
import json


class Client:
    def __init__(self, url: str):
        self.url = url[:-1] if url[-1] == "/" else url

    def __convert_json_to_dict(self, json_bytes: bytes) -> dict:
        return json.loads(json_bytes)

    def __convert_dict_to_obj(self, name: str, dict_: dict) -> object:
        return namedtuple(name, dict_.keys())(*dict_.values())

    def get_paste(
        self,
        paste_id: str,
        file_format: str = "base64",
        plain_text_output: bool = False,
    ) -> object:
        params = {"file_format": file_format, "plain_text_output": plain_text_output}
        output = get(f"{self.url}/paste/{paste_id}", params).text
        if not plain_text_output:
            output = self.__convert_json_to_dict(output)
        else:
            output = output.decode("utf-8")
        return self.__convert_dict_to_obj("Paste", output)

    def upload_file(self, filename: str) -> object:
        mime_type = MimeTypes().guess_type(filename)[0]
        if mime_type in allowed_media_types:
            with open(filename, "rb") as file:
                response = post(f"{self.url}/upload", files={"file": (filename, file, mime_type)})
                return response.text
        else:
            print("Invalid mime type")