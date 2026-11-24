import math
import os

# კონსტანტა ფაილის სახელისთვის (სადაც შეინახება გამოთვლების ისტორია)
HISTORY_FILE = "history.txt"


def get_number(prompt):
  """
    ითხოვს მომხმარებლისგან რიცხვის შეყვანას და ამოწმებს ვალიდურობას.
    არასწორი მონაცემის (ტექსტი, სიმბოლო) შეყვანისას პროგრამა არ ითიშება.
    """
  while True:
    try:
      return float(input(prompt))
    except ValueError:
      print("\n[შეცდომა]: გთხოვთ შეიყვანოთ მხოლოდ ვალიდური რიცხვი!")


def get_operation():
  """
    აჩვენებს ხელმისაწვდომ ოპერაციებს, იღებს მომხმარებლის არჩევანს
    და ამოწმებს შეყვანილი ოპერატორის სისწორეს.
    """
  valid_ops = ["+", "-", "*", "/", "**", "%", "sqrt"]
  print("\nხელმისაწვდომი ოპერაციები:")
  print(
      "  +    (შეკრება)       |  -    (გამოკლება)   |  *  (გამრავლება)"
  )
  print(
      "  /    (გაყოფა)       |  **   (ახარისხება)  |  %  (პროცენტი)"
  )
  print("  sqrt (კვადრატული ფესვი)")

  while True:
    op = input("\nაირჩიეთ ოპერაცია: ").strip().lower()
    if op in valid_ops:
      return op
    print(f"\n[შეცდომა]: არასწორი ოპერაცია! აირჩიეთ სიიდან: {valid_ops}")


def calculate(a, b, op):
  """
    ასრულებს მათემატიკურ გამოთვლებს ლექსიკონის (dictionary) დახმარებით.
    ითვალისწინებს ნულზე გაყოფისა და უარყოფითი რიცხვიდან ფესვის შეზღუდვებს.
    """
  operations = {
      "+": lambda: a + b,
      "-": lambda: a - b,
      "*": lambda: a * b,
      "/": lambda: a / b if b != 0 else None,
      "**": lambda: a**b,
      "%": lambda: (a * b) / 100,
      "sqrt": lambda: math.sqrt(a) if a >= 0 else None,
  }
  return operations[op]()


def save_history(record):
  """ქმნის ან ხსნის ტექსტურ ფაილს და ამატებს ახალ ჩანაწერს."""
  try:
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
      file.write(record + "\n")
  except IOError as error:
    print(f"\n[ფაილის შეცდომა]: მონაცემი ვერ შეინახა ({error}).")


def view_history():
  """კითხულობს ისტორიის ფაილს და ეკრანზე გამოაქვს შენახული გამოთვლები."""
  print("\n" + "=" * 35)
  print("        გამოთვლების ისტორია")
  print("=" * 35)

  if not os.path.exists(HISTORY_FILE):
    print("ისტორია ცარიელია (ფაილი ჯერ არ შექმნილა).")
    return

  with open(HISTORY_FILE, "r", encoding="utf-8") as file:
    content = file.read().strip()
    print(content if content else "ისტორია ცარიელია.")


def delete_history():
  """შლის ისტორიის ფაილს დისკიდან."""
  if os.path.exists(HISTORY_FILE):
    os.remove(HISTORY_FILE)
    print("\n[წარმატება]: ისტორიის ფაილი სრულად წაიშალა!")
  else:
    print("\n[ინფორმაცია]: წასაშლელი ფაილი არ არსებობს.")


def handle_calculation():
  """მართავს ერთი სრული გამოთვლის პროცესს, ფორმატირებასა და შენახვას."""
  op = get_operation()

  a = get_num("\nშეიყვანეთ პირველი რიცხვი: ")
  b = 0 if op == "sqrt" else get_num("\nშეიყვანეთ მეორე რიცხვი: ")

  result = calculate(a, b, op)

  # მათემატიკური შეცდომების შემოწმება
  if result is None:
    print(
        "\n[მათემატიკური შეცდომა]: ნულზე გაყოფა ან უარყოფითი რიცხვიდან ფესვის"
        " ამოღება დაუშვებელია!"
    )
    return

  # შედეგის ფორმატირება ოპერაციის მიხედვით (:g აშორებს ზედმეტ .0-ს)
  if op == "sqrt":
    record = f"\u221a{a:g} = {result:g}"
  elif op == "%":
    record = f"{a:g}-ის {b:g}% = {result:g}"
  else:
    record = f"{a:g} {op} {b:g} = {result:g}"

  print("\n" + "-" * 35)
  print(f"შედეგი: {record}")
  print("-" * 35)

  save_history(record)


def main():
  """პროგრამის მთავარი გამშვები ციკლი და მენიუ."""
  print("=" * 45)
  print("     კონსოლ კალკულატორი (Python პროექტი)")
  print("=" * 45)

  while True:
    print("\nმთავარი მენიუ:")
    print("  1. ახალი გამოთვლა")
    print("  2. ისტორიის ნახვა")
    print("  3. ისტორიის წაშლა")
    print("  4. პროგრამიდან გასვლა")

    choice = input("\nაირჩიეთ მოქმედება (1-4): ").strip()

    if choice == "1":
      handle_calculation()
    elif choice == "2":
      view_history()
    elif choice == "3":
      delete_history()
    elif choice == "4":
      print("\nპროგრამა დასრულდა. გმადლობთ!")
      break
    else:
      print("\n[შეცდომა]: გთხოვთ აირჩიოთ ციფრი 1-დან 4-მდე!")


# პროგრამის უსაფრთხო გაშვების წერტილი
if __name__ == "__main__":
  main()
