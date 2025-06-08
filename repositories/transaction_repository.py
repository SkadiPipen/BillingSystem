import psycopg2
from database.Database import DBConnector
from datetime import date

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
                SELECT 
                    t.TRANS_CODE,            
                    t.TRANS_PAYMENT_DATE,    
                    c.CLIENT_NUMBER,         
                    c.CLIENT_NAME,           
                    t.READING_ID,            
                    b.BILLING_CONSUMPTION,   
                    b.BILLING_TOTAL,         
                    b.BILLING_DUE,           
                    t.TRANS_STATUS,          
                    r.READING_DATE           
                FROM TRANSACTIONS AS t
                JOIN CLIENT AS c ON t.CLIENT_ID = c.CLIENT_ID
                JOIN BILLING AS b ON t.BILLING_ID = b.BILLING_ID
                LEFT JOIN READING AS r ON t.READING_ID = r.READING_ID
                ORDER BY t.TRANS_ID ASC
            """)
            transactions = cursor.fetchall()

            return transactions

        except Exception as e:
            print(f"Database error: {e}")
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

    def get_transaction_id_by_billing_id(self, billing_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TRANS_ID FROM TRANSACTIONS WHERE BILLING_ID = %s", (billing_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    from datetime import date

    def update_transaction_status(self, transaction_id, new_status):
        conn = self.get_connection()
        cursor = conn.cursor()
        payment_date = date.today()
        cursor.execute("""
            UPDATE TRANSACTIONS 
            SET TRANS_STATUS = %s, TRANS_PAYMENT_DATE = %s
            WHERE TRANS_ID = %s
        """, (new_status, payment_date, transaction_id))
        conn.commit()
        conn.close()