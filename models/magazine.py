import sqlite3
from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category="General"):
        if name and category:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
            self._id = cursor.lastrowid
            self._name = name
            self._category = category
            conn.commit()
            conn.close()
        elif id:
            self._id = id
            self._name = name
            self._category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str) or len(new_name) < 2 or len(new_name) > 16:
            raise ValueError("Magazine name must be between 2 and 16 characters")
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if not isinstance(new_category, str) or len(new_category) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = new_category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return [{"id": contributor["id"], "name": contributor["name"]} for contributor in contributors]
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title["title"] for title in titles] if titles else None

    def contributing_authors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT author_id FROM articles
            WHERE magazine_id = ?
            GROUP BY author_id
            HAVING COUNT(*) > 2
        ''', (self.id,))
        author_ids = cursor.fetchall()
        conn.close()
        authors = []
        for author_id in author_ids:
            authors.append(Author.get_by_id(author_id["author_id"]))
        return authors if authors else None