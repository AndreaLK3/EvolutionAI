import string


def get_character_names(bold_txt_ls):
    """Given the list of strings that were in bold in the script, determine which of these are character names"""
    bold_txt_set = set(bold_txt_ls)
    not_name_substrings = ["INT", "EXT", "CUT", "DRAFT", "Writers", "Genres"] + list(string.punctuation) + list(string.digits)

    candidate_character_names = []
    for txt_elem in bold_txt_set:
        found_ls = [substr in txt_elem for substr in not_name_substrings]
        if not(any(found_ls)):
            txt_elem = txt_elem.replace("(V.0.)", "")
            candidate_character_names.append(txt_elem)

    return candidate_character_names


def get_gender_from_intro(name):
    """Check if a character name has an introduction (Mr./Ms.). In which case the gender of the character is obvious"""
    female_intro = ["MS", "MISS", "MRS", "LADY", "MADAME", "MADEMOISELLE", "DEMOISELLE", "QUEEN"]
    male_intro = ["MR", "MISTER", "LORD", "MONSIEUR", "SIR", "KING", "FATHER"]

    if any([substr in name for substr in female_intro]):
        gender = "f"
    elif any([substr in name for substr in male_intro]):
        gender = "m"        # the order of the check is determined by Mr vs. Mrs
    else:
        gender = None  # no solution from here
    return gender


def get_gender_from_df(name, df):
    """Consult the Dataframe containing the columns "name" and "gender" """
    name_adjusted = name[0].upper() + name[1:].lower()
    try:
        gender = df[df["name"] == name_adjusted]["gender"].item()
    except ValueError:
        gender = None
    return gender


def get_names_gender(candidate_names_ls, names_gender_df):
    """ Given a list of character names, determine their gender,
    and store it in a dictionary that will be used when processing the script of a movie"""
    names_gender_dict = dict()

    for name in candidate_names_ls:
        if len(name)>=1:
            gender = get_gender_from_intro(name)
            if gender is not None:
                names_gender_dict[name] = gender
                continue
            else:
                # We consult the archive from BehindTheNames.com
                gender = get_gender_from_df(name, names_gender_df)
                if gender is None:  # name not found.
                    if len(name.split()) > 1:  # Maybe the name has two words, like "John Reed". Try again with each
                        first_name = name.split()[0]
                        gender = get_gender_from_df(first_name, names_gender_df)
                        if gender is None:
                            second_name = name.split()[1]
                            gender = get_gender_from_df(second_name, names_gender_df)

                if gender is None:  # We just can not find it, e.g. "Rochester"
                    gender = "mf"
            names_gender_dict[name] = gender

    return names_gender_dict

