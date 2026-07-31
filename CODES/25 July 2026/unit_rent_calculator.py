u = int(input("Enter Electrical Units used: "))

cost_unit = u*10

if (u<= 100):
    amount = cost_unit + 100
    
elif (u > 100 and u <= 200):
    amount = cost_unit + 200
    
else:
    amount = cost_unit + 300
    
print(f"The Total Rent is {amount}.")