a = int(input("Enter a number: "))

prime = 0

for i in range(2, a):
    if (a % i == 0):
        prime = 1
        break
if prime == 1:
    print(f"{a} is not a prime number.")
else:
    print(f"{a} is a prime number.")