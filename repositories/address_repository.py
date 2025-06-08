import psycopg2
from database.Database import DBConnector

class AddressRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()
    
    def get_address(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ADDRESS;")
        address = cursor.fetchall()
        cursor.close()
        conn.close()
        return address
    
    def get_address_by_id(self, address_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ADDRESS WHERE ADDRESS_ID = %s;", (address_id,))
        address = cursor.fetchone()
        cursor.close()
        conn.close()
        return address
    
    def toggle_status(self, address_id, address_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE ADDRESS SET ADDRESS_STATUS = %s WHERE ADDRESS_ID = %s",
                (address_status, address_id)
            )
            conn.commit()
            return True  # ✅ Add this line
        except Exception as e:
            print("Database Error:", e)
            return False  # ✅ Optional for error handling
        finally:
            cursor.close()
            conn.close()


