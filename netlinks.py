#! /usr/bin/env python3

import os
import ssl
import sys
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

from pathlib import Path

IGNORE_DIRS = {".git", ".tox", "build", "dist", "eggs", "venv", "__pycache__"}


def find_netlinks() -> list[Path]:
    netlinks: list[Path] = []
    for dir, _, files in os.walk("."):
        if dir in IGNORE_DIRS:
            print(f"Skipping directory: {dir}")
            continue
        netlinks += (Path(dir) / Path(f) for f in files if f.endswith(".netlink"))
    return netlinks


def parse_scheme(netlink: Path) -> str | None:
    """
    Parses the protocol scheme from a .netlink file, such as 'http', 'https', 'ftp', 'git', etc.
    """
    if not netlink.is_symlink():
        print(f"{netlink} is not a symlink.")
        return ""
    target = str(netlink.readlink())
    scheme = target.split(":", 1)[0] if ":" in target else None
    return scheme


def test(file: Path, contents: str) -> bool:
    """
    Example test function to demonstrate how to use the parse_scheme function.
    This is not part of the main functionality and can be removed or modified as needed.
    """
    with open(Path("test") / file, "r") as f:
        expected = f.read()
    return contents == expected


def get_https_content(netlink: Path) -> str | None:
    """
    Retrieves the contents of an HTTPS link.
    This is a placeholder function and should be implemented according to your needs.
    """
    try:
        url = str(os.readlink(netlink))
        print(f"Retrieving content from {url}")
        with urllib.request.urlopen(
            url,
            context=ctx,
        ) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"Error retrieving {netlink}: {e}", file=sys.stderr)
        return None


def get_contents(netlink: Path, scheme: str) -> str | None:
    """
    Retrieves the contents of the target file based on the scheme.
    This is a placeholder function and should be implemented according to your needs.
    """
    if scheme == "http":
        # TODO: Placeholder for HTTP content retrieval
        return f"Contents of {netlink} with scheme {scheme}"
    elif scheme == "https":
        return get_https_content(netlink)
    elif scheme == "ftp":
        # TODO:  Placeholder for FTP content retrieval
        return f"Contents of {netlink} with scheme {scheme}"
    elif scheme == "git":
        # TODO: Placeholder for Git content retrieval
        return f"Contents of {netlink} with scheme {scheme}"
    else:
        return ""


def main():
    netlinks = find_netlinks()
    if not netlinks:
        print("No .netlink files found.")
    else:
        for netlink in netlinks:
            scheme = parse_scheme(netlink)
            contents = ""
            if scheme:
                contents = get_contents(netlink, scheme)
            else:
                print(
                    f"{netlink}: No scheme found or not a valid link.", file=sys.stderr
                )
            assert test(netlink.stem, contents)
            assert not test(netlink.stem, contents + "\n")
            with open(netlink.parent / netlink.stem, "w") as f:
                f.write(contents)


if __name__ == "__main__":
    main()
