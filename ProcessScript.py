import requests
from bs4 import BeautifulSoup

import Names
import pandas as pd
import Utilities

NAMES_GENDER_FILE = "btn_givennames.txt"

def get_bold_segments(script_url=Utilities.EXAMPLE_FILE):
    """Get all the bold elements <b> in the script page, that include the names of the characters when they speak"""
    page = requests.get(script_url)
    soup = BeautifulSoup(page.content, "html.parser")

    bold_elements = soup.find_all("b")
    bold_txt_ls = [b.contents[0].strip() for b in bold_elements]
    return bold_txt_ls


def get_dialogues(script_url=Utilities.EXAMPLE_FILE):
    """Given the URL containing the text of a movie script, transform each bolded line into one of:
    {'m','mf','f'}: a character speaks, their name is male/female/either
    'nd': non-dialogue, like the INT and EXT scene specifications"""

    bold_txt_ls = get_bold_segments(script_url)
    candidate_character_names = Names.get_character_names(bold_txt_ls)
    names_gender_df = pd.read_csv(NAMES_GENDER_FILE, sep='\t', names=["name", "gender"], skiprows=list(range(0, 8)))
    names_gender_dict = Names.get_names_gender(candidate_character_names, names_gender_df)

    sequence_ls = []
    for token in bold_txt_ls:
        if token in names_gender_dict.keys():
            sequence_ls.append(names_gender_dict[token])
        else:
            sequence_ls.append('nd')

    dialogues_lls = []
    current_dialogue = []
    for dialogue_token in sequence_ls:
        if dialogue_token in ['m', 'f', 'mf']:
            current_dialogue.append(dialogue_token)
        else:
            if len(current_dialogue) > 0:
                dialogues_lls.append(current_dialogue)
                current_dialogue = []

    return dialogues_lls


def locate_female_dialogues(dialogues_lls, min_lines=4):
    """ Locate the fragments of dialogue where only female characters participate.
    :param dialogues_lls: list of lists containing each dialogue with gender id. From: ProcessScript.get_dialogues(...)
    :param min_lines: The minimum number of lines in a scene to be considered a relevant dialogue
    :return: number of female dialogues, total number of dialogues"""

    tot_dialogues = 0
    female_dialogues = 0
    for dialogue in dialogues_lls:
        if len(dialogue) < min_lines:
            continue  # not a relevant dialogue
        if all([character_gender=='f' for character_gender in dialogue]):
            female_dialogues = female_dialogues + 1
        tot_dialogues = tot_dialogues + 1

    return female_dialogues, tot_dialogues