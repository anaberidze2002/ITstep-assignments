import re

user_input = input("შეიყვანეთ ტექსტი (მაგ:მინდა 2 ბილეთი, გადავიხადე 40 ლარი ):\n ")

try:
    numbers = re.findall(r'\d+\.\d+|\d+', user_input)
    tickets_count = int(numbers[0])
    paid_amount = float(numbers[1])
    total_cost = tickets_count * 15
    
    if tickets_count <= 0:
        raise ValueError("ბილეთების რაოდენობა უნდა იყოს მინიმუმ 1")
    if paid_amount < total_cost:
        raise ValueError("თანხა არ არის საკმარისი")

except IndexError:
    print("შეცდომა: ტექსტში ვერ მოიძებნა საჭირო რაოდენობის რიცხვები (ბილეთები ან თანხა).")
except ValueError as e:
    print(f"შეცდომა: {e}")

else:
    change = paid_amount - total_cost
    print("ჯავშანი წარმატებით დასრულდა!")
    print(f"თქვენ შეიძინეთ {tickets_count} ბილეთი. გადახდილი თანხა: {paid_amount:.1f} ლარი.")
    print(f"თქვენ გეკუთვნით ხურდა: {change:.2f} ლარი")
    
finally:
    print("[სისტემა]: ტრანზაქციის მცდელობა დასრულდა")
    