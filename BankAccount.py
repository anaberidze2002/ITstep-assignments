class BankAccount:
    bank_name = "BOG"
    
    def __init__(self, cardtype, owner, balance):
        self.cardtype = cardtype
        self.owner = owner
        self.__balance = balance
        
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"ანგარიშზე დაემატა {amount} ლარი. მიმდინარე ბალანსი: {self.__balance}")
        else:
            print("შეიყვანეთ დადებითი რიცხვი")
            
    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print(f"ანგარიშიდან მოიხსნა {amount} ლარი. მიმდინარე ბალანსი: {self.__balance}")
        else:
            print("საკმარისი თანხა არ არის ანგარიშზე.")
            
            
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self.__balance = amount
        else:
            raise ValueError("შეიყვანეთ დადებითი რიცხვი")
    
    @balance.deleter
    def balance(self):
        print("ბალანსის ჩანაწერი წაიშალა.")
        del self.__balance
    
    @classmethod
    def return_bank_name(cls):
        return cls.bank_name
        
    @staticmethod
    def calculate_tax(amount, tax_rate = 0.05):
        return amount * tax_rate
        

class SavingsAccount(BankAccount):
    def __init__(self, cardtype, owner, balance, interest_rate = 0.05):
        super().__init__(cardtype, owner, balance)
        self.interest_rate = interest_rate
        
    def apply_interest(self):
        interest = self.balance * self.interest_rate
        print(f"დაირიცხა სარგებელი({self.interest_rate * 100}%): {interest} ლარი.")
        self.deposit(interest)
  
    def withdraw(self, amount):
        commission = 2
        total_deduction = amount + commission
        if amount <= 0:
            print("შეიყვანეთ დადებითი თანხა.")
        elif total_deduction <= self.balance:
            self.balance  -=total_deduction
            print(f"მოიხსნა {amount} ლარი (საკომისიო: {commission} ლარი). მიმდინარე ბალანსი: {self.balance}")
        else:
            print("არ არის საკმარისი თანხა.")
            
class CreditAccount(BankAccount):
    def __init__(self, cardtype, owner, balance, credit_limit = 2000):
        super().__init__(cardtype, owner, balance)
        self.credit_limit = credit_limit
        
    def withdraw(self, amount):
        if self.balance - amount >= -self.credit_limit:
            self._BankAccount__balance -= amount
            print(f"საკრედიტო ანგარიშიდან მოიხსნა {amount} ლარი. მიმდინარე ბალანსი: {self.balance}")
        else:
            print("ოპერაცია უარყოფილია: გადაჭარბებულია საკრედიტო ლიმიტი.")
            
b1 = BankAccount("Visa", "John Doe", 1000)
b1.deposit(500)
b1.withdraw(200)

s1 = SavingsAccount("Visa", "John Doe", b1.balance, interest_rate=0.05)
s1.apply_interest()
s1.withdraw(100)

c1 = CreditAccount("Visa", "John Doe", s1.balance, credit_limit=2000)
c1.withdraw(1400)

print("ბანკის სახელი:", BankAccount.return_bank_name())
print("გადასახადი 500 ლარზე:", BankAccount.calculate_tax(500))
            