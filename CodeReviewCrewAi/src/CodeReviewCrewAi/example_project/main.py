from models.user import User
from models.product import Product
from services.user_service import UserService
from services.product_service import ProductService

if __name__ == "__main__":
    user_service = UserService()
    product_service = ProductService()

    user_service.add_user(User(1, "Alice"))
    user_service.add_user(User(2, "Bob"))
    
    product_service.add_product(Product(101, "Laptop", 1200.00))
    product_service.add_product(Product(102, "Phone", 800.00))

    print("Users:", user_service.get_all_users())
    print("Products:", product_service.get_all_products())

    print("User by ID:", user_service.get_user_by_id(1))
    print("User by ID:", user_service.get_user_by_id(2))