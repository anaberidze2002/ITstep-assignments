class Product:
    store_name = "Techshop Georgia"
    currency = "GEL"
    total_products = 0
    
    def __init__(self, name: str,  price: float, stock: int, category: str, discount: float = 0):
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.discount = discount
        
        Product.total_products += 1
    
    def get_info(self):
        return f"პროდუქტი: {self.name}, ფასი: {self.price} {Product.currency}, მარაგშია: {self.stock}, კატეგორია: {self.category}, ფასდაკლება: {self.discount}%"
    
    def apply_discount(self, percent):
        self.discount = percent
        print(f"პროდუქტზე '{self.name}' დაწესდა {percent}%-იანი ფასდაკლება.")
    
    def update_stock(self, amount: int):
        if self.stock + amount < 0:
            print(f"მარაგის {amount}-ით შეცვლა შეუძლებელია! არასაკმარისი რაოდენობა.")
        else:
            self.stock += amount
            
    def calculate_final_price(self):
        final_price = self.price - (self.price * self.discount / 100)
        return final_price
    
    @classmethod
    def get_total_products_count(cls):
        return cls.total_products
    
p1 = Product("Smartphone X", 1200, 15, "Electronics")
p2 = Product("Wireless Headphones", 250, 30, "Electronics", discount = 10)
p3 = Product("Running Shoes", 180, 8, "Sportswear")

print(p1.get_info())
p1.apply_discount(15)
print(f"საბოლოო ფასი ფასდაკლებით: {p1.calculate_final_price()} {Product.currency}\n")

p3.update_stock(5)
p3.update_stock(-2)

print(f"სულ შექმნილი პროდუცტები: {Product.get_total_products_count()}")