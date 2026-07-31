a = int(input("Enter a number: "))

b = a % 10

if (b % 3 == 0):
    print("Yes the last digit is divisible by 3")
    
else:
    print("No the last digit is not divisible by 3")