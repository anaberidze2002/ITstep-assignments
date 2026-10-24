inventory = {
    "leptop": {"price": 2500, "stock": 5, "year": 2023},
    "smartphone": {"price": 1200, "stock": 10, "year": 2024},
    "headphones": {"price": 150, "stock": 0, "year": 2022},
    "smartwatch": {"price": 350, "stock": 3, "year": 2023}
}
print("არსებული ინვენტარი ")
for name, details in inventory.items():
    print(f". {name}: {details}")
print()
print("ახალი პროდუქტის დამატება / განახლება")
new_product_name = input("შეიყვანეთ პროდუქტის სახელი:\n").lower().strip()
while True:
 try:
  new_product_price = int(input("შეიყვანეთ პროდუქტის ფასი:\n"))
  new_product_stock = int(input("შეიყვანეთ პროდუქტის რაოდენობა:\n"))
  new_product_year = int(input("შეიყვანეთ პროდუქტის გამოშვების წელი:\n"))

  if new_product_name in inventory:
    inventory[new_product_name]["stock"] += new_product_stock
    inventory[new_product_name]["price"] = new_product_price
    print(f"პროდუქტი '{new_product_name}' უკვე არსებობს, მარაგი შეივსო და გახდა: {inventory[new_product_name]['stock']}")
  else:
    inventory[new_product_name] = {
        "price": new_product_price,
        "stock": new_product_stock,
        "year": new_product_year
    }
    print(f"ბაზაში წარმატებით დაემატა ახალი პროდუქტი: '{new_product_name}'")
  break
 except ValueError:
   print("შეიყვანეთ მხოლოდ რიცხვი")
    
active_users = {"giga@example.com", "anna@example.com", "luka@example.com", "nino@example.com"}
vip_users = {"anna@example.com", "nino@example.com", "saba@example.com", "giorgi@exaample.com"}

all_unique_users = active_users.union(vip_users)
active_vip_users = active_users.intersection(vip_users)
active_non_vip = active_users.difference(vip_users)

available_poducts = {}
for name, details in inventory.items():
    if details["stock"] > 0:
        available_poducts[name] = details
        
expensive_product_name = None
max_price = -1

for name, details in inventory.items():
    if details["price"] > max_price:
        max_price = details["price"]
        expensive_product_name = name

print("განახლებული ინვენტარის სრული სია:")
total_inventory_value = 0

for name, details in inventory.items():
    print(f"  {name.capitalize()}: ფასი = {details['price']} ლარი, რაოდენობა = {details['stock']}, გამოშვების წელი = {details['year']}")
    total_inventory_value += details["price"] * details["stock"]
    
print(f"ინვენტარის ჯამური ღირებულება: {total_inventory_value} ლარი")
print()
print("ხელმისაწვდომი პროდუქტები (მარაგშია):")
for name in available_poducts:
    print(f"- {name}")

print(f"ყველაზე ძვირადღირებული პროდუქტი: {expensive_product_name} ({max_price} ლარი)")
 
print()
print("მომხმარებელთა ანალიტიკა")
print(f"ყველა უნიკალური მომხმარებელი:\n {all_unique_users}")
print(f"აქტიური VIP მომხმარებლები:\n {active_vip_users}")
print(f"აქტიური მომხმარებლები VIP სტატუსის გარეშე:\n {active_non_vip}")
    