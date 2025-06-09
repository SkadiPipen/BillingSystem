import psycopg2
from database.Database import DBConnector

class ReadingRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_all_reading(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM READING;")
        readings = cursor.fetchall()
        cursor.close()
        conn.close()
        return readings

    def get_reading_by_id(self, reading_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT reading_prev, reading_current
                FROM READING
                WHERE reading_id = %s;
            """, (reading_id,))
            result = cursor.fetchone()
            return result  # Tuple like (123, 234)
        except Exception as e:
            print(f"[DB ERROR] Failed to get reading: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def create_reading(self, read_date, prev_read, pres_read, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO READING (READING_DATE, READING_PREV, READING_CURRENT, METER_ID)
            VALUES (%s, %s, %s, %s)
            RETURNING READING_ID;
        """, (read_date, prev_read, pres_read, meter_id))
        new_reading_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return new_reading_id
    
    def get_reading_id_by_billing_id(self, billing_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT reading_id FROM billing WHERE billing_id = %s", (billing_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    
    def void_reading(self, reading_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE reading SET is_voided = true WHERE reading_id = %s", (reading_id,))
        conn.commit()
        cursor.close()
        conn.close()




