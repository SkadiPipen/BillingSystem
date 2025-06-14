from repositories.client_repository import ClientRepository
from repositories.user_repository import UserRepository
from repositories.billing_repository import BillingRepository
from repositories.address_repository import AddressRepository
from repositories.category_repository import CategoryRepository
from repositories.meter_repository import MeterRepository
from repositories.reading_repository import ReadingRepository
from repositories.transaction_repository import TransactionRepository
from repositories.rateblock_repository import RateBlockRepository
import psycopg2
from datetime import datetime
from database.Database import DBConnector


class adminPageBack:
    def __init__(self, user_name="System"):
        self.user_name = user_name

    def log_action(self, message):
        try:
            db = DBConnector()
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO system_logs (message, user_name, timestamp)
                VALUES (%s, %s, %s)
            """, (message, self.user_name, datetime.now()))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Logging error: {e}")

    def fetch_clients(self):
        client_repository = ClientRepository()
        return client_repository.get_all_clients()

    def fetch_users(self):
        user_repository = UserRepository()
        return user_repository.get_all_employee()

    def fetch_user_by_id(self, user_id):
        user_repository = UserRepository()
        user = user_repository.get_user_by_id(user_id)
        self.log_action(f"Fetched user by ID: {user_id}")
        return user

    def fetch_billing(self):
        billing_repository = BillingRepository()
        return  billing_repository.get_all_billing()


    def add_billing(self, billing_due, billing_total, billing_consumption, reading_id, client_id, categ_id,
                    billing_date, billing_status, billing_amount, billing_sub_capital, billing_late_payment,
                    billing_penalty, billing_total_charge):
        billing_repository = BillingRepository()
        result = billing_repository.create_billing(billing_due, billing_total, billing_consumption, reading_id,
                                                   client_id, categ_id, billing_date, billing_status,
                                                   billing_amount, billing_sub_capital, billing_late_payment,
                                                   billing_penalty, billing_total_charge)
        self.log_action(f"Added billing for client ID: {client_id}")
        return result
    
    def update_billing_status(self, billing_id, new_status):
        billing_repo = BillingRepository()
        return billing_repo.update_status(billing_id, new_status)
    
    def add_transaction(self, billing_id, trans_status, trans_payment_date, trans_total_amount, client_id, reading_id):
        transaction_repo = TransactionRepository()
        return transaction_repo.create_transaction(billing_id, trans_status, trans_payment_date, trans_total_amount, client_id, reading_id)


    def fetch_client_by_id(self, client_id):
        client_repository = ClientRepository()
        client = client_repository.get_client_by_id(client_id)
        self.log_action(f"Fetched client by ID: {client_id}")
        return client
    
    def update_reading(self, reading_id, reading_date, reading_current):
        reading_repo = ReadingRepository()
        return reading_repo.update_reading(reading_id, reading_date, reading_current)

    def get_meter_id_by_reading_id(self, reading_id):
        meter_repo = MeterRepository()
        return meter_repo.get_meter_id_by_reading_id(reading_id)

    def add_client(self, client_name, client_lname, client_contact_num, client_location, meter_id,
                   address_id, categ_id, client_mname, status):
        client_repository = ClientRepository()
        result = client_repository.create_client(client_name, client_lname, client_contact_num, client_location,
                                                 meter_id, address_id, categ_id, client_mname, status)
        self.log_action(f"Added new client: {client_name} {client_lname}")
        return result

    def fetch_categories(self):
        category_repository = CategoryRepository()
        return category_repository.get_category()

    def get_category_by_id(self, id):
        category_repository = CategoryRepository()
        return category_repository.get_category_by_id(id)

    def toggle_category_status(self, id, status):
        category_repository = CategoryRepository()
        result = category_repository.toggle_status_category(id, status)
        if result:
            self.log_action(f"Toggled category status: ID={id}, Status={status}")
        return result

    def fetch_address(self):
        address_repository = AddressRepository()
        return address_repository.get_address()

    def get_address_by_id(self, id):
        address_repository = AddressRepository()
        return address_repository.get_address_by_id(id)

    def toggle_address_status(self, address_id, new_status):
        address_repo = AddressRepository()
        result = address_repo.toggle_status(address_id, new_status)
        if result:
            self.log_action(f"Changed address ID {address_id} to status {new_status}")
        return result



    def add_reading(self, read_date, prev_read, pres_read, meter_id):
        reading_repository = ReadingRepository()
        result = reading_repository.create_reading(read_date, prev_read, pres_read, meter_id)
        self.log_action(f"Added new reading for meter ID: {meter_id}")
        return result
    
    def get_transaction_id_by_billing_id(self, billing_id):
        transaction_repo = TransactionRepository()
        return transaction_repo.get_transaction_id_by_billing_id(billing_id)
    
    def update_transaction_status(self, transaction_id, new_status):
        transaction_repo = TransactionRepository()
        return transaction_repo.update_transaction_status(transaction_id, new_status)

    def add_meter(self, meter_last_reading, serial_number):
        meter_repository = MeterRepository()
        result = meter_repository.create_meter(meter_last_reading, serial_number)
        self.log_action(f"Added new meter: SN={serial_number}")
        return result

    def fetch_meter_by_id(self, meter_id):
        meter_repository = MeterRepository()
        meter = meter_repository.get_meter_by_id(meter_id)
        self.log_action(f"Fetched meter by ID: {meter_id}")
        return meter

    def update_meter_latest_reading(self, pres_read, read_date, meter_id):
        meter_repository = MeterRepository()
        return meter_repository.update_meter_latest_reading(pres_read, read_date, meter_id)
    
    def fetch_rate_blocks_by_categ(self, categ_id):
        rateblock_repo = RateBlockRepository()
        return rateblock_repo.get_rate_block_by_category(categ_id)

    def fetch_transactions(self):
        transactions_repository = TransactionRepository()
        return transactions_repository.get_all_transaction()

    def update_client(self, client_id, fname, lname, contact, location, mname):
        client_repository = ClientRepository()
        result = client_repository.update_client(client_id, fname, lname, contact, location, mname)
        self.log_action(f"Updated client: ID={client_id}")
        return result

    def update_client_status(self, client_id, new_status):
        client_repository = ClientRepository()
        result = client_repository.update_client_status(client_id, new_status)
        if result:
            self.log_action(f"Updated client status: ID={client_id}, Status={new_status}")
        return result

    def fetch_meters(self):
        meter_repository = MeterRepository()
        return meter_repository.get_all_meters()

    def update_meter(self, meter_id, serial_number, meter_code, last_read):
        meter_repository = MeterRepository()
        result = meter_repository.update_meter(meter_id, serial_number, meter_code, last_read)
        self.log_action(f"Updated meter: ID={meter_id}")
        return result

    def get_meter_by_id(self, meter_id):
        meter_repository = MeterRepository()
        return meter_repository.get_meter_by_id(meter_id)

    def get_bill_data_by_code(self, billing_id):
        billing_repository = BillingRepository()
        return billing_repository.get_bill_data(billing_id)

    def fetch_meter_previous_reading(self, meter_id):
        meter_repository = MeterRepository()
        return meter_repository.get_meter_previous_reading(meter_id)

    def get_reading_by_id(self, reading_id):
        reading_repository = ReadingRepository()
        result = reading_repository.get_reading_by_id(reading_id)
        return result[0] if result else None  # return (reading_prev, reading_current)

    def get_prev_current_by_id(self, reading_id):
        reading_repository = ReadingRepository()
        return reading_repository.get_reading_by_id(reading_id)  # DO NOT do result[0]
    
    def get_reading_info_by_id(self, reading_id):
        reading_repo = ReadingRepository()
        return reading_repo.get_reading_info_by_id(reading_id)

    def get_billing_id(self, billing_code):
        billing_repository = BillingRepository()
        return billing_repository.get_billing_id(billing_code)
    
    def get_billing_by_id(self, billing_id):
        billing_repository = BillingRepository()
        return billing_repository.get_billing_by_id(billing_id)

    def fetch_readings_by_meter_id(self, meter_id):
        reading_repository = MeterRepository()
        return reading_repository.get_readings_by_meter_id(meter_id)

    def fetch_transaction_logs(self):
        transaction_repo = TransactionRepository()
        return transaction_repo.get_all_transaction_logs()

    def fetch_system_logs(self):
        transaction_repo = TransactionRepository()
        return transaction_repo.get_all_system_logs() 
    
    def update_billing_issued_date(self, billing_id, issued_date):
        billing_repo = BillingRepository()
        return billing_repo.update_billing_issued_date(billing_id, issued_date)
    
    def edit_billing(self, billing_id, billing_total, billing_due, sub_capital, late_payment, penalty, total_charge, billing_amount, billing_consumption, billing_date):
        billing_repo = BillingRepository()
        return billing_repo.edit_billing(billing_id, billing_total, billing_due, sub_capital, late_payment, penalty, total_charge, billing_amount, billing_consumption, billing_date)


    def insert_rate_block(self, is_minimum, min_con, max_con, rate, categ_id):
        rateblock_repo = RateBlockRepository()
        return rateblock_repo.insert_rate_block(is_minimum, min_con, max_con, rate, categ_id)

    def update_rate_block(self, block_id, is_minimum, min_con, max_con, rate):
        rateblock_repo = RateBlockRepository()
        result = rateblock_repo.update_rate_block(block_id, is_minimum, min_con, max_con, rate)
        if result:
            self.log_action(f"Updated rate block ID {block_id}: "
                            f"{'Fixed' if is_minimum else 'Per Cubic Meter'} rate = {rate}, "
                            f"Range = {min_con} to {max_con if max_con is not None else '+'}")
        return result

    def delete_rate_block(self, block_id):
        rateblock_repo = RateBlockRepository()
        return rateblock_repo.delete_rate_block(block_id)

    def replace_meter(self, old_meter_id, new_serial_number, initial_reading):
        meter_repository = MeterRepository()
        success = meter_repository.replace_meter(old_meter_id, new_serial_number, initial_reading)
        if success:
            self.log_action(f"Replaced meter ID {old_meter_id} with new serial '{new_serial_number}'")
        return success

    def serial_exists(self, serial_number):
        meter_repo = MeterRepository()
        return meter_repo.serial_exists(serial_number)
    
    def void_reading(self, reading_id):
        reading_repo = ReadingRepository()
        return reading_repo.void_reading(reading_id)

    def get_reading_id_by_billing_id(self, billing_id):
        reading_repo = ReadingRepository()
        return reading_repo.get_reading_id_by_billing_id(billing_id)


    def mark_transaction_paid(self, transaction_id, payment_date):
        transaction_repo = TransactionRepository()
        return transaction_repo.mark_transaction_paid(transaction_id, payment_date)
    
    def get_reading_by_current_and_meter(self, current_val, meter_id):
        reading_repo = ReadingRepository()
        return reading_repo.get_reading_by_current_and_meter(current_val, meter_id)


    def mark_bill_paid(self, billing_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE billing SET billing_status='PAID' WHERE billing_id=%s", (billing_id,))
        cursor.execute("UPDATE transactions SET trans_status='PAID', trans_payment_date=NOW() WHERE billing_id=%s", (billing_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def void_billing(self, billing_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE billing SET billing_status='VOID' WHERE billing_id=%s", (billing_id,))
        cursor.execute("UPDATE transactions SET trans_status='VOID' WHERE billing_id=%s", (billing_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def reissue_billing(self, original_billing_id, updated_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE billing SET billing_status='VOID' WHERE billing_id=%s", (original_billing_id,))
        cursor.execute("UPDATE transactions SET trans_status='VOID' WHERE billing_id=%s", (original_billing_id,))

        cursor.execute("""
            INSERT INTO billing (billing_due, billing_total, billing_status)
            VALUES (%s, %s, 'ISSUED')
            RETURNING billing_id
        """, (updated_data["billing_due"], updated_data["billing_total"]))
        new_billing_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO transactions (billing_id, trans_status, trans_total_amount)
            VALUES (%s, 'PENDING', %s)
        """, (new_billing_id, updated_data["billing_total"]))

        cursor.execute("""
            INSERT INTO billing_history (original_billing_id, new_billing_id)
            VALUES (%s, %s)
        """, (original_billing_id, new_billing_id))

        conn.commit()
        cursor.close()
        conn.close()

    def fetch_active_clients(self):
        """
        Fetches all active clients from the database.
        Returns a list of tuples with selected fields.
        """
        try:
            db = DBConnector()
            conn = db.get_connection()
            cursor = conn.cursor()

            query = """
                    SELECT c.CLIENT_ID, \
                           c.CLIENT_NUMBER, \
                           c.CLIENT_NAME, \
                           c.CLIENT_MNAME, \
                           c.CLIENT_LNAME, \
                           c.CLIENT_STATUS, \
                           m.METER_ID, \
                           c.CATEG_ID
                    FROM CLIENT c
                             LEFT JOIN METER m ON c.METER_ID = m.METER_ID
                    WHERE c.CLIENT_STATUS = 'Active'
                    ORDER BY c.CLIENT_LNAME ASC, c.CLIENT_NAME ASC \
                    """

            cursor.execute(query)
            result = cursor.fetchall()
            return result

        except Exception as e:
            print("Error fetching active clients:", str(e))
            return []

        finally:
            if conn:
                cursor.close()
                conn.close()    

    def delete_billing(self, billing_code):
        conn = None
        try:
            db = DBConnector()
            conn = db.get_connection()
            cursor = conn.cursor()

            # Get billing ID from code
            cursor.execute("SELECT billing_id FROM billing WHERE billing_code = %s", (billing_code,))
            result = cursor.fetchone()
            if not result:
                raise Exception(f"No billing found with code {billing_code}")
            billing_id = result[0]

            # Get associated reading_id
            cursor.execute("SELECT reading_id FROM billing WHERE billing_id = %s", (billing_id,))
            reading_result = cursor.fetchone()
            if not reading_result:
                raise Exception(f"No reading found linked to billing ID {billing_id}")
            reading_id = reading_result[0]

            # Get reading details before deletion
            cursor.execute("""
                           SELECT meter_id, reading_prev, reading_current, reading_date
                           FROM reading
                           WHERE reading_id = %s
                           """, (reading_id,))
            reading_info = cursor.fetchone()
            if not reading_info:
                raise Exception(f"Reading data missing for ID {reading_id}")
            meter_id, prev_reading, current_reading, reading_date = reading_info

            # Delete billing and reading records
            cursor.execute("DELETE FROM billing WHERE billing_id = %s", (billing_id,))
            cursor.execute("DELETE FROM reading WHERE reading_id = %s", (reading_id,))

            # Find latest non-deleted reading
            cursor.execute("""
                           SELECT reading_current, reading_date
                           FROM reading
                           WHERE meter_id = %s
                             AND reading_date < %s
                           ORDER BY reading_date DESC LIMIT 1
                           """, (meter_id, reading_date))
            last_reading = cursor.fetchone()

            # Determine fallback values
            if last_reading:
                last_value, last_date = last_reading
            else:
                last_value = prev_reading
                last_date = reading_date

            # Update meter with previous reading
            cursor.execute("""
                           UPDATE meter
                           SET meter_last_reading      = %s,
                               meter_last_reading_date = %s
                           WHERE meter_id = %s
                           """, (last_value, last_date, meter_id))

            conn.commit()
            print(f"[SUCCESS] Billing {billing_code} deleted successfully.")

        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Failed to delete billing: {str(e)}")
            raise Exception(f"Failed to delete billing: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def fetch_billing_to_issue(self):
        try:
            db = DBConnector()
            conn = db.get_connection()
            cursor = conn.cursor()

            query = """
                    SELECT b.billing_code, b.billing_due, c.client_name
                    FROM billing b
                             JOIN client c ON b.client_id = c.client_id
                    WHERE b.billing_status = 'PRINTED' \
                    """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error fetching billings for issuing:", str(e))
            return []
        finally:
            if conn:
                conn.close()

    def fetch_billing_pending_payment(self):
        try:
            db = DBConnector()
            conn = db.get_connection()
            cursor = conn.cursor()

            query = """
                    SELECT b.billing_code, b.issued_date, c.client_name
                    FROM billing b
                             JOIN client c ON b.client_id = c.client_id
                    WHERE b.billing_status = 'PENDING PAYMENT' \
                    """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error fetching pending payments:", str(e))
            return []
        finally:
            if conn:
                conn.close()

    def fetch_transaction(self):
        try:
            db = DBConnector()
            conn = db.get_connection()
            cursor = conn.cursor()
            query = """
                    SELECT t.TRANS_CODE, 
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
                    """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    
    
