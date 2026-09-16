n = int(input("Enter a number: "))

for i in range(5, n + 1, 5):
    if i % 10 != 0:
        i -= i*2
        print(i)
    elif i % 10 == 0:
        print(i)