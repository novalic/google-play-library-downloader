Google Play Music Library Download
=

This script will download your whole google play music library. Each downloaded song is saved into a database, so if the script fails while running, you won't be downloading songs twice. If a song fails downloading, it will be saved to database with downloaded equals to 0: you should try downloading this again manually.

The generated directory structure is of the format:

`[album_artist | artist]/album_name`

And inside each album, you will get:

`track_id - track_name`

Usage
-

- In a terminal run:

`python download_library.py`

- You will get a link to login with the google account where all the music is, google will give you a string that you have to copy and then paste it back into the terminal and hit enter.

- Let it r(b)u(r)n.


Dependencies
-

- Python >= v3.6

### Packages

For this program to work you will need to (virtual environment recommended) install:

- (pip install) sqlite3
- (pip install) gmusicapi

