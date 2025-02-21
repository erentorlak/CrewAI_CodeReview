```python
# File: example_project\\services\\user_service.py
from models.user import User

class UserService:
    def __init__(self):
        """Initialize UserService with an empty dictionary for users."""
        self.users = {}  # Using a dictionary to maintain unique user entries by ID

    def add_user(self, user: User):
        """Add a User instance to the service.
        
        Args:
            user (User): The User instance to be added.
        
        Raises:
            ValueError: If user is not an instance of User or if user with the same ID already exists.
        """
        if not isinstance(user, User):
            raise ValueError("Expected an instance of User")

        if user.user_id in self.users:
            raise ValueError(f"User with ID {user.user_id} already exists.")

        self.users[user.user_id] = user

    def get_all_users(self):
        """Retrieve all users in the service.

        Returns:
            list: A list of user information strings.
        """
        return [user.get_user_info() for user in self.users.values()]

    def get_user_by_id(self, user_id: int):
        """Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The User instance associated with the given ID.

        Raises:
            KeyError: If no user with the given ID exists.
        """
        if user_id not in self.users:
            raise KeyError(f"No user found with ID {user_id}.")
        
        return self.users[user_id]
```
This completes the `user_service.py` file with improved functionalities, including type checks, duplicate entry prevention, efficient user retrieval, and added documentation for clarity. The new structure using a dictionary enhances overall performance, and the error handling ensures robustness against common issues.