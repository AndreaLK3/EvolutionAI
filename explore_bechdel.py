import logging
import sqlite3
import Scraping
import pickle
import ProcessScript
import Utilities
import argparse
import os

def parse_training_arguments():
    parser = argparse.ArgumentParser(description='Examine if the movies on IMSDB pass the Bechdel test.'
                'Computes genre and movie statistics, saved on a database')

    parser.add_argument('--movies_per_genre', type=int, default=30,
                        help='maximum number of movies analyzed, in each genre')

    args = parser.parse_args()
    return args


def store_movie_stats(movie_title, stats_4_lines, stats_8_lines):
    """ Once we have computed how many dialogues with 4/8 lines have only women, no women, and their total,
    store this in a database. Two tables (for 4 and 8 lines), one movie == one row"""
    db = sqlite3.connect(Utilities.RESULTS_DATABASE)
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS movie_dialogues_4_lines
             (movie varchar(128), dialogues_only_women INT, dialogues_no_women INT, tot_dialogues INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS movie_dialogues_8_lines
                 (movie varchar(128), dialogues_only_women INT, dialogues_no_women INT, tot_dialogues INT)""")

    cursor.execute("INSERT INTO movie_dialogues_4_lines VALUES (?,?,?,?)",
                   (movie_title, stats_4_lines[0], stats_4_lines[1], stats_4_lines[2]))
    cursor.execute("INSERT INTO movie_dialogues_8_lines VALUES (?,?,?,?)",
                   (movie_title, stats_8_lines[0], stats_8_lines[1], stats_8_lines[2]))
    db.commit()
    db.close()


if __name__ == "__main__":
    args = parse_training_arguments()
    Utilities.init_logging("Explore Bechdel Stats.log")

    _, scripts_ls = Scraping.run_scraping(args.movies_per_genre)

    # delete database with old results
    if os.path.exists(Utilities.RESULTS_DATABASE):
        os.remove(Utilities.RESULTS_DATABASE)

    for i, script_url in enumerate(scripts_ls):
        movie_title = Utilities.get_movie_title_from_script_url(script_url)
        if movie_title is None:
            continue
        dialogues_lls = ProcessScript.get_dialogues(script_url)
        dialogues_only_w_4, dialogues_no_w_4, tot_dialogues_4 = ProcessScript.locate_gender_dialogues(dialogues_lls, min_lines=4)
        dialogues_only_w_8, dialogues_no_w_8, tot_dialogues_8 = ProcessScript.locate_gender_dialogues(dialogues_lls, min_lines=8)

        # insert statistics into database
        stats_4_lines = dialogues_only_w_4, dialogues_no_w_4, tot_dialogues_4
        stats_8_lines = dialogues_only_w_8, dialogues_no_w_8, tot_dialogues_8
        store_movie_stats(movie_title, stats_4_lines, stats_8_lines)
        if i % (len(scripts_ls)//20) == 0:
            logging.info("Locating dialogues and gender of speakers: " + str(i) + "/" + str(len(scripts_ls)) + " scripts...")

    logging.info("The results can be found in: " + Utilities.RESULTS_DATABASE)


