import sqlite3
from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if name:
            # Insert new author into database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
            self._id = cursor.lastrowid
            self._name = name
            conn.commit()
            conn.close()
        elif id and name:
            # Retrieve the author from the database by id
            self._id = id
            self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return f'<Author {self.name}>'

    @staticmethod
    def get_by_id(author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        author = cursor.fetchone()
        conn.close()
        if author:
            return Author(author["id"], author["name"])
        return None

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles
            WHERE author_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles]

    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM magazines
            WHERE id IN (SELECT magazine_id FROM articles WHERE author_id = ?)
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in magazines]
