
import numpy as np
from scipy.optimize import minimize 

CALORIE_REQ = 2000     #calories
SATURATED_FAT_LIM = 20 #grams
SODIUM_LIM = 2400      #milligrams
VITAMIN_C_MIN = 90     #milligrams
VITAMIN_A_MIN = 700    #micrograms
PROTEIN_MIN = 56       #grams

'''
Some amount of a food item. All quantities with 'per_amount' suffix must 
have units consistent with amount units. For example 400gil/ounce and 20 
ounces are compatible.

amount: is a variable of the optimization problem
cost_per_amount: Ex: 400 munny/item, 100gil/pound
calories_per_amount: Ex: 350cal/kg 
'''
class Food:
    def __init__(self, name, cost_per_amount, cals_per_amount, sat_fat_per_amount, 
                 sodium_per_amount, vitc_per_amount, vita_per_amount, protein_per_amount):
        #provided attributes
        self.cost_per_amount = cost_per_amount
        self.cals_per_amount = cals_per_amount
        self.sat_fat_per_amount = sat_fat_per_amount
        self.sodium_per_amount = sodium_per_amount
        self.vitc_per_amount = vitc_per_amount #vitamin c
        self.vita_per_amount = vitc_per_amount #vitamin a
        self.protein_per_amount = protein_per_amount
        self.name = name
        #derived/default attributes
        self.amount = 0.0
        self.total_cost = self.cost_per_amount*self.amount
        self.total_cals = self.cals_per_amount*self.amount
        self.total_sat_fat = self.sat_fat_per_amount*self.amount
        self.total_sodium = self.sodium_per_amount*self.amount
        self.total_vitc = self.vitc_per_amount*self.amount
        self.total_vita = self.vita_per_amount*self.amount
        self.total_protein = self.protein_per_amount*self.amount

'''
Objective function to be minimized
amounts: list of item amounts
*args: list of costs associated with items
'''
def objective(amounts, *args):
    total_cost = 0.0
    for i in range(len(amounts)):
        total_cost = total_cost + amounts[i]*args[0][i]
    return total_cost

#TODO: Make a general linear constraint function
'''
Caloric constraint, total calories needs to be at 2000 
'''
def constraint_cal(amounts, *args):
    total_cal = 0.0
    for i in range(len(amounts)):
        total_cal = total_cal + amounts[i]*args[i]
    return (total_cal-CALORIE_REQ)

'''
Sodium constraint, 2400mg or less of sodium
'''
def constraint_sodium(amounts, *args):
    total_sodium = 0.0
    for i in range(len(amounts)):
        total_sodium = total_sodium + amounts[i]*args[i]
    return -(total_sodium - SODIUM_LIM) 

'''
Saturated fat constraint, 20g or less of saturated fat
'''
def constraint_sat_fat(amounts, *args):
    total_sat_fat = 0.0
    for i in range(len(amounts)):
        total_sat_fat = total_sat_fat + amounts[i]*args[i]
    return -(total_sat_fat - SATURATED_FAT_LIM) 

'''
Vitamin C constraint, 90mg or more of Vitamin C
'''
def constraint_vitc(amounts, *args):
    total_vitc = 0.0
    for i in range(len(amounts)):
        total_vitc = total_vitc + amounts[i]*args[i]
    return (total_vitc - VITAMIN_C_MIN) 

'''
Vitamin A constraint, 700mcg or more of Vitamin A
'''
def constraint_vita(amounts, *args):
    total_vita = 0.0
    for i in range(len(amounts)):
        total_vita = total_vita + amounts[i]*args[i]
    return (total_vita - VITAMIN_A_MIN) 

'''
Protein constraint, 56g or more of protein
'''
def constraint_protein(amounts, *args):
    total_protein = 0.0
    for i in range(len(amounts)):
        total_protein = total_protein + amounts[i]*args[i]
    return (total_protein - PROTEIN_MIN) 

def main():
    #Initialize food items.
    #TODO: Don't hardcode these, make .txt files that hold the info
    food_list = []
    food0 = Food(name='test_food_0', cost_per_amount=2.5, cals_per_amount=350, 
                 sat_fat_per_amount=3, vitc_per_amount=50, vita_per_amount=50,
                 protein_per_amount=10, sodium_per_amount=100)
    food1 = Food(name='test_food_1', cost_per_amount=3.3, cals_per_amount=100,
                 sat_fat_per_amount=0.1, vitc_per_amount=100, vita_per_amount=100,
                 protein_per_amount=10, sodium_per_amount=200)
    food_list.append(food0)
    food_list.append(food1)

    #Get food properties in lists
    costs = []
    cals = []
    sat_fats = []
    sodiums = []
    vitcs = []
    vitas = []
    proteins = []
    
    for food in food_list:
        costs.append(food.cost_per_amount)
        cals.append(food.cals_per_amount)
        sat_fats.append(food.sat_fat_per_amount)
        sodiums.append(food.sodium_per_amount)
        vitcs.append(food.vitc_per_amount)
        vitas.append(food.vita_per_amount)
        proteins.append(food.protein_per_amount)

    #set up and execute minmization
    guess = [0,0]
    b = (0,None)
    bnds = (b,b)
    con_cal = {'type' : 'eq', 'fun' : constraint_cal, 'args' : cals}
    con_sodium = {'type' : 'ineq', 'fun' : constraint_sodium, 'args' : sodiums}
    con_sat_fat = {'type' : 'ineq', 'fun' : constraint_sat_fat, 'args' : sat_fats}
    con_vitc = {'type' : 'ineq', 'fun' : constraint_vitc, 'args' : vitcs}
    con_vita = {'type' : 'ineq', 'fun' : constraint_vita, 'args' : vitas}
    con_protein = {'type' : 'ineq', 'fun' : constraint_protein, 'args' : proteins}
    cons = (con_cal, con_sodium, con_sat_fat, con_vitc, con_vita, con_protein)
    min_object = minimize(fun=objective, x0=guess, args=(costs), constraints=cons, bounds=bnds)
    
    #grab minimized amounts, calculate total cals/costs for each food item
    print(min_object.x)
    for food, amount in zip(food_list, min_object.x):
        food.amount = amount
        food.total_cost = food.amount*food.cost_per_amount
        food.total_cals = food.amount*food.cals_per_amount

    
if __name__ == '__main__':
    main()