import re

HTML_COMMENT_REGEX = re.compile(r"<!--(.*?)-->", re.DOTALL)
EMAIL_REGEX = re.compile(r"\S+@\S+\.\S+")
HTTP_URL_REGEX = re.compile(r"https?://")
