#!/usr/bin/env python3
"""Entrypoint for news-image-20261120 (Python 3.13, standard library only).

Copies the repository's entry.png to the output directory named by
MAKEFUN_OUTPUT_DIR (default /output). Deterministic: the same bytes
in, the same bytes out.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
