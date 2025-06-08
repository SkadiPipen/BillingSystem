import psycopg2
from database.Database import DBConnector

class UserRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()
    
    def get_user_by_id(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM USER WHERE ID = %s;",
            (user_id,)
        )
        user = cursor.fetchall()
        cursor.close()
        conn.close()
        return user

    def check_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ROLE FROM USERS WHERE USERNAME = %s AND PASSWORD = %s;", (username, password))
        role = cursor.fetchone()
        cursor.close()
        conn.close()
        return role[0] if role else None

    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS;")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    
    def get_all_employee(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.USER_ID, u.NAME, u.USERNAME
                FROM USERS u
            """)
            users = cursor.fetchall()

            formatted_clients = [
                (
                    user_id, name, username
                )
                for user_id, name, username in users
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
    
    def create_user(self, username, password, role, name, user_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO USERS (USERNAME, PASSWORD, ROLE, NAME, USER_STATUS)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING _ID;
        """, (username, password, role, name, user_status))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id


    def update_user(self, username, password, role, name, user_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE USERS 
            SET USERNAME = %s, PASSWORD = %s, role = %s, name = %s, user_status = %s 
            WHERE METER_ID = %s
        """, (username, password, role, name, user_status))
        conn.commit()
        cursor.close()
        conn.close()
