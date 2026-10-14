cart_total = float(input("შეიყვანეთ კალათის ღირებულება ლარებში: "))
user_status = input("შეიყვანეთ სტატუსი (regular, vip, admin): ").strip().lower()
has_promo_code = input("აქვს პრომოკოდი? (true/false): ").strip().lower() == "true"
loyalty_points = int(input("შეიყვანეთ დაგროვილი ქულები: "))
delivery_city = input("შეიყვანიეთ მიტანის ქალაქი: ").strip()
is_account_active = input("აქტიურია ანგარიში? (true/false): ").strip().lower() == "true"

if not is_account_active:
    print("ანგარიში დაბლოკილია. შეკვეთა ვერ დამუშავდება.")
    exit()
    

if cart_total == 0:
    print("შეკვეთა არ გატარდა, კალათა ცარიელია.")
    exit()
if cart_total <= 0:
    print("შეცდომა: კალათა ცარიელია ან მინუსშია.")
    exit()

discount_percentage = 0
initial_cart_total = cart_total

if user_status == "vip":
    discount_percentage = 20
    if loyalty_points >= 500:
        discount_percentage += 5
elif user_status == "regular":
    if has_promo_code or cart_total >= 150:
        discount_percentage = 10
    else:
        discount_percentage = 0
elif user_status == "admin":
    discount_percentage = 50

discount_amount = initial_cart_total * (discount_percentage /100)
discounted_cart_total = initial_cart_total - discount_amount

if delivery_city in ["თბილისი", "ქუთაისი", "ბათუმი"]:
     if discounted_cart_total >= 100:
         delivery_cost = 0
     else:
         delivery_cost = 5
else:
     delivery_cost = 15
     
final_total_price = discounted_cart_total + delivery_cost

print("\n--- დეტალური ინვოისი ---")
print(f"კალათის საწყისი ფასი: {initial_cart_total:.1f} ლარი")
print(f"მიღებული ფასდაკლების პროცენტი: {discount_percentage}%")
print(f"ფასდაკლებული კალათის ფასი: {discounted_cart_total:.1f} ლარი")
print(f"მიტანის საფასური: {delivery_cost} ლარი")
print(f"საბოლოო გადასახდელი თანხა: {final_total_price:.1f} ლარი")
        