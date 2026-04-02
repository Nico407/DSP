# Basal Metabolic Rate (BMR)

def calculate_bmr(user):
    if user.sex == 'male':
        sex_adjustment = 5
    else:
        sex_adjustment = -161
 
    bmr = (10 * user.weight) + (6.25 * user.height) - (5 * user.age) + sex_adjustment

    return bmr

# Total Daily Energy Expenditure (TDEE)

def calculate_tdee(user):
    activity_map = {
        "1"     : 1.2,      #sedentary
        "2"     : 1.375,    #light
        "3"     : 1.55,     #moderate
        "4"     : 1.725,    #active
        "5"     : 1.9       #extreme
    }

    #if wrong/unexpected answer is inserted, instead of crashing the base multiplier of 1.2 is chosen
    multiplier = activity_map.get(str(user.activity_level), 1.2)
    bmr = calculate_bmr(user)
    tdee = bmr * multiplier
    return tdee 

###
# gain          +500
# mild gain     +250
# maintain      2600
# mild loss     -250
# loss          -500
###

goal_settings = {
    "1": {"kcal_adjustment": 500,   "protein_base": 1.8, "fat_multiplier": 1.1},    #strong gain
    "2": {"kcal_adjustment": 250,   "protein_base": 1.6, "fat_multiplier": 1.0},    #mild gain
    "3": {"kcal_adjustment": 0,     "protein_base": 1.0, "fat_multiplier": 0.9},    #maintain
    "4": {"kcal_adjustment": -250,  "protein_base": 1.4, "fat_multiplier": 0.8},    #mild loss
    "5": {"kcal_adjustment": -500,  "protein_base": 1.6, "fat_multiplier": 0.7}     #strong loss
}

def calculate_macros(user, tdee, goal_choice):
    config = goal_settings.get(goal_choice, goal_settings["3"]) #default set to maintain

    #age adjustment (Anabolic Resistance)
    protein_multiplier = config["protein_base"]
    if user.age >= 50:
        protein_multiplier += 0.3
    elif user.age >= 40:
        protein_multiplier += 0.2
    
    target_kcal = tdee + config["kcal_adjustment"]

    #fixed protein and fat calculations
    protein_gram = user.weight * protein_multiplier
    fat_gram = user.weight * config["fat_multiplier"]

    #calculating remaining kcal as carbs
    protein_kcal = protein_gram * 4
    fat_kcal = fat_gram * 9

    remaining_kcal = target_kcal - (protein_kcal + fat_kcal)
    carbs_gram = max(0, remaining_kcal / 4)

    return {
        "daily_kcal":   round(target_kcal),
        "protein":      round(protein_gram),
        "fat":          round(fat_gram),
        "carbs":        round(carbs_gram),
        "p_multiplier_used":  round(protein_multiplier, 1)
    }

