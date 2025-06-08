from repositories.client_repository import ClientRepository

class ClientController:
    def __init__(self):
        self.client_repo = ClientRepository()

    def get_client_by_id(self, client_id):
        return self.client_repo.get_client_by_id(client_id)

    def get_all_clients(self):
        return self.client_repo.get_all_clients()

    def create_client(self, client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status):
        return self.client_repo.create_client(client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status)

    def update_client(self, client_id, client_name, client_mname,  client_lname, contact_num, payment_id, address_id, categ_id, meter_id):
        return self.client_repo.update_client(client_id, client_name, client_mname, client_lname, contact_num, payment_id, address_id, categ_id, meter_id)

    def delete_client(self, client_id):
        return self.client_repo.delete_client(client_id)