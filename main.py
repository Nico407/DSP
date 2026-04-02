from models import UserProfile
from calculations import calculate_bmr, calculate_tdee, calculate_macros

def get_user_input():
    print("=== testing macro calculator ===")

    #basic info
    name = input("Enter your name: ")
    sex = input("Sex (male/female): ").strip().lower()

    #numeric inputs
    try:
        height = float(input("Height (cm): "))
        weight = float(input("Weight (kg): "))
        age = int(input("Age (years): "))
    except ValueError:
        print("Error: Please enter numbers for height, weight and age.")
        return None
    
    #Activity Level Menu
    print("\n--- Activity Level ---")
    print("1 = Sedentary    | Office job, little exercise")
    print("2 = Light        | Excercise 1-3 days/week")
    print("3 Moderate       | Excercise 3-5 days/week")
    print("4 Active         | Excercise 5+ days/week")
    print("5 Extreme        | Physcial Job + Exercising")
    activity_choice = input("Select Level 1-5:")

    #Goal Menu
    print("\n--- Your Goal ---")
    print("1. Strong Gain (+0.5kg/week)")
    print("2. Mild Gain   (+0.25kg/week)")
    print("3. Maintain")
    print("4. Mild Loss   (-0.25kg/week)")
    print("5. Strong Loss (-0.5kg/week)")
    goal_choice = input("Select 1-5: ")

    user = UserProfile(name, sex, height, weight, age, activity_choice)

    return user, goal_choice

########################################


def main():
    data = get_user_input()
    
    if data:
        user, goal_choice = data
        
        # 1. Calculate TDEE
        # Note: calculate_tdee calls calculate_bmr internally
        tdee = calculate_tdee(user)
        
        # 2. Calculate Macros
        results = calculate_macros(user, tdee, goal_choice)
        
        # 3. Display Results
        print("\n" + "="*30)
        print(f" RESULTS FOR: {user.name.upper()} ")
        print("="*30)
        print(f"Maintenance (TDEE): {round(tdee)} kcal")
        print(f"Target Intake:     {results['daily_kcal']} kcal")
        print("-" * 30)
        print(f"PROTEIN: {results['protein']}g  ({results['p_multiplier_used']}g/kg)")
        print(f"FATS:    {results['fat']}g")
        print(f"CARBS:   {results['carbs']}g")
        print("="*30)

if __name__ == "__main__":
    main()