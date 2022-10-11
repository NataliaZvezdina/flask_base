import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Error while reading from db {e}")
        return []

    def add_post(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute(
                "INSERT INTO posts(title, text, time) "
                "VALUES(?, ?, ?)", (title, text, tm)
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"Error while adding post to db {e}")
            return False
        return True

    def get_post(self, post_id):
        try:
            self.__cur.execute(
                f'SELECT title, text FROM posts WHERE id = {post_id}'
            )
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Error while getting post to db {e}")

        return False, False

    def get_posts_overview(self):
        try:
            self.__cur.execute('SELECT id, title, text FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Error while getting posts overview from db {e}")
        return []
