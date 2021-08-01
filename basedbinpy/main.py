from urllib.request import urlopen
from urllib.parse import urlencode
from collections import namedtuple
from typing import Optional, Any
import json


class Client:
    def __init__(self, url: str):
        self.url = url[:-1] if url[-1] == "/" else url

    def __convert_json_to_dict(self, json_bytes: bytes) -> dict:
        return json.loads(json_bytes.decode("utf-8"))

    def __convert_dict_to_obj(self, name: str, dict_: dict) -> object:
        return namedtuple(name, dict_.keys())(*dict_.values())

    def __do_get_request(self, endpoint: str, value: Any, params: Optional[dict] = None):
        request_url = f"{self.url}/{endpoint}/{value}"
        if params:
            parsed_params = urlencode(params)
            request_url += f"?{parsed_params}"
        response = urlopen(request_url).read()
        return response

    def get_paste(
        self,
        paste_id: str,
        file_format: str = "base64",
        plain_text_output: bool = False,
    ) -> object:
        params = {"file_format": file_format, "plain_text_output": plain_text_output}
        output = self.__do_get_request("paste", str(paste_id), params)
        if not plain_text_output:
            output = self.__convert_json_to_dict(output)
        else:
            output = output.decode("utf-8")
        return self.__convert_dict_to_obj("Paste", output)
