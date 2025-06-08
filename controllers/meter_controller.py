from repositories.meter_repository import MeterRepository

class MeterController:
    def __init__(self):
        self.meter_repo = MeterRepository()

    def get_all_meter(self):
        return self.meter_repo.get_all_meter()
    
    def get_meter_by_id(self, meter_id):
        return self.meter_repo.get_meter_by_id(meter_id)

    def create_meter(self, meter_last_reading, meter_last_reading_date, serial_number):
        return self.meter_repo.create_meter(meter_last_reading, meter_last_reading_date, serial_number)
