import logging
import urllib
from bs4 import BeautifulSoup
import requests
import re
import Utilities

SITE_URL = "https://imsdb.com"


def get_specific_urls(required_href_fragment, page_url, base_url, outer_element="a"):
    """ From the <a> elements in a page, possibly to be found inside a specified type of outer element,
    get all the URLs containing a required_href_fragment.
    Every URL is appended to base_url to deal with relative links.
    :return: list of strings (the URLs)"""

    page = requests.get(page_url)
    # if page.status_code == 404: # when the title has whitespaces, %20 may be necessary. E.g. Midnight%in%Paris
    #    page = requests.get(urllib.parse.quote(page_url))
    soup = BeautifulSoup(page.content, "html.parser")

    all_outer_elements = soup.find_all(outer_element)
    # It can be something else than "a", for instance "p" if the <p> elements contain the <a> we seek
    if outer_element != "a":
        all_links = []
        for outer_elem in all_outer_elements:
            for descendant in outer_elem.children:
                if descendant.name == "a" and "href" in descendant.attrs:
                    all_links.append(descendant)
    else:
        all_links = all_outer_elements
    specific_links = [base_url + tag_elem["href"] for tag_elem in all_links if (required_href_fragment in tag_elem.attrs["href"])]

    return specific_links


def retrieve_movies(max_movies_per_genre):
    """ Get all the movie URLs from imsdb.com, organized in a dictionary where keys are genres.
    n: A genre is present if it has at least 10 movies on imsdb.com
    :parameter: how many movies we wish to retrieve in each genre. Useful for small tests
    :return: dictionary with key=genre and value=list of movie URLs
    """
    genre_movies_dict = dict()
    genre_pages_urls = get_specific_urls("genre", SITE_URL, SITE_URL, "a")

    pattern = re.compile("(?<=/)[^/]*$")

    for genre_url in genre_pages_urls:
        genre = re.search(pattern, genre_url).group(0)
        logging.debug(genre)
        movie_pages_urls = get_specific_urls("Scripts", genre_url, SITE_URL, "p")
        movie_pages_urls = movie_pages_urls[0:max_movies_per_genre]
        if len(movie_pages_urls) >=5:  # a minimum
            genre_movies_dict[genre] = movie_pages_urls

    return genre_movies_dict


def retrieve_script_pages(genre_movies_dict):
    """ Given the dictionary that contains the URLs of the movie pages organized by genre,
    eliminate duplicates and find the URLs of the script pages.
    :return: a list of URLs (strings)
    """
    movies_lls = list(genre_movies_dict.values())
    movies_ls = sum(movies_lls, [])
    movies_ls_noduplicates = list(set(movies_ls))

    scripts_ls = []
    num_movies = len(movies_ls_noduplicates)
    for i, movie_page in enumerate(movies_ls_noduplicates):
        script_page_ls = get_specific_urls("scripts", movie_page, SITE_URL, outer_element="td")
        if len(script_page_ls) != 1:
            logging.info("Could not find 1 script on the site; movie_page= " + movie_page)
            continue
        script_page = script_page_ls[0]
        scripts_ls.append(script_page)
        if i % (num_movies//10) == 0:
            logging.info("Retrieving scripts: " + str(i) + "/" + str(num_movies) + " movies...")

    return scripts_ls


def run_scraping(max_movies_per_genre):
    """  Entry point function: access the imsdb.com site to get the URLs for movies and scripts
    :return: genre_movies_dict (the movie URLs, by genre, in a dictionary); scripts_ls (the URLs for all the scripts)
    """
    # Utilities.init_logging("Scraping.log")
    genre_movies_dict = retrieve_movies(max_movies_per_genre)
    scripts_ls = retrieve_script_pages(genre_movies_dict)

    return genre_movies_dict, scripts_ls