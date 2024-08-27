from urllib.parse import parse_qs, urlparse, ParseResult, urlencode

import bs4
from bs4 import BeautifulSoup


def get_forms(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.findAll("form")


def parse_form(form: bs4.element.Tag):
    method = form.get("method", "get")
    action = form.get("action", "/")
    args = dict()
    for input_tag in form.findAll("input"):
        name = input_tag.get("name", None)
        if name is None:
            continue
        value = input_tag.get("value", None)
        args[name] = value
    return method, action, args


def change_url_param_value(url: str, param: str, new_value: str):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params[param][0] = new_value
    return ParseResult(scheme=parsed.scheme, netloc=parsed.hostname, path=parsed.path, params=parsed.params, query=urlencode(params),
                       fragment=parsed.fragment).geturl()


def url_parameters(url: str):
    parsed = urlparse(url)
    return list(parse_qs(parsed.query).keys())
