first_name = input("შეიყვანეთ თქვენი სახელი\n")
print("სახელი: ",first_name.upper())
last_name = input("შეიყვანეთ თქვენ გვარი\n")
print("გვარი: ", last_name.upper())

birth_year = int(input("შეიყვანეთ თქვენი დაბადების წელი\n"))
print("დაბადების წელი: ", birth_year)
fav_language = input("შეიყვანეთ თქვენი საყვარელი პროგრამირების ენა\n")
print("საყვარელი პროგრამირების ენა: ", fav_language)


age = 2026-birth_year 
print("ასაკი:", age)

is_adult = age >= 18
print("სრულწლოვანი:", is_adult)

print(first_name.upper(), last_name.upper(), age, fav_language.upper(), is_adult, sep=" | ")

student_score = float(input("შეიყვანეთ მოსწავლის ქულა (მაქსიმუმ 20 ქულა)\n"))
student_final_score = int(student_score // 2)
print("მოსწავლის ნიშანი 10-ბალიანი სისტემით: ", student_final_score)