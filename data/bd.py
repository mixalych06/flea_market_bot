import sqlite3


class DataBase:
    def __init__(self, bd_file):
        self.connection = sqlite3.connect(bd_file)
        self.cursor = self.connection
        self.connection.execute('CREATE TABLE IF NOT EXISTS users_products (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,users_id,'
                                'name_users, date, photo_id, product_name, specifications, priсe,'
                                'contact, value INTEGER DEFAULT 1)')
        self.connection.commit()

    def add_column(self):
        with self.connection:
            self.cursor.execute("ALTER TABLE users_products ADD COLUMN city")
            self.connection.commit()

    def adds_user_products(self, user_product):
        with self.connection:
            self.cursor.execute("INSERT INTO users_products (users_id, name_users, date, city, photo_id, product_name, specifications, priсe, contact)"
                                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_product)
            self.connection.commit()

    def exists_id_product(self, users_id, photo_id):
        """Отдаёт обьявление по id пользователя и id фото"""
        with self.connection:
            return self.cursor.execute("SELECT ID FROM users_products WHERE users_id = ? AND photo_id = ?", (users_id, photo_id)).fetchone()[0]

    def exists_product(self, id_ad):
        """Ищет обьявление по id"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM users_products WHERE ID = ?", (id_ad,)).fetchall()

    def del_ad_bd(self, id_ad):
        """удаление обьявления из базы"""
        with self.connection:
            self.cursor.execute("DELETE FROM users_products WHERE ID = ? ", (id_ad,))
            self.connection.commit()

    def user_products(self, id_user):
        """Ищет обьявление по id user"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM users_products WHERE users_id = ?", (id_user,)).fetchall()

    def number_of_entries_user_products(self, id_user):
        """Ищет количество записей по id user"""
        with self.connection:
            a = self.cursor.execute("SELECT product_name FROM users_products WHERE users_id = ?", (id_user,)).fetchall()
            return len(a)

    def update_value(self, id_message, id_ad):
        """Записывает id объявления размещенного наканале"""
        with self.connection:
            self.cursor.execute("UPDATE users_products SET value = ? WHERE ID = ?", (id_message, id_ad,))



