from repositories.client_repository import ClientRepository

class EmployeePageBack:
    def fetch_customers(self, user_type):
        client_repository = ClientRepository()
        return client_repository.get_all_clients(user_type)

