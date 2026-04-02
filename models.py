from sqlalchemy import Column, Integer, String, Float
from database import Base

#Database Table
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    sex = Column(String)
    height = Column(Float)
    weight = Column(Float)
    age = Column(Integer)
    activity_level = Column(String)
    goal_choice = Column(String)

    daily_kcal = Column(Integer)
    protein = Column(Integer)
    fat = Column(Integer)
    carbs = Column(Integer)

    

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