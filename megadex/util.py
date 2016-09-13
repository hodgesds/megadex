import os


def get_ext(filename):
    return os.path.splitext(filename)[-1].lower()
