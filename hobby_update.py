import json
import sqlite3
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

DATABASE_NAME = 'hobbies.db'
DATA_JSON_PATH = 'hobby_data/data.json'


class HobbyDatabase:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hobbies (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE NOT NULL,
                profile_id TEXT NOT NULL,
                hobby_desc TEXT NOT NULL,
                hobby_link TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def insert_hobby(self, title, profile_id, hobby_desc, hobby_link):
        try:
            self.cursor.execute('''
                INSERT INTO hobbies (title, profile_id, hobby_desc, hobby_link)
                VALUES (?, ?, ?, ?)
            ''', (title, profile_id, hobby_desc, hobby_link))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Хобби '{title}' уже существует в базе данных.")

    def close(self):
        self.connection.close()

class DataHandler(FileSystemEventHandler):
    def __init__(self, db):
        self.db = db

    def on_modified(self, event):
        if event.src_path == DATA_JSON_PATH:
            print(f"Файл {DATA_JSON_PATH} изменен. Обновление базы данных...")
            self.update_database()

    def update_database(self):
        with open(DATA_JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for key, value in data.items():
                title = value['title']
                profile_id = value['profile_id']
                hobby_desc = value['description']['hobby_desc']
                hobby_link = value['description']['hobby_link']
                self.db.insert_hobby(title, profile_id, hobby_desc, hobby_link)

def main():
    db = HobbyDatabase(DATABASE_NAME)
    
    event_handler = DataHandler(db)
    observer = Observer()
    observer.schedule(event_handler, path='hobby_data/', recursive=False)

    observer.start()
    print(f"Начато отслеживание изменений в {DATA_JSON_PATH}...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    db.close()


if __name__ == '__main__':
    main()
