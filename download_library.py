import logging
import os
import sqlite3

from gmusicapi import Musicmanager
from os import path


logger = logging.getLogger(__name__)


def save_log(text):
	log_file = open("log", "a")
	log_file.write(text)
	log_file.close()


def create_db():
	try:
		sqliteConnection = sqlite3.connect('songs.db')
		sqlite_create_table_query = '''CREATE TABLE success_ids (
					id INTEGER PRIMARY KEY,
					google_id TEXT NOT NULL;'''

		cursor = sqliteConnection.cursor()
		cursor.execute(sqlite_create_table_query)

		sqlite_create_table_query = '''CREATE TABLE failure_ids (
					id INTEGER PRIMARY KEY,
					google_id TEXT NOT NULL;'''
		cursor.execute(sqlite_create_table_query)

		sqliteConnection.commit()

		cursor.close()

	except sqlite3.Error as exc:
		logger.error(f'Error creating the database: {exc}')



mm = Musicmanager()
mm.perform_oauth()
mm.login()
songs = mm.get_uploaded_songs(incremental=False)


logger.info(f'There\'s {len(songs)} songs to download . . .')


for song in songs:
	if song['album_artist']:
		level_one = song['album_artist']
	elif song['artist']:
		level_one = song['artist']
	else:
		level_one = 'Unknown Artist'
	if song['album']:
		level_two = song['album']
	else:
		level_two =  'Unknown Album'
	full_path = f'{level_one}/{level_two}'
	try:
		os.mkdir(level_one)
	except FileExistsError:
		pass
	except Exception as exc:
		save_log(f"\n\n{song} \n {exc} \n\n")
		continue
	try:
		os.mkdir(full_path)
	except FileExistsError:
		pass
	except Exception as exc:
		save_log(f"\n\n{song} \n {exc} \n\n")
		continue
	try:
		downloaded_song = mm.download_song(song['id'])
	except Exception as exc:
		save_log(f"\n\n{song} \n {exc} \n\n")
	full_path += f"/{downloaded_song[0]}"
	file_path = path.relpath(full_path)
	file_to_write = open(file_path, "wb")
	file_to_write.write(downloaded_song[1])
	file_to_write.close()
