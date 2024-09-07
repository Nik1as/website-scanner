# Website scanner

A fast and powerful website scanner for CTFs.

## Modules

- basic information (title, generator, redirects)
- crawler (directories, forms, emails, comments)
- robots.txt
- favicon fingerprint
- interesting headers
- directory enumeration
- technology identification
- scan for vulnerabilities (SQL-Injection, XSS, SSTI, LFI)

## Usage

```
usage: main.py [-h] -u URL -o OUTPUT [-c COOKIE] [-t TIMEOUT] [-i [IGNORE ...]] [--user-agent USER_AGENT] [--depth DEPTH] [--vulns] [--lfi-depth LFI_DEPTH]

Scan a website

options:
  -h, --help                              show this help message and exit
  -u URL, --url URL                       URL to scan
  -o OUTPUT, --output OUTPUT              Output json file
  -c COOKIE, --cookie COOKIE              Cookie
  -t TIMEOUT, --timeout TIMEOUT           Timeout
  -i [IGNORE ...], --ignore [IGNORE ...]  Directories to ignore e.g. /logout
  --user-agent USER_AGENT                 User Agent
  --depth DEPTH                           Maximum crawler depth
  
  --vulns                                 Scan for vulnerabilities
  --lfi-depth LFI_DEPTH                   Maximum lfi depth

```
