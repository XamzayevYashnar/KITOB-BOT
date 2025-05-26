import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("baza_2.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(""" 
         CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id TEXT,
             username TEXT,
             phone_number TEXT
         );
         """)

        self.cursor.execute(""" 
         CREATE TABLE IF NOT EXISTS books (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             categorie_id INTEGER,
             category_name TEXT,
             name TEXT, 
             image TEXT,
             price TEXT,
             author TEXT,
             sarlavha TEXT,
             FOREIGN KEY (categorie_id) REFERENCES categories(id)
         );
         """)

        self.cursor.execute(""" 
         CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
         );
         """)

        self.cursor.execute(""" 
         CREATE TABLE IF NOT EXISTS order_1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            name TEXT,
            count TEXT,
            price TEXT,
            total_price TEXT,
            author TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
         );
         """)

        self.cursor.execute(""" 
         CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            name TEXT,
            count TEXT,
            price TEXT,
            total_price TEXT,
            author TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
         );
         """)
        self.conn.commit()

        self.cursor.execute(""" 
         CREATE TABLE IF NOT EXISTS buy_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            phone_number TEXT,
            latitude TEXT,
            longitude TEXT,
            name_product TEXT,
            one_price TEXT,
            total_price TEXT,
            count TEXT
         );
         """)
        self.conn.commit()

class User(Database):
    def add_user(self, user_id, username, phone_number):
        self.cursor.execute(""" 
        INSERT INTO users (user_id, username, phone_number) 
        VALUES (?, ?, ?)
        """, (user_id, username, phone_number))
        self.conn.commit()

    def check_users(self, user_id):
        result = self.cursor.execute(""" 
        SELECT * FROM users WHERE user_id = ? 
        """, (user_id,)).fetchone()
        return result is not None

    def get_phone_number(self, user_id):
        number = self.cursor.execute(""" SELECT * FROM users WHERE user_id = ? """, (user_id,)).fetchone()
        return number


class Book(Database):
    def add_book(self, categorie_id, category_name, name, image, price, author, sarlavha):
        self.cursor.execute(""" 
        INSERT INTO books (categorie_id, category_name, name, image, price, author, sarlavha) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (categorie_id, category_name, name, image, price, author, sarlavha))
        self.conn.commit()

    def get_books(self, name_book):
        result = self.cursor.execute(""" 
        SELECT * FROM books WHERE name = ? 
        """, (name_book,)).fetchone()
        return result

    def get_book_id(self, book_name):
        result = self.cursor.execute(""" SELECT id FROM books WHERE name = ? """, (book_name,)).fetchone()[0]
        return result

    def add_order(self, user_id, name, count, price, total_price, author):
        self.cursor.execute(""" 
        INSERT INTO order_1 (user_id, name, count, price, total_price, author) 
        VALUES (?, ?, ?, ?, ?, ?) 
        """, (user_id, name, count, price, total_price, author))
        self.conn.commit()

    def get_orders(self, user_id):
        result = self.cursor.execute(""" 
        SELECT * FROM order_1 WHERE user_id = ? 
        """, (user_id,)).fetchall()
        return result

    def delete_cart(self, user_id):
        self.cursor.execute(""" 
        DELETE FROM cart WHERE user_id = ? 
        """, (user_id,))
        self.conn.commit()


class Categories(Database):
    def get_categories_for_button(self):
        result = self.cursor.execute(""" 
        SELECT * FROM categories 
        """).fetchall()
        return result

    def mt_books(self, name):
        row = self.cursor.execute(""" 
        SELECT id FROM categories WHERE name = ? 
        """, (name,)).fetchone()
        if row:
            categorie_id = int(row[0])
            natija = self.cursor.execute(""" 
            SELECT * FROM books WHERE categorie_id = ? 
            """, (categorie_id,)).fetchall()
            return natija
        return []

    def get_books_for_name(self, name_book):
        result = self.cursor.execute(""" SELECT * FROM books WHERE name = ? """, (name_book,)).fetchone()
        return result

    def check_categorie(self, category_name):
        result = self.cursor.execute(""" SELECT * FROM categories WHERE name = ? """, (category_name,)).fetchone()
        return result

    def check_order(self, user_id):
        result = self.cursor.execute(""" SELECT * FROM order_1 WHERE user_id = ? """, (user_id,)).fetchall()
        return result

    def add_categorie(self, name):
        self.cursor.execute(""" 
        INSERT INTO categories (name) VALUES (?) 
        """, (name,))
        self.conn.commit()

    def get_books_for_id_product(self, product_id):
        result = self.cursor.execute(""" SELECT * FROM books WHERE id = ? """, (product_id,)).fetchone()
        return result


class Cart(Database):
    def add_cart(self, user_id, name, count, price, total_price, author):
        self.cursor.execute(""" 
        INSERT INTO cart (user_id, name, count, price, total_price, author) 
        VALUES (?, ?, ?, ?, ?, ?) 
        """, (user_id, name, count, price, total_price, author))
        self.conn.commit()

    def get_cart(self, user_id):
        result = self.cursor.execute(""" 
        SELECT * FROM cart WHERE user_id = ? 
        """, (user_id,)).fetchall()
        return result

    def add_history(self, user_id, username, phone_number, latitude, longitude, name_product, one_price, total_price, count):
        self.cursor.execute(""" INSERT INTO buy_history (user_id, username, phone_number, latitude, longitude, name_product, one_price, total_price, count)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
         """, (user_id, username, phone_number, latitude, longitude, name_product, one_price, total_price, count))
        self.conn.commit()