a = input("Enter a string: ")
b = input("Enter a character: ")
count = 0

for i in a:
    if (i == b):
        count += 1

print(f"The number of occurrences of '{b}' in the string is: {count}")