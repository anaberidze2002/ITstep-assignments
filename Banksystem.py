from functools import wraps

SYSTEM_ACTIVE = True
GLOBAL_AUDIT_LOG = []

def audit_system(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if SYSTEM_ACTIVE:
            GLOBAL_AUDIT_LOG.append(f"გამოძახებულია ფუნქცია: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def create_account_generator(initial_balance):
    balance = initial_balance
    transaction_id = 0
    
    @audit_system
    def transaction_generator():
        nonlocal balance, transaction_id
        amount = yield(transaction_id, balance)
        while True:
            if amount is not None:
                transaction_id += 1
                balance += amount
            amount = yield(transaction_id, balance)
    gen = transaction_generator()
    next(gen)  
    return gen

account = create_account_generator(1000)
initial_id, initial_balance = account.send(None)
print(f"საწყისი ბალანსი: {initial_balance}")

trans_id, current_balance = account.send(1500)
print(f"ტრანზაქცია {trans_id}: ბალანსი შევსებულია, მიმდინარე ნაშთი = {current_balance}")

trans_id, current_balance = account.send(-700)
print(f"ტრანზაქცია {trans_id}: თანხა გატანილია, მიმდინარე ნაშთი = {current_balance}")


    