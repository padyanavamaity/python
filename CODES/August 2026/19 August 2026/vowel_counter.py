string = input("Enter a string: ")
count = 0
for i in string:
    if i.lower() in 'aeiou':
        count += 1
print(f"The number of vowels in the string is: {count}")