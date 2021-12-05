from html import unescape


def sanitize_name(filename: str) -> str:
    return unescape(filename).replace("/", "-").replace("\\", "-").strip()


def create_cli_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Origin folder in which the tracks and\
                            csv (if any) files are")
    parser.add_argument("destination", help="Destination folder")
    parser.add_argument("--dry_run", "-d",
                        help="Perform a dry_run: print the output but does not\
                                move files aroud",
                        action="store_true")
    parser.add_argument("--move", "-m",
                        help="Move the files instead of copying them",
                        action="store_true")
    parser.add_argument("--google-music", "-g",
                        action="store_true",
                        help="Uses Google CSV files instead of mp3 tags")

    return parser.parse_args()
