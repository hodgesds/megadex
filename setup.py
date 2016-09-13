from setuptools import setup, find_packages

setup(
    name             = "megadex",
    description      = "Mega Indexer",
    url              = "https://github.com/hodgesds/megadex",
    version          = "0.0.1",
    author           = "Daniel Hodges",
    author_email     = "hodges.daniel.scott@gmail.com",
    scripts          = [ "bin/megadex" ],
    install_requires = [
                        "elasticsearch",
                        "exifread",
                        "openpyxl",
                        "pyshp",
                        "python-docx",
                        "python-pptx",
                        "watchdog",
                        "xlrd",
                        "xmltodict",
                       ],
    test_suite       = "",
    tests_require    = [ "tox", "nose" ],
    packages         = find_packages(
        where        = ".",
        exclude      = ("tests*", "bin*", "example*"),
    ),
)
