a = input("Enter a string: ")
n = ' '

for i in a:
    if (i == ' '):
        n += '-'
        
    else:
        n += i

print(f"The string after replacing spaces with hyphens is: {n}")