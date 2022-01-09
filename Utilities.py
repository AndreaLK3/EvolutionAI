import logging
import sys
import re

RESULTS_DATABASE = "Results.db"
SCRIPT_URLS_FILE = "script_URLs.pickle"


EXAMPLE_FILE = "https://imsdb.com/scripts/Jane-Eyre.html"
# "https://imsdb.com/scripts/Matrix,-The.html"
# "https://imsdb.com/scripts/Lord-of-the-Rings-Fellowship-of-the-Ring,-The.html"


def init_logging(logfilename, loglevel=logging.INFO):
    """Invoked to write a message to a text logfile and also print it"""

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=loglevel, filename=logfilename, filemode="w",
              format='%(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    if len(logging.getLogger().handlers) < 2:
        outlog_h = logging.StreamHandler(sys.stdout)
        outlog_h.setLevel(loglevel)
        logging.getLogger().addHandler(outlog_h)


def get_movie_title_from_script_url(script_url):
    pattern = re.compile("/([^/])+html$")
    mtc = re.search(pattern, script_url)
    if mtc is None:
        logging.warning("No script at URL: " + script_url + " Moving on...")
        return None  # URL that corresponds to no movie, such as https://imsdb.com/scripts/.
    title_segment = mtc.group(0)
    title = title_segment.replace(".html", "")
    title = title[1:]  # to remove the starting /
    return title
