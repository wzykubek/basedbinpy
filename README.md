# basedbinpy

Simple python library and CLI for [basedbin](https://github.com/samedamci/basedbinpy) pastebin-like service.

## Installing
```shell
$ python3 -m pip install basedbinpy
```

## Library demo
```python
from basedbinpy import Client

client = Client(BASEDBIN_URL)  # example: "http://localhost:8080"

paste = client.get_paste(PASTE_ID)

print(paste["file_content"])
```

## CLI upload file demo
```bash
$ python3 -m basedbinpy --url http://localhost:8080 upload -f note.txt
```