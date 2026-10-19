total = 0
count = 0
min_val = None
max_val = None


while True:
    user_input = input("შეიყვანეთ რიცხვი ან 'stop': \n")
    if user_input.strip() == "stop":
        break
    
    try:
        number = float(user_input)
        total += number
        count +=1
        if min_val is None or number < min_val:
            min_val = number
        if max_val is None or number > max_val:
            max_val = number
    except ValueError: 
        print("გთხოვთ შეიყვანოთ მხოლოდ რიცხვი ან ' stop'")
        
print(f"შეყვანილი ვალიდური რიცხვების ჯამი (total): {total}")
print(f"შეყვანილი რიცხვების რაოდენობა: {count}")

if count > 0:
    print(f"მინიმალური რიცხვი (min): {min_val}")
    print(f"მაქსიმალური რიცხვი (max): {max_val}")
else:
    print("ვალიდური რიცხვი არ ყოფილა შეყვანილი.")