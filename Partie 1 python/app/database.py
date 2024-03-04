import sqlite3

class Database:

    db_file = 'database.db'
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS cat_images
                            (id TEXT PRIMARY KEY,
                            image_url TEXT,
                            width INTEGER,
                            height INTEGER)''')
        self.conn.commit()


    def insert_cat_image(self, image_id, image_url, width, height):
        try:
            self.conn.execute("INSERT INTO cat_images (id, image_url, width, height) VALUES (?, ?, ?, ?)",
                          (image_id, image_url, width, height))
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'insertion des données : {e}")



    def fetch_data(self):
        cursor = self.conn.execute("SELECT * FROM data")
        return cursor.fetchall()
    
    def fetch_first_ten_entries(self):
        cursor = self.conn.execute("SELECT * FROM cat_images LIMIT 10")
        return cursor.fetchall()
    
    def fetch_all_entries(self):
        cursor = self.conn.execute("SELECT * FROM cat_images")
        return cursor.fetchall()
    
    def get_average_height(self):
        cursor = self.conn.execute("SELECT AVG(height) FROM cat_images")
        result = cursor.fetchone()
        return result[0] if result else None

    def get_average_width(self):
        cursor = self.conn.execute("SELECT AVG(width) FROM cat_images")
        result = cursor.fetchone()
        return result[0] if result else None

    def get_all_sizes(self):
        cursor = self.conn.execute("SELECT width, height FROM cat_images")
        return cursor.fetchall()





    def clear_table(self):
        self.conn.execute("DELETE FROM cat_images")
        self.conn.commit()

    def execute_query(self, query):
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
