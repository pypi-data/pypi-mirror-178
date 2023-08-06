import os


def string():
    try:
        with open("VERSION", "r", encoding="utf-8") as fh:
            version = fh.read().strip()
            if version:
                return version
    except:
        pass
    return "unknown (git checkout)"
