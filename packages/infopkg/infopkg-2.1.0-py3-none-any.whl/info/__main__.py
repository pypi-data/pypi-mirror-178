# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2022-present Artic

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from sys import (
    path,
    argv
)
from os import getcwd

from requests import (
    get,
    Response,
    exceptions
)

from .Constants import (
    __author__,
    __description__,
    __version__
)

class colour:
    VIOLET: str = '\033[95m'
    CYAN: str = '\033[96m'
    DARK_CYAN: str = '\033[36m'
    BLUE: str = '\033[94m'
    GREEN: str = '\033[92m'
    YELLOW: str = '\033[93m'
    RED: str = '\033[91m'
    WHITE: str = '\033[37m'
    BLACK: str = '\033[30m'
    GRAY: str = '\033[38;2;88;88;88m'
    MAGENTA: str = '\033[35m'
    BOLD: str = '\033[1m'
    DIM: str = '\033[2m'
    NORMAL: str = '\033[22m'
    UNDERLINED: str = '\033[4m'
    STOP: str = '\033[0m'

if path[0] in ("", getcwd()):
    path.pop(0)

def __get__(name: str = None) -> None:
    try:
        if name is None:
            raise SyntaxError("Missing the \"name\" argument.")
        try:
            response: Response = get(
                url=f"https://pypi.org/pypi/{name}/json",
                timeout=10.0
            )
        except ConnectionError:
            print(f"{colour.RED}The module cannot work without an Internet connection.{colour.STOP}")
        if response.status_code == 404:
            print(f"{colour.RED}This module doesn't exist.{colour.STOP}")
            return
        try:
            downloads: str = "{:,}".format(get(
                url=f"https://pypistats.org/api/packages/{name.replace('.', '-').lower()}/recent",
                timeout=2.0
            ).json()["data"]["last_month"])
        except TypeError:
            downloads: str = "Unable to get downloads"
        except exceptions.Timeout:
            downloads: str = "Unable to get downloads"
        json: dict = response.json()
        info: dict = json["info"]

        try:
            _requires: str = f"{colour.GRAY}\n- {colour.STOP}".join([i.split(" ")[0] for i in info["requires_dist"]])
        except TypeError:
            _requires: str = "No requires provided."
        try:
            _urls: str = f"{colour.GRAY}\n- {colour.STOP}".join([f"{colour.BOLD}{i}{colour.STOP}: {colour.DARK_CYAN}{info['project_urls'][i]}{colour.STOP}" for i in list(info["project_urls"])])
        except TypeError:
            _urls: str = "Unable to get the urls"
        _versions: str = f"{colour.GRAY}\n- {colour.STOP}".join([i for i in list(json["releases"])])

        print(f"""{info["name"]} {colour.GREEN}{info["version"]} {colour.GRAY}({colour.DARK_CYAN}https://pypi.org/project/{info["name"]}/{colour.STOP}{colour.GRAY}){colour.STOP}
{colour.GRAY}by{colour.STOP} {info["author"] or (info["maintainer"] or "nobody")} {colour.GRAY}({info["author_email"] or (info["maintainer_email"] or "no email")})

maintained by{colour.STOP} {info["maintainer"] or (info["author"] or "nobody")} {colour.GRAY}({info["author_email"] or (info["maintainer_email"] or (info["author_email"] or "no email"))})

description: {colour.STOP}{info["summary"]}{colour.GRAY}
downloads last month: {colour.STOP}{downloads}{colour.GRAY}
license: {colour.STOP}{info["license"] or "no license"}{colour.GRAY}

Requires:
- {colour.STOP}{_requires}{colour.GRAY}

URLs:
- {colour.STOP}{_urls}{colour.GRAY}

Versions:
- {colour.STOP}{_versions}{colour.STOP}
""")
    except Exception as e:
        print(f"{colour.RED}Error when searching this module:{colour.STOP} {e.__class__.__name__}: {e}")
    return

try:
    __get__(argv[1])
except IndexError:
    print(f"""{colour.GRAY}python -m info <YOUR PACKAGE NAME>

    author: {colour.STOP}{__author__}{colour.GRAY}
    version: {colour.STOP}{__version__}{colour.GRAY}
    description: {colour.STOP}{__description__}
""")
