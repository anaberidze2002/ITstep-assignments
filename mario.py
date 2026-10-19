print("გთხოვთ შეიყვანო პირამიდის სიმაღლე (მთელი რიცხვი 1-დან 8-ს ჩათვლით)")

while True:
    try:
        height = int(input())
        if 1 <= height <= 8:
            break
        else:
            print("გთხოვთ შეიყვანოთ რიცხვი 1-დან 8-ის ჩათვლით.")
    except ValueError:
        print("შეცდომა! გთხოვთ შეიყვანოთ მთელი რიცხვი.")
        
for i in range(1, height + 1):
    for j in range(height - i):
        print(" ", end="")
    for k in range(i):
        print("#", end="")
    print()