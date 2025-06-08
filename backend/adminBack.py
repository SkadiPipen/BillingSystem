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


    def fetch_client_by_id(self, client_id):
        client_repository = ClientRepository()
        client = client_repository.get_client_by_id(client_id)
        self.log_action(f"Fetched client by ID: {client_id}")
        return client

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

    def get_billing_id(self, billing_code):
        billing_repository = BillingRepository()
        return billing_repository.get_billing_id(billing_code)

    def fetch_readings_by_meter_id(self, meter_id):
        reading_repository = MeterRepository()
        return reading_repository.get_readings_by_meter_id(meter_id)

    def fetch_transaction_logs(self):
        transaction_repo = TransactionRepository()
        return transaction_repo.get_all_transaction_logs()

    def fetch_system_logs(self):
        transaction_repo = TransactionRepository()
        return transaction_repo.get_all_system_logs() 

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





