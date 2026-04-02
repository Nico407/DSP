class UserProfile:
    def __init__(self, 
                 name, 
                 sex, 
                 height, 
                 weight, 
                 age, 
                 activity_level):
        self.name = name
        self. sex = sex.lower()                 # 'male' or 'female'
        self.height = height                    # in cm
        self.weight = weight                    # in kg
        self.age = age                          # in years
        self.activity_level = activity_level    # in Level

    def __repr__(self):
        return f"<UserProfile(name={self.name}, weight={self.weight}kg)>"