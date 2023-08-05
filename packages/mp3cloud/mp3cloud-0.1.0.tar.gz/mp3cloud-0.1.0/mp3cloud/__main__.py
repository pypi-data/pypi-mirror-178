import argparse
import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from mp3cloud.utils import parse_args


def valid_q(arg):
    if len(arg) < 2:
        raise argparse.ArgumentTypeError("should be at least 2 characters")
    return arg


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="FreeMp3Cloud.com music downloader")
    parser.add_argument(
        "query",
        type=valid_q,
        help="The query to search (a combination of the song name and artists)",
    )
    parser.add_argument(
        "--download",
        help="Use this flag if you want the song to be downloaded (True by default)",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--no-download",
        help="Use this flag if you DO NOT want the song to be downloaded",
        action="store_false",
        dest="download",
    )
    parser.add_argument(
        "-s",
        "--save-urls",
        help="Use this flag if you want to save a .txt file containing all the found URLs of the songs",
        action="store_true",
    )

    args = parser.parse_args()
    parse_args(args)
