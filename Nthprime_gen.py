def prime_numbers():
    num = 2
    while True:
        prime = [i for i in range(2, num) if num % i == 0]
        if not prime:
            yield num
        num += 1
        
gen = prime_numbers()
for p in range(10):
 print(next(gen))