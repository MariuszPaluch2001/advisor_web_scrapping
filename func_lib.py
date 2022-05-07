from typing import IO, Dict
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json


def make_request(url: str, hdrs: Dict[str, str]) -> Request:
    return Request(url, headers=hdrs)


def get_bytes_from_page(request: Request) -> bytes:
    return urlopen(request).read()


def preparing_soup(url: str, headers: Dict[str, str], parser_type: str) -> BeautifulSoup:
    req = make_request(url, headers)
    page_code_bytes = get_bytes_from_page(req)
    soup = BeautifulSoup(page_code_bytes, parser_type)
    return soup


def read_config(file: IO[str]):
    return json.load(file)
