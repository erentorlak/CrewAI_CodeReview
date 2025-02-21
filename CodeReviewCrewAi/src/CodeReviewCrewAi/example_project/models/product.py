class Product:
    def __init__(product_id: int, name: str, price: float):  # Defect: missing 'self'
        self.product_id = product_id
        self.name = name
        self.price = price

    def get_product_info(self):
        return f"Product[ID: {self.product_id}, Name: {self.name}, Price: ${self.price}]"