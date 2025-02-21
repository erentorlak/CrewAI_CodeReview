class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name

    def get_user_info(self):
        return f"User[ID: {self.user_id}, Name: {self.name}]"