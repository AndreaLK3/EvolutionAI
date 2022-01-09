import string
import urllib
import requests
from bs4 import BeautifulSoup


EXAMPLE_FILE = "https://imsdb.com/scripts/Lord-of-the-Rings-Fellowship-of-the-Ring,-The.html"
# https://imsdb.com/scripts/Matrix,-The.html" # https://imsdb.com/scripts/Jane-Eyre.html"

def get_bold_segments(script_url=EXAMPLE_FILE):
    """Get all the bold elements <b> in the script page, that include the names of the characters when they speak"""
    page = requests.get(script_url)
    soup = BeautifulSoup(page.content, "html.parser")

    bold_elements = soup.find_all("b")
    bold_txt_ls = [b.contents[0].strip() for b in bold_elements]
    return bold_txt_ls


def get_character_names(bold_txt_ls):
    """Given the list of strings that were in bold in the script, determine which of these are character names"""
    bold_txt_set = set(bold_txt_ls)
    not_name_substrings = ["INT", "EXT", "CUT", "DRAFT", "Writers", "Genres"] + list(string.punctuation) + list(string.digits)

    character_names = []
    for txt_elem in bold_txt_set:
        found_ls = [substr in txt_elem for substr in not_name_substrings]
        if not(any(found_ls)):
            character_names.append(txt_elem)

    return character_names

