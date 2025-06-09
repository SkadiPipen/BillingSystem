import psycopg2
from database.Database import DBConnector

class MeterRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_all_meters(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT m.METER_ID, m.SERIAL_NUMBER, m.METER_CODE, 
                    m.METER_LAST_READING_DATE, c.CLIENT_NAME, c.CLIENT_LNAME
                FROM METER m
                LEFT JOIN CLIENT c ON c.METER_ID = m.METER_ID
                WHERE m.status = 'Active'
                ORDER BY m.METER_ID ASC
            """)

            meters = cursor.fetchall()

            formatted_meters = [
                (meter_code, f"{client_name} {client_lname}" if client_name and client_lname else "N/A",
                serial_number, last_read, meter_id)
                for (meter_id, serial_number, meter_code, last_read, client_name, client_lname) in meters
            ]

            return formatted_meters

        except Exception as e:
            print(f"Database error: {e}")
            return []

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    

    def create_meter(self, meter_last_reading, serial_number):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO METER (
                METER_LAST_READING, METER_LAST_READING_DATE, METER_CODE, SERIAL_NUMBER
            ) VALUES (
                %s, CURRENT_DATE,
                'MTR-' || LPAD(nextval('meter_code_alphanumeric')::text, 5, '0'), %s
            )
            RETURNING METER_ID;
        """, (
            meter_last_reading, serial_number
        ))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    def update_meter_latest_reading(self, pres_read, read_date, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE METER
                       SET METER_LAST_READING      = %s,
                           METER_LAST_READING_DATE = %s
                       WHERE METER_ID = %s
                       """, (pres_read, read_date, meter_id))
        conn.commit()
        cursor.close()
        conn.close()
    
    def update_meter(self, meter_id, serial_number, meter_code, last_read):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE meter 
                SET serial_number = %s, 
                    meter_code = %s, 
                    meter_last_read = %s  
                WHERE meter_id = %s
            """, (
                serial_number, 
                meter_code, 
                last_read, 
                meter_id
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_readings_by_meter_id(self, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT reading_date, reading_prev, reading_current, is_voided
                       FROM READING
                       WHERE METER_ID = %s
                       ORDER BY READING_DATE DESC
                       """, (meter_id,))
        readings = cursor.fetchall()
        cursor.close()
        conn.close()
        return readings

    def replace_meter(self, old_meter_id, new_serial_number, initial_reading):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Mark old meter as replaced
            cursor.execute("UPDATE meter SET status = 'Replaced' WHERE meter_id = %s", (old_meter_id,))

            # Get client linked to old meter
            cursor.execute("SELECT client_id FROM client WHERE meter_id = %s", (old_meter_id,))
            result = cursor.fetchone()
            if not result:
                raise Exception("No client linked to this meter.")
            client_id = result[0]

            # Insert new meter with user-defined initial reading
            cursor.execute("""
                              INSERT INTO meter (meter_code, serial_number, meter_last_reading, meter_last_reading_date,
                                                 status)
                              VALUES ('MTR-' || LPAD(nextval('meter_code_alphanumeric')::text, 5, '0'),
                                      %s, %s, CURRENT_DATE, 'Active') RETURNING meter_id
                              """, (new_serial_number, initial_reading))

            new_meter_id = cursor.fetchone()[0]

            # Link client to new meter
            cursor.execute("UPDATE client SET meter_id = %s WHERE client_id = %s", (new_meter_id, client_id))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error replacing meter: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def serial_exists(self, serial_number):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM meter WHERE serial_number = %s LIMIT 1", (serial_number,))
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists

    def get_meter_previous_reading(self, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT meter_last_reading FROM METER WHERE METER_ID = %s", (meter_id,))
        last_reading = cursor.fetchone()
        cursor.close()
        conn.close()
        return last_reading[0] if last_reading else None

    def get_meter_by_id(self, meter_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.METER_ID, m.SERIAL_NUMBER, m.METER_CODE, 
                    m.METER_LAST_READING, m.METER_LAST_READING_DATE,
                    c.CLIENT_NAME, c.CLIENT_LNAME
                FROM METER m
                LEFT JOIN CLIENT c ON c.METER_ID = m.METER_ID
                WHERE m.METER_ID = %s
            """, (meter_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching meter by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()    


    def get_meter_id_by_reading_id(self, reading_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT meter_id FROM reading WHERE reading_id = %s", (reading_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None



        

