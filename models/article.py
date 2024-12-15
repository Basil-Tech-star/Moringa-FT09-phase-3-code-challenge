import sqlite3
from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        if title and content and author_id and magazine_id:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                           (title, content, author_id, magazine_id))
            self._id = cursor.lastrowid
            self._title = title
            self._content = content
            self._author_id = author_id
            self._magazine_id = magazine_id
            conn.commit()
            conn.close()
        elif id:
            self._id = id
            self._title = title
            self._content = content
            self._author_id = author_id
            self._magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if not isinstance(new_title, str) or len(new_title) < 5 or len(new_title) > 50:
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = new_title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'

    def author(self):
        from models.author import Author
        return Author.get_by_id(self._author_id)

    def magazine(self):
        from models.magazine import Magazine
        return Magazine(self._magazine_id)
