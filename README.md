### Task
We are interested in looking for movies that pass the Bechdel test (https://en.wikipedia.org/wiki/Bechdel_test). We've found a website that has a large collection of movie scripts - http://www.imsdb.com/.  We would like you to scrape a few hundred scripts from this website (doesn't have to be all of them), and look for instances where a female character is talking to another female character.  Produce some statistics for the movies you have data for, that you think would be relevant to the Bechdel test.

### Method
We observe that characters, changes of scene, and scene descriptions are all introduced by a 
<b>bold</b> element in IMSDB. We use this to get the names - and from the names, the gender - of the characters in the movie.<br/>
Every sequence with characters that speak uninterrupted is considered a <b>dialogue</b>. 
We focus on dialogues with 4 lines and 8 lines, to try and pick exchanges that are somewhat relevant. <br/>
How many dialogue segments can be found in each movie? How many of them have only women speaking? How many have no women present at all?

##### Running the pipeline
- `pip install -r requirements.txt` installs `pandas`, `bs4` (BeautifulSoup, for scraping) and `requests`.
- Then, `python explore_bechdel.py` will collect the scripts from https://imsdb.com/ and read them to create the statistics 
  on the genders of speakers in dialogues
  <br/>
  - Optional parameter: `--movies_per_genre` (int), to limit the amount of movies selected for analysis from each genre.
    <br/>
    The default value is 40, resulting in 343 scripts given that several movies belong to more than one genre
    <br/>
    It can be set to a very high value (e.g. 500) to process all the movies on IMSDB, resulting in the analysis of 1150 scripts
- The results are stored in the database `Results.db` using `sqlite3`

#### Note:
The pipeline `Scripts -> Names -> Genders -> Dialogues -> Statistics`
is fully functional, but its effectiveness is limited by the fact that we attempt to guess the
character's gender by checking the name's gender in `btn_givennames.txt`, from https://www.behindthename.com/.
<br/>
<br/>
Relying on the names of the actors would be better and determine nearly every character's gender,
but it would require accessing IMDB movie data or scraping from Wikipedia, and thus more development time. 

### Steps

#### 1) Scraping
In `Scraping.py`: <br/>
From https://imsdb.com, access each genre's page to scrape the URLs for all the movie pages. <br/>
Then, in each movie page find the script page URL, if it exists

#### 2) Getting the names of a movie's characters and finding their gender
In `Names.py`:<br/>
Considering all the text fragments that were bold in the script, determine which are the character names. 
We exclude all the scene descriptions (INT, EXT) and scene CUTs<br/>
Then, consult the file taken from https://www.behindthename.com/ to guess a character's gender. It is set to "mf" if we can not find out.

#### 4) Locating dialogue sequences
In `ProcessScript.py`:<br/>
The bold segments of the script are either characters speaking or scene cuts and descriptions. Find the sequences
where the characters speak uninterrupted and transform them into a sequence of speaker genders, e.g. `[m,f,f,m,f]`

#### 5) Examining the gender of the speakers and saving the results
In `ProcessScript.py`, `explore_bechdel.py`: <br/>
How many dialogues of 4 (or 8) lines can we find in a movie? How many of them have only women speaking? How many have no women present at all?
<br/>