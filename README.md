# basedbinpy

Simple python library for [basedbin](https://github.com/samedamci/basedbinpy) pastebin-like service.

## Installing

```shell
$ python3 -m pip install basedbinpy
```

## Usage demo

```python
from basedbinpy import Client

client = Client(BASEDBIN_URL)  # example: "http://localhost:8080"

paste = client.get_paste(PASTE_ID)

print(paste["file_content"])
```