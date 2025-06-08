import psycopg2
from database.Database import DBConnector

class BillingRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_billing_by_id(self, billing_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BILLING WHERE ID = %s;", (billing_id,))
        bill = cursor.fetchone()
        cursor.close()
        conn.close()
        return bill

    def get_bill_data(self, billing_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT c.CLIENT_NAME,
                              c.CLIENT_LNAME,
                              c.CLIENT_LOCATION,
                              c.CLIENT_NUMBER,
                              b.BILLING_CODE,
                              b.BILLING_DUE,
                              CURRENT_DATE,
                              r.READING_PREV,
                              r.READING_CURRENT,
                              b.BILLING_CONSUMPTION,
                              b.BILLING_AMOUNT,
                              c.CATEG_ID,
                              b.BILLING_SUB_CAPITAL,
                              b.BILLING_LATE_PAYMENT,
                              b.BILLING_PENALTY,
                              b.BILLING_TOTAL_CHARGE,
                              b.BILLING_TOTAL
                       FROM BILLING AS b
                                JOIN CLIENT AS c ON b.CLIENT_ID = c.CLIENT_ID
                                JOIN READING AS r ON b.READING_ID = r.READING_ID
                       WHERE b.BILLING_ID = %s;
                       """, (billing_id,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None  # No data found

        (
            client_fname, client_lname, address, client_number, bill_code, due_date, current_date,
            prev_reading, current_reading, meter_consumed, amount, categ_id,
            subscribe_capital, late_payment, penalty, total_charges, total_amount
        ) = row

        # Concatenate the first name and last name
        full_name = f"{client_lname}, {client_fname}"

        # Determine category code based on CATEG_ID
        category_code_map = {
            100001: 1,
            100002: 2,
            100003: 3,
            100004: 4
        }
        category_code = category_code_map.get(categ_id, 0)  # Default to 0 if not found

        data = {
            "client_name": full_name,
            "address": address,
            "client_num": client_number,
            "bill_code": bill_code,
            "due_date": due_date,
            "current_date": current_date,
            "prev_reading": prev_reading,
            "current_reading": current_reading,
            "meter_consumed": meter_consumed,
            "amount": amount,
            "category_code": category_code,
            "subscribe_capital": subscribe_capital,
            "late_payment": late_payment,
            "penalty": penalty,
            "total_charges": total_charges,
            "total_amount_due": total_amount
        }

        return data

    def get_billing_id(self, billing_code):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT BILLING_ID FROM BILLING WHERE BILLING_CODE = %s", (billing_code,))
        billing_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return billing_id

    def create_billing(self,
                       billing_due, 
                       billing_total, 
                       billing_consumption, 
                       reading_id, 
                       client_id, 
                       categ_id, 
                       billing_date, 
                       billing_status, 
                       billing_amount, 
                       billing_sub_capital,
                       billing_late_payment, 
                       billing_penalty, 
                       billing_total_charge
                       ):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO BILLING (BILLING_DUE, BILLING_TOTAL, BILLING_CONSUMPTION, READING_ID, CLIENT_ID, CATEG_ID, BILLING_DATE, BILLING_CODE, BILLING_STATUS, BILLING_AMOUNT, BILLING_SUB_CAPITAL, BILLING_LATE_PAYMENT, BILLING_PENALTY, BILLING_TOTAL_CHARGE)"
            "VALUES (%s, %s, %s, %s, %s, %s,%s, LPAD(nextval('billing_code_seq')::text, 5, '0'),  %s, %s, %s, %s, %s, %s) RETURNING BILLING_ID, BILLING_CODE;",
            (          billing_due, 
                       billing_total, 
                       billing_consumption, 
                       reading_id, 
                       client_id, 
                       categ_id, 
                       billing_date,  
                       billing_status, 
                       billing_amount, 
                       billing_sub_capital,
                       billing_late_payment, 
                       billing_penalty, 
                       billing_total_charge)
        )
        new_bill_id, new_bill_code = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_bill_id, new_bill_code

    
    def get_all_billing(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.billing_code, b.issued_date, b.billing_due, c.client_name, c.client_lname, c.client_location,
                            b.billing_total, b.billing_status
                FROM BILLING b
                JOIN CLIENT c ON b.client_id = c.client_id
                ORDER BY BILLING_CODE ASC
            """)

            billings = cursor.fetchall()

            # Prepare data for the table (formatted_clients)
            formatted_clients = [
                (
                    billing_code, issued_date, billing_due, client_id, client_name, client_location, billing_total, billing_status
                )
                for billing_code, issued_date, billing_due, client_id, client_name, client_location, billing_total, billing_status in billings
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




    def update_billing(self, user_id, username, password, role):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE USER_ID = %s;", (user_id,))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE USERS SET USERNAME = %s, PASSWORD = %s, ROLE = %s WHERE USER_ID = %s;",
                (username, password, role, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False
        
    def update_status(self, billing_id, new_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE billing SET billing_status = %s WHERE billing_id = %s", (new_status, billing_id))
        conn.commit()
        cursor.close()
        conn.close()

