
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
        self.cost_per_amount = cost_per_amount #i will use dollar/amount
        self.cals_per_amount = cals_per_amount
        self.sat_fat_per_amount = sat_fat_per_amount
        self.sodium_per_amount = sodium_per_amount
        self.vitc_per_amount = vitc_per_amount #vitamin c
        self.vita_per_amount = vita_per_amount #vitamin a
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
        self.amount_unit = None

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
Caloric constraint, total calories needs to be equal to CALORIE_REQ 
'''
def constraint_cal(amounts, *args):
    total_cal = 0.0
    for i in range(len(amounts)):
        total_cal = total_cal + amounts[i]*args[i]
    return (total_cal-CALORIE_REQ)

'''
Sodium constraint, SODIUM_LIM mg or less of sodium
'''
def constraint_sodium(amounts, *args):
    total_sodium = 0.0
    for i in range(len(amounts)):
        total_sodium = total_sodium + amounts[i]*args[i]
    return -(total_sodium - SODIUM_LIM) 

'''
Saturated fat constraint, SATURATED_FAT_LIM g or less of saturated fat
'''
def constraint_sat_fat(amounts, *args):
    total_sat_fat = 0.0
    for i in range(len(amounts)):
        total_sat_fat = total_sat_fat + amounts[i]*args[i]
    return -(total_sat_fat - SATURATED_FAT_LIM) 

'''
Vitamin C constraint, VITAMIN_C_MIN mg or more of Vitamin C
'''
def constraint_vitc(amounts, *args):
    total_vitc = 0.0
    for i in range(len(amounts)):
        total_vitc = total_vitc + amounts[i]*args[i]
    return (total_vitc - VITAMIN_C_MIN) 

'''
Vitamin A constraint, VITAMIN_A_MIN mcg or more of Vitamin A
'''
def constraint_vita(amounts, *args):
    total_vita = 0.0
    for i in range(len(amounts)):
        total_vita = total_vita + amounts[i]*args[i]
    return (total_vita - VITAMIN_A_MIN) 

'''
Protein constraint, PROTEIN_MIN g or more of protein
'''
def constraint_protein(amounts, *args):
    total_protein = 0.0
    for i in range(len(amounts)):
        total_protein = total_protein + amounts[i]*args[i]
    return (total_protein - PROTEIN_MIN) 


def print_amounts(food_list):
    for food in food_list:
        print('{0:5.3f} {1:s}'.format(food.amount, food.amount_unit))
    print()

def print_single_summary(food):
    print('Totals for food: {0:s}'.format(food.name))
    print('Cost: {0:6.3f} dollars'.format(food.total_cost))
    print('Calories: {0:6.3f} cal'.format(food.total_cals))
    print('Saturated fat : {0:6.3f} mg'.format(food.total_sat_fat))
    print('Sodium: {0:6.3f} mg'.format(food.total_sodium))
    print('Protein: {0:6.3f} g'.format(food.total_protein))
    print('Vitamin A: {0:6.3f} mcg'.format(food.total_vita))
    print('Vitamin C: {0:6.3f} mg'.format(food.total_vitc))
    print()

def print_summary(food_list):
    total_cost = 0
    total_cals = 0
    total_sat_fat = 0
    total_protein = 0
    total_vitc = 0
    total_vita = 0
    total_sodium = 0
    print('Daily diet:\n')
    print_amounts(food_list)
    for food in food_list:
        total_cost = total_cost + food.total_cost
        total_cals = total_cals + food.total_cals
        total_sat_fat = total_sat_fat + food.total_sat_fat
        total_protein = total_protein + food.total_protein
        total_vitc = total_vitc + food.total_vitc
        total_vita = total_vita + food.total_vita
        total_sodium = total_sodium + food.total_sodium
        print_single_summary(food)
    print('\nTotal nutrition values for this diet:\n')
    print('Cost: {0:6.3f} dollars'.format(total_cost))
    print('Calories: {0:6.3f} cal'.format(total_cals))
    print('Saturated fat : {0:6.3f} mg'.format(total_sat_fat))
    print('Sodium: {0:6.3f} mg'.format(total_sodium))
    print('Protein: {0:6.3f} g'.format(total_protein))
    print('Vitamin A: {0:6.3f} mcg'.format(total_vita))
    print('Vitamin C: {0:6.3f} mg'.format(total_vitc))


def main():
    #Initialize food items.
    #TODO: Don't hardcode these, make a .txt file that holds the data and extract it when needed

    #per 3.5oz skinless boneless chicken breast
    chicken_breast = Food(name='chicken breast', cost_per_amount=0.91, cals_per_amount=165, 
                 sat_fat_per_amount=1, vitc_per_amount=0, vita_per_amount=0,
                 protein_per_amount=34, sodium_per_amount=74)
    chicken_breast.amount_unit = '3.5oz skinless boneless chicken breast'
    #per 3/4 cup of cereal including skim milk
    lucky_charms = Food(name='lucky charms', cost_per_amount=0.27, cals_per_amount=150,
                        sat_fat_per_amount=0.0, vitc_per_amount=9, vita_per_amount=105,
                        protein_per_amount=2, sodium_per_amount=170)
    lucky_charms.amount_unit = '0.75 cups lucky charms with 0.5 cups skim milk'
    #per tortilla
    corn_tortilla = Food(name='corn tortilla', cost_per_amount=0.070, cals_per_amount=55,
                         sat_fat_per_amount=0, sodium_per_amount=5, vitc_per_amount=0,
                         vita_per_amount=0, protein_per_amount=1)
    corn_tortilla.amount_unit = 'tortilla'
    #per 100g broccoli
    broccoli = Food(name='broccoli', cost_per_amount=0.33, cals_per_amount=34,
                    sat_fat_per_amount=0, sodium_per_amount=33, vitc_per_amount=134.1,
                    vita_per_amount=84, protein_per_amount=2.8)
    broccoli.amount_unit = '100g raw broccoli'
    #per avocado
    avocado = Food(name='avocado', cost_per_amount=0.69, cals_per_amount=250,
                   sat_fat_per_amount=3, sodium_per_amount=10, vitc_per_amount=15.3,
                   vita_per_amount=70, protein_per_amount=3)
    avocado.amount_unit = 'medium sized avocado'

    food_list = [chicken_breast, lucky_charms, corn_tortilla, broccoli, avocado]

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
    guess = [1]*len(food_list)
    b = (0,None)
    bnds = (b,b,b,b,b)
    con_cal = {'type' : 'eq', 'fun' : constraint_cal, 'args' : cals}
    con_sodium = {'type' : 'ineq', 'fun' : constraint_sodium, 'args' : sodiums}
    con_sat_fat = {'type' : 'ineq', 'fun' : constraint_sat_fat, 'args' : sat_fats}
    con_vitc = {'type' : 'ineq', 'fun' : constraint_vitc, 'args' : vitcs}
    con_vita = {'type' : 'ineq', 'fun' : constraint_vita, 'args' : vitas}
    con_protein = {'type' : 'ineq', 'fun' : constraint_protein, 'args' : proteins}
    cons = (con_cal, con_sodium, con_sat_fat, con_vitc, con_vita, con_protein)
    min_object = minimize(fun=objective, x0=guess, args=(costs), constraints=cons, bounds=bnds)
    
    #grab minimized amounts, calculate totals for each item
    for food, amount in zip(food_list, min_object.x):
        food.amount = amount
        food.total_cost = food.amount*food.cost_per_amount
        food.total_cals = food.amount*food.cals_per_amount
        food.total_sat_fat = food.amount*food.sat_fat_per_amount
        food.total_protein = food.amount*food.protein_per_amount
        food.total_sodium = food.amount*food.sodium_per_amount
        food.total_vitc = food.amount*food.vitc_per_amount
        food.total_vita = food.amount*food.vita_per_amount

    print_summary(food_list)

    
if __name__ == '__main__':
    main()