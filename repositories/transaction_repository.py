import psycopg2
from database.Database import DBConnector

class TransactionRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()
    
    def get_transaction_by_id(self, trans_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM TRANSACTIONS WHERE TRANS_ID = %s;",
            (trans_id,)
        )
        transaction = cursor.fetchall()
        cursor.close()
        conn.close()
        return transaction


    def get_all_transaction(self): 
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.TRANS_CODE, t.TRANS_PAYMENT_DATE, c.CLIENT_NUMBER, c.CLIENT_NAME, u.USER_NAME,
                    b.BILLING_CONSUMPTION, b.BILLING_TOTAL, b.BILLING_DUE, t.TRANS_STATUS
                FROM TRANSACTIONS as t
                JOIN CLIENT as c ON t.CLIENT_ID = c.CLIENT_ID
                JOIN BILLING as b ON t.BILLING_ID = b.BILLING_ID
                JOIN USERS as u ON t.user_id = u.user_id
                ORDER BY TRANS_ID ASC
            """)
            transactions = cursor.fetchall()

            formatted_transactions = [
                (
                    trans_code, trans_payment_date, client_number, client_name, user_name, billing_consumption, billing_total, billing_due, trans_status
                )
                for  trans_code, trans_payment_date, client_number, client_name, user_name, billing_consumption, billing_total, billing_due, trans_status in transactions
            ]

            return formatted_transactions

        except Exception as e:
            print(f"Database error: {e}")
            return []

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()



    def create_transaction(self, billing_id, trans_status, trans_payment_date, trans_total_amount, payment_id, client_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO TRANSACTIONS (
                BILLING_ID, TRANS_STATUS, TRANS_PAYMENT_DATE, TRANS_TOTAL_AMOUNT,
                PAYMENT_ID, TRANS_CODE, CLIENT_ID, USER_ID
            ) VALUES (
                %s, %s, %s, %s, %s,
                'TR-' || LPAD(nextval('trans_id_seq')::text, 5, '0'), %s, %s       
            )
            RETURNING TRANS_ID;
        """, (
            billing_id, trans_status, trans_payment_date, trans_total_amount, payment_id, client_id, user_id 
        ))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    def get_all_transaction_logs(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT log_id, transaction_id, action, timestamp, user_name, old_status, new_status
                           FROM transaction_logs
                           ORDER BY timestamp DESC
                           """)
            logs = cursor.fetchall()
            return logs
        except Exception as e:
            print(f"Error fetching transaction logs: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_all_system_logs(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT log_id, message, timestamp, user_name
                           FROM system_logs
                           ORDER BY timestamp DESC
                           """)
            logs = cursor.fetchall()
            return logs
        except Exception as e:
            print(f"Error fetching system logs: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
