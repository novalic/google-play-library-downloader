import logging
import os
import sqlite3

from gmusicapi import Musicmanager
from os import path


def start_db():
	try:
		sqliteConnection = sqlite3.connect('songs.db')
		sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS song (
					id INTEGER PRIMARY KEY,
					google_id TEXT NOT NULL,
					downloaded INTEGER);'''

		cursor = sqliteConnection.cursor()
		cursor.execute(sqlite_create_table_query)

		sqliteConnection.commit()

		cursor.close()

	except sqlite3.Error as exc:
		return

	return sqliteConnection


def insert_song(connection, song_id, failure=False):
	sql = ''' INSERT INTO song (google_id, downloaded)
	      VALUES(?,?) '''

	cursor = connection.cursor()
	cursor.execute(sql, (song_id, int(not failure)))
	connection.commit()
	lastrowid = cursor.lastrowid
	cursor.close()

	return lastrowid


def get_all_song_ids(connection):
	sql = ''' SELECT google_id from song WHERE downloaded = 1;'''

	cursor = connection.cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	return {r[0] for r in results}


def main():
	mm = Musicmanager()
	mm.perform_oauth()
	mm.login()
	songs = mm.get_uploaded_songs(incremental=False)

	db_connection = start_db()
	already_downloaded = get_all_song_ids(db_connection)


	for song in songs:
		song_id = song['id']

		if song_id in already_downloaded:
			continue

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
			insert_song(db_connection, song_id, True)
			continue

		try:
			os.mkdir(full_path)
		except FileExistsError:
			pass
		except Exception as exc:
			insert_song(db_connection, song_id, True)
			continue

		try:
			downloaded_song = mm.download_song(song_id)
		except Exception as exc:
			insert_song(db_connection, song_id, True)

		full_path += f"/{downloaded_song[0]}"
		file_path = path.relpath(full_path)
	
		file_to_write = open(file_path, "wb")
		file_to_write.write(downloaded_song[1])
		file_to_write.close()
		insert_song(db_connection, song_id)


if __name__ == "__main__":
    main()
