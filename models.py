from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


ingredient_tags = Table(
    "ingredient_tags",
    Base.metadata,
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

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


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


# Macros are stored per 100g so recipes can scale any ingredient amount.
class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    kcal_per_100g = Column(Float)
    protein_per_100g = Column(Float)
    fat_per_100g = Column(Float)
    carbs_per_100g = Column(Float)

    tags = relationship("Tag", secondary=ingredient_tags, backref="ingredients")


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    servings = Column(Integer, default=1)
    instructions = Column(String, nullable=True)

    items = relationship("RecipeItem", back_populates="recipe", cascade="all, delete-orphan")


class RecipeItem(Base):
    __tablename__ = "recipe_items"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    grams = Column(Float)

    recipe = relationship("Recipe", back_populates="items")
    ingredient = relationship("Ingredient")



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