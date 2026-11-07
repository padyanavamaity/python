a = input("Enter a sentence: ")
count = 0

for i in a:
    if (i in ' '):
        count += 1
print(f"The number of words in the sentence is: {count + 1}")