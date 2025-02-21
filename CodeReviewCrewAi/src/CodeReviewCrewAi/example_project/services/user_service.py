from models.user import User

class UserService:
    def __init__(self):
        self.users = []

    def add_user(self, user: User):
        self.users.append(user)

    def get_all_users(self):
        return [user.get_user_info() for user in self.users]

    # TODO