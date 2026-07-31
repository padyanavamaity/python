a = int(input("Enter 1st Number: "))
b = int(input("Enter 2nd Number: "))
c = int(input("Enter 3rd Number: "))

if (a>b and a>c):
    print(f"{a} is Greatest.")
    
elif (b>a and b>c):
    print(f"{b} is Greatest.")
    
else:
    print(f"{c} is Greatest.")