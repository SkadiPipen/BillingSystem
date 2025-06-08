import psycopg2
from database.Database import DBConnector

class CategoryRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()
    
    def get_category(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CATEGORY;")
        category = cursor.fetchall()
        cursor.close()
        conn.close()
        return category
    
    def get_category_by_id(self, categ_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM CATEGORY WHERE CATEG_ID = %s;",
            (categ_id,)
        )
        category = cursor.fetchall()
        cursor.close()
        conn.close()
        return category
    
    def create_category(self, categ_name, categ_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO CATEGORY (CATEG_NAME, CATEG_STATUS) VALUES (%s, %s) RETURNING CATEG_ID;",
                       (categ_name, categ_status))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    def toggle_status_category(self, categ_id, categ_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE CATEGORY SET CATEG_STATUS = %s WHERE CATEG_ID = %s",
                (categ_status, categ_id)
            )
            conn.commit()
            return True  # ✅ Add this line
        except Exception as e:
            print("Database Error:", e)
            return False  # ✅ Optional for error handling
        finally:
            cursor.close()
            conn.close()    
    
    def update_category(self, categ_id, categ_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE CATEGORY
            SET CATEG_NAME = %s
            WHERE CATEG_ID = %s
        """, (categ_name, categ_id))
        conn.commit()
        cursor.close()
        conn.close()
