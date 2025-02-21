from models.product import Product

class ProductService:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def get_all_products(self):
        return {product.get_product_info() for product in self.products}  