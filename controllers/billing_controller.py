from repositories.billing_repository import BillingRepository

class BillingController:
    def __init__(self):
        self.billing_repo = BillingRepository()

    def get_all_billing(self):
        return self.billing_repo.get_all_billing()

    def create_billing(self, billing_code, issued_date, billing_due, client_id, client_name, client_location, billing_total, billing_status):
        return self.billing_repo.create_billing(billing_code, issued_date, billing_due, client_id, client_name, client_location, billing_total, billing_status)

    def get_billing_by_id(self, billing_id):
        return self.billing_repo.get_billing_by_id(billing_id)
    