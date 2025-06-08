import psycopg2
from PyQt5 import QtWidgets

from database.Database import DBConnector

class ClientRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()
    
    def get_client_by_id(self, client_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM CLIENT WHERE CLIENT_ID = %s;",
            (client_id,)
        )
        client = cursor.fetchall()
        cursor.close()
        conn.close()
        return client


    def get_all_clients(self): 
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.CLIENT_ID, c.CLIENT_NUMBER, c.CLIENT_NAME, c.CLIENT_MNAME, c.CLIENT_LNAME, c.CLIENT_CONTACT_NUM,
                    cat.CATEG_NAME,  a.ADDRESS_NAME, c.CLIENT_LOCATION, c.CLIENT_DATE_CREATED, c.CLIENT_STATUS
                FROM CLIENT c
                JOIN CATEGORY cat ON c.CATEG_ID = cat.CATEG_ID
                JOIN ADDRESS a ON c.ADDRESS_ID = a.ADDRESS_ID
                ORDER BY client_id ASC
            """)
            clients = cursor.fetchall()

            formatted_clients = [
                (
                    client_id, client_number, fname, middle_name, lname, contact, categ_name, address_id, location, created_at, client_status
                )
                for  client_id, client_number, fname, middle_name, lname, contact, categ_name, address_id, location, created_at,  client_status in clients
            ]

            return formatted_clients

        except Exception as e:
            print(f"Database error: {e}")
            return []

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()



    def create_client(self, client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CLIENT (
                CLIENT_NAME, CLIENT_LNAME, CLIENT_CONTACT_NUM, CLIENT_LOCATION,
                METER_ID, ADDRESS_ID, CATEG_ID, CLIENT_MNAME, CLIENT_STATUS, CLIENT_NUMBER
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                LPAD(nextval('client_number_seq')::text, 5, '0')        
            )
            RETURNING CLIENT_ID;
        """, (
            client_name, client_lname, client_contact_num, client_location,
            meter_id, address_id, categ_id, client_mname, status
        ))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id


    def update_client(self, client_id, fname, lname, contact, location, mname):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE CLIENT 
                SET CLIENT_NAME = %s, 
                    CLIENT_LNAME = %s, 
                    CLIENT_CONTACT_NUM = %s, 
                    CLIENT_LOCATION = %s, 
                    CLIENT_MNAME = %s  
                WHERE CLIENT_ID = %s
            """, (
                fname,          # CLIENT_NAME
                lname,          # CLIENT_LNAME
                contact,        # CLIENT_CONTACT_NUM
                location,       # CLIENT_LOCATION
                mname,          # CLIENT_MNAME
                client_id       # WHERE CLIENT_ID
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            QtWidgets.QMessageBox.critical(None, "Database Error", str(e))
        finally:
            cursor.close()
            conn.close()


    def update_client_status(self, client_id, new_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE CLIENT SET CLIENT_STATUS = %s WHERE CLIENT_ID = %s",
                (new_status, client_id)
            )
            conn.commit()
            return True  # ✅ Add this line
        except Exception as e:
            print("Database Error:", e)
            return False  # ✅ Optional for error handling
        finally:
            cursor.close()
            conn.close()        
            
            