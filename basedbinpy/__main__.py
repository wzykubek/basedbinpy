from basedbinpy import Client
from basedbinpy.exceptions import PasteNotFound, InvalidObjectId, InvalidMimeType
import sys
import argparse

parser = argparse.ArgumentParser(
    prog="basedbinpy",
    description="CLI for basedbin pastebin-like API service.",
    allow_abbrev=False,
)
subparsers = parser.add_subparsers(dest="method", required=True)
parser.add_argument(
    "--url", metavar="URL", type=str, help="basedbin server URL", required=True
)

parser_get = subparsers.add_parser("get", help="get paste by ID")
parser_get.add_argument(
    "--id",
    dest="paste_id",
    metavar="PASTE ID",
    type=str,
    help="paste ID",
    required=True,
)

parser_upload = subparsers.add_parser("upload", help="upload new file")
parser_upload.add_argument(
    "-f", "--filename", type=str, help="path to file", required=True
)

args = parser.parse_args()

client = Client(args.url)
method = args.method


def handle_error(message: str, code: int = 1):
    name = parser.prog + " " + args.method
    print(f"{name}: error: {message}")
    sys.exit(code)


def main():
    if method == "get":
        paste_id = args.paste_id
        try:
            paste = client.get_paste(paste_id)
            file_content = paste["file_content"]
            print(file_content)
        except PasteNotFound:
            handle_error("paste not found")
        except InvalidObjectId:
            handle_error("invalid paste ID")
    elif method == "upload":
        filename = args.filename
        try:
            status = client.upload_file(filename)
            paste_id = status["paste_id"]
            paste_url = status["paste_url"]
            print(f"Paste ID: {paste_id}\nPaste URL: {paste_url}")
        except InvalidMimeType as e:
            mime_type = str(e).split(" ")[0]
            handle_error(f"invalid mime type ({mime_type})")
        except FileNotFoundError:
            handle_error("file not found")


if __name__ == "__main__":
    main()
