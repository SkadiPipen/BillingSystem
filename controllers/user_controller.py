from repositories.user_repository import UserRepository

class UserController:
    def __init__(self):
        self.user_repo = UserRepository()

    def get_meter_by_id(self, user_id):
        return self.user_repo.get_user_by_id(user_id)

    def check_user(self, username, password):
        return self.user_repo.check_user(username, password)
    
    def get_all_users(self):
        return self.user_repo.get_all_users()

    def create_user(self, id, name, username):
        return self.user_repo.create_user(id, name, username)

    def update_user(self, user_id, username, password, role):
        return self.user_repo.update_user(user_id, username, password, role)

    def delete_user(self, user_id):
        return self.user_repo.delete_user(user_id)
