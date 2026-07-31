cost_price = int(input("Enter the cost of the bike: "))

if (cost_price < 50000):
    tax = cost_price*0.05
    
elif (cost_price >= 50000 and cost_price <= 100000):
    tax = cost_price*0.10
    
else:
    tax = cost_price*0.15
    
print(f"The Tax is {tax}")