principal = int(input("Enter the amount being invested: "))
rate = float(input("Enter the rate of interest: "))
time = int(input("Enter the time of investment (in Years): "))

interest = (principal*rate*time)/100

print(f"The Interest is {interest}")