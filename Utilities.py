import logging
import sys

EXAMPLE_FILE = "https://imsdb.com/scripts/Lord-of-the-Rings-Fellowship-of-the-Ring,-The.html"
# "https://imsdb.com/scripts/Matrix,-The.html"
# "https://imsdb.com/scripts/Jane-Eyre.html"
# "https://imsdb.com/scripts/Lord-of-the-Rings-Fellowship-of-the-Ring,-The.html"
#

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