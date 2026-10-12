first_name = input("შეიყვანეთ თქვენი სახელი\n")
last_name = input("შეიყვანეთ თქვენი გვარი\n")
platform = input("აირჩიეთ პლათფორმა(მაგალითად: gmail.com, itstep.ge, yahoo.com)\n")

clean_first_name = first_name.replace(" ", "")
clean_last_name = last_name.replace(" ", "")
first_two_chars = clean_first_name[0:2]

email= f"{first_two_chars}{clean_last_name}@{platform}".lower()
print(email)
print(f"გენერირებული ელფოსტა: {email}\n\n თქვენი ელფოსტა წარმატებით შეიქმნა!")

