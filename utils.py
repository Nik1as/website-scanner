import os
import traceback
from importlib import util
from urllib.parse import parse_qs, urlparse, ParseResult, urlencode

import bs4


def print_json_tree(data, indent=""):
    if isinstance(data, dict):
        for i, (key, value) in enumerate(data.items()):
            prefix = "└─ " if i == len(data) - 1 else "├─ "
            print(indent + prefix + f"{key}", end="")
            if isinstance(value, (dict, list)):
                print()
                print_json_tree(value, indent + ("   " if i == len(data) - 1 else "│  "))
            else:
                print(f": {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            prefix = "└─ " if i == len(data) - 1 else "├─ "
            print(indent + prefix + str(item))
    else:
        print(indent + str(data))


def get_req_kwargs(args):
    kwargs = dict()
    if args.proxy is not None:
        kwargs["proxy"] = args.proxy
    return kwargs


def unique_not_none(seq):
    results = set(seq)
    if None in results:
        results.remove(None)
    return list(results)


def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_modules(path):
    dirpath = os.path.dirname(path)

    for fname in os.listdir(dirpath):
        if not fname.startswith(".") and \
                not fname.startswith("__") and fname.endswith(".py"):
            try:
                load_module(os.path.join(dirpath, fname))
            except:
                traceback.print_exc()


def get_forms(html: str):
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup.findAll("form")


def parse_form(form: bs4.element.Tag):
    method = form.get("method", "get")
    action = form.get("action", "")
    args = dict()
    for input_tag in form.findAll("input"):
        name = input_tag.get("name", None)
        if name is None:
            continue
        value = input_tag.get("value", "")
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
