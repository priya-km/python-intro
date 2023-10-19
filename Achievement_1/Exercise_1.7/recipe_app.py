from sqlalchemy import create_engine

# Connecting to database
engine = create_engine("mysql://cf-python:password@localhost/my_database")

# Import declarative_base and generate class so they can be inherited
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy.orm import sessionmaker

# Generate session class
Session = sessionmaker(bind=engine)

session = Session()

# Import Column and data types
from sqlalchemy import Column

from sqlalchemy.types import Integer, String


# Inherit base and create recipe table
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Quick recipe representation
    def __repr__(self):
        return (
            "<Recipe ID/Name: "
            + str(self.id)
            + "-"
            + self.name
            + "Diff: "
            + self.difficulty
            + ">"
        )

    # Print full recipe
    def __str__(self):
        list_ingredients = self.ingredients.split(", ")
        output = (
            "-" * 50
            + f"\n"
            + f"\nRecipe name: {self.name}"
            + f"\nCooking Time: {self.cooking_time} minutes"
            + f"\nDifficulty: {self.difficulty}"
            + "\nIngredients: \n"
        )
        for ingredient in list_ingredients:
            output += f"\t- {ingredient}\n"
        output
        return output

    # Calculate recipe difficulty
    def calculate_difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = "Easy"
        if self.cooking_time < 10 and len(ingredients) >= 4:
            self.difficulty = "Medium"
        if self.cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = "Intermediate"
        if self.cooking_time >= 10 and len(ingredients) >= 4:
            self.difficulty = "Hard"

    # Retrieve ingredients as a list
    def return_ingredients_as_list(self):
        # If no ingredients return empty list
        if len(self.ingredients == 0):
            return []
        # Split ingredients into a list with a comma and space in between ingredients
        else:
            return self.ingredients.split(", ")


# Create_all method used to create tables of all defined models
Base.metadata.create_all(engine)


def create_recipe():
    try:
        # Recipe name
        name = str(input("\nEnter recipe name: ")).title()
        # Validate length of name
        while len(name) > 50:
            print("\n\t*Error: Name must be 50 characters or less*")
            name = str(input("\nEnter recipe name: "))

        # Cooking time
        cooking_time = input("\nEnter cooking time (in mintues): ")
        # Validate user has inputted a number
        while not cooking_time.isnumeric():
            print("\n\t*Error: Cooking must be a numeric value")
            cooking_time = input("\nEnter cooking time (in mintues): ")
        # Convert input to integer
        cooking_time = int(cooking_time)

        # Number of Ingredients
        ingredients = []
        num = input("\nEnter the number of ingredients in the recipe: ")
        # Validate user has inputted a number
        while not num.isnumeric():
            print("\n\t*Error: number of ingredients must be a numeric value")
            num = input("\nEnter the number of ingredients in the recipe: ")
        # Convert entry to integer
        num = int(num)
        # Run for loop to get ingredients from user
        for ingredient in range(num):
            ingredient = str(input("\nEnter ingredient: ")).capitalize()
            # Validate user has inputted a string
            while not any(c for c in ingredient if c.isalpha() or c.isspace()):
                print(
                    "\n\t*Error: Ingredients can only contain alphabetic characters or spaces"
                )
                ingredient = str(input("\nEnter ingredient: ")).capitalize()
            ingredients.append(ingredient)
        # Convert list into comma seperated string
        ingredients = ", ".join(ingredients)

        recipe_entry = Recipe(
            name=name, cooking_time=cooking_time, ingredients=ingredients
        )

        recipe_entry.calculate_difficulty()
        # Add new recipe to database
        session.add(recipe_entry)
        # Commit changes
        session.commit()
        # Success message
        print()
        print("\n\tRecipe added successfully!")
        print()
        main_menu()

    # Error handling
    except Exception as e:
        print("\nThere was an error creating the recipe...")
        print(e)
        print()
        main_menu()


def view_all_recipes():
    # Query database for all recipes
    recipes_list = session.query(Recipe).all()
    # if no recipes exist then inform the user
    if len(recipes_list) == 0:
        print("\n\tLooks like there are no recipes on the list...")
        print("\n\tBetter add some!")
        main_menu()
    # Print all recipes
    else:
        print()
        print("*" * 6 + "All recipes in databse" + "*" * 6)
        for recipe in recipes_list:
            print(recipe)
        main_menu()


def search_by_ingredients():
    # Query database to count number of stored recipes
    recipe_count = session.query(Recipe).count()
    # If no recipes in database alert user
    if recipe_count == 0:
        print("\n\tLooks like there are no recipes on the list...")
        print("\n\tBetter add some!")
        print()
        main_menu()
    # Query database for all ingredient rows
    results = session.query(Recipe.ingredients).all()
    # Initialize empty ingredients list
    all_ingredients = []
    # Loop to populate ingredient list
    for result in results:
        # Split strings received from database
        temp_list = result[0].split(", ")
        # Add ingredients to main list
        for item in temp_list:
            if item not in all_ingredients:
                all_ingredients.append(item)

    # Add numbers to all ingredients list starting at index 1
    lst = enumerate(all_ingredients, 1)
    # Turn into a list
    numbered_lst = list(lst)
    # Provide list to user
    print("\nAll Ingredients in database: ")
    # Loop numbered list and print all elements
    for ingredient in numbered_lst:
        print(f"\n\t{ingredient[0]} {ingredient[1]}")
    # Empty options list
    options = []

    for item in numbered_lst:
        num = item[0]
        options.append(num)
    # Ask user to select ingredients they would like to search
    selected = input(
        "\nEnter number assigned to each ingredient you want to search (seperated by spaces): "
    ).split()

    search_ingredients = []
    for i in selected:
        # Error handling
        if not i.isnumeric() or int(i) not in options:
            print("\n\t*Error: Only numeric values that match an ingredient accepted.")
            print("\n\tPlease try again.")
            return None
        # Populate search ingredients list with names of ingredients
        else:
            i = int(i)
            ingredient = numbered_lst[i - 1][1]
            search_ingredients.append(ingredient)

    condition_list = []
    # Loop search ingredients to populate condition list
    for ingredient in search_ingredients:
        like_term = str(f"%{ingredient}%")
        condition_list.append(Recipe.ingredients.like(like_term))
    # Query db for ingredients that match user input
    matching_recipes = session.query(Recipe).filter(*condition_list).all()
    # Inform user if no matches
    if len(matching_recipes) == 0:
        print("\n\tOh no, looks like no recipes matched your search. :(")
        main_menu()
    # Show user recipes with specified ingredients
    else:
        print("\nMatching Recipes: ")
        print()

        for recipe in matching_recipes:
            print(recipe)
        print()
        main_menu()


def edit_recipe():
    # Query database to count number of stored recipes
    recipe_count = session.query(Recipe).count()
    # If no recipes in database then alert user
    if recipe_count == 0:
        print("\n\tLooks like there are no recipes on the list...")
        print("\n\tBetter add some!")
        print()
        main_menu()
    # Get all recipes from database
    results = session.query(Recipe.id, Recipe.name).all()
    options = []
    print("\nAll Recipes in database:")
    # Display all recipes and their index ID numbers
    for result in results:
        print(f"\n\tID: {result[0]} - {result[1]}")
        # Populate options list with ID of all recipes
        options.append(result[0])
    # Collect ID of choosen recipe from user
    choosen = input("\nEnter the ID of the recipe you'd like to edit: ")
    # Validate entry is numeric
    while not choosen.isnumeric():
        print("\n\t*Error: ID must be a numeric value")
        choosen = input("\nEnter the ID of the recipe you'd like to edit: ")
    # Convert user input into integer
    choosen = int(choosen)
    # Confirm entry in options list
    if choosen not in options:
        print("\n\tOh no, looks like there was no recipe that matched this ID. :(")
        print("\n\tYou'll have to try again.")
        main_menu()
    # Query databade for recipe to be edited
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == choosen).one()
    print()
    print("-" * 70)
    # Show recipe to be edited
    print("\nRecipe that will be edited: ")
    print(f"\n\t1.  Name: {recipe_to_edit.name}")
    print(f"\n\t2.  Cooking Time: {recipe_to_edit.cooking_time}")
    print(f"\n\t3.  Ingredients: {recipe_to_edit.ingredients}")
    print()
    print("-" * 70)
    # Create list of options user can select to edit
    edit_options = [1, 2, 3]
    # Have user determine what row they would like to edit
    row_to_edit = input(
        "\nEnter the number matching the recipe attribute you'd like to edit: "
    )
    # Confirm user input is numeric
    while not row_to_edit.isnumeric():
        print("\n\t*Error: Choice must be a numeric value")
        row_to_edit = input(
            "\nEnter the number matching the recipe attribute you'd like to edit: "
        )
    # Convert input to integer
    row_to_edit = int(row_to_edit)
    # Validate input is in options list
    if row_to_edit not in edit_options:
        print(
            "\n\tOh no, looks like there was no attribute that matched your choice. :("
        )
        print("\n\tYou'll have to try again.")
        main_menu()
    # Editing name row
    if row_to_edit == 1:
        print()
        print("-" * 50)
        print(f"\nUpdating name of {recipe_to_edit.name}")
        print()
        print("-" * 50)
        # Collect new name
        new_name = str(input("\nEnter the new name: ")).title()
        #  Validate number of characters
        while len(new_name) > 50:
            print("\n\t*Error: Name must be 50 characters or less*")
            new_name = str(input("\nEnter the new name: "))
        # Update recipe name in database
        try:
            session.query(Recipe).filter(Recipe.id == choosen).update(
                {Recipe.name: new_name}
            )
            # Commit changes
            session.commit()
            # Success message
            print()
            print("\n\tRecipe updated successfully!")
            print()
            main_menu()

        # Error handling
        except Exception as e:
            print("\nThere was an error updating the recipe...")
            print(e)
            print()
            main_menu()
    # Edit cooking time
    elif row_to_edit == 2:
        print()
        print("-" * 50)
        print(f"\nUpdating the cooking time of {recipe_to_edit.name}")
        print()
        print("-" * 50)
        # Get new cooking time from user
        new_time = input("\nEnter cooking time (in mintues): ")
        # Validate user input is numeric
        while not new_time.isnumeric():
            print("\n\t*Error: Cooking must be a numeric value")
            new_time = input("\nEnter cooking time (in mintues): ")
        # Convert cooking time to integer
        new_time = int(new_time)
        try:
            # Re-calculate difficulty of edited recipe as a new recipe
            recipe_update = Recipe(
                name=recipe_to_edit.name,
                cooking_time=new_time,
                ingredients=recipe_to_edit.ingredients,
            )
            recipe_update.calculate_difficulty()
            session.query(Recipe).filter(Recipe.id == choosen).update(
                {
                    Recipe.cooking_time: new_time,
                    Recipe.difficulty: recipe_update.difficulty,
                }
            )
            # Commit changes
            session.commit()
            # Success message
            print()
            print("\n\tRecipe updated successfully!")
            print()
            main_menu()

        # Error handling
        except Exception as e:
            print("\nThere was an error updating the recipe...")
            print(e)
            print()
            main_menu()
    # Editing ingredients
    else:
        print()
        print("-" * 50)
        print(f"\nUpdating the ingredients of {recipe_to_edit.name}")
        print(
            "\n\tNOTE: ALL current ingredients will be replaced by the NEW entries!"
        )
        print()
        print("-" * 50)
        new_ingredients = []
        # Get number of new ingredients from user
        num = input("\nEnter the number of ingredients in the recipe: ")
        # Validate entry is numeric
        while not num.isnumeric():
            print("\n\t*Error: number of ingredients must be a numeric value")
            num = input("\nEnter the number of ingredients in the recipe: ")
        # Convert entry to integer
        num = int(num)
        try:
            # Run for loop to get ingredients from user
            for ingredient in range(num):
                ingredient = str(input("\nEnter ingredient: ")).capitalize()
                # Validate user entry is alphabetical
                while not any(c for c in ingredient if c.isalpha() or c.isspace()):
                    print(
                        "\n\t*Error: Ingredients can only contain alphabetic characters or spaces"
                    )
                    ingredient = str(input("\nEnter ingredient: ")).capitalize()
                # Add ingredient to new list
                new_ingredients.append(ingredient)
            # Convert list into comma seperated string
            new_ingredients = ", ".join(new_ingredients)
            # Re-calculate difficulty with new amount of ingredients
            recipe_update = Recipe(
                name=recipe_to_edit.name,
                cooking_time=recipe_to_edit.cooking_time,
                ingredients=new_ingredients,
            )
            recipe_update.calculate_difficulty()
            # Update recipe and new difficulty
            session.query(Recipe).filter(Recipe.id == choosen).update(
                {
                    Recipe.ingredients: new_ingredients,
                    Recipe.difficulty: recipe_update.difficulty,
                }
            )
            # Commit changes
            session.commit()
            # Success message
            print()
            print("\n\tRecipe updated successfully!")
            print()
            main_menu()
        # Error handling
        except Exception as e:
            print("\nThere was an error updating the recipe...")
            print(e)
            print()
            main_menu()


def delete_recipe():
    # Query database to count number of recipes
    recipe_count = session.query(Recipe).count()
    # If no recipes in database alert user
    if recipe_count == 0:
        print("\n\tLooks like there are no recipes on the list...")
        print("\n\tBetter add some!")
        print()
        main_menu()
    # Get all recipes
    results = session.query(Recipe.id, Recipe.name).all()
    options = []
    print("\nAll Recipes in database:")
    # Loop to print all recipes with ID
    for result in results:
        print(f"\n\tID: {result[0]} - {result[1]}")
        options.append(result[0])
    # Prompt user to input desired ID
    choosen = input("\nEnter the ID of the recipe you'd like to delete: ")
    # Validate user input is numeric
    while not choosen.isnumeric():
        print("\n\t*Error: ID must be a numeric value")
        choosen = input("\nEnter the ID of the recipe you'd like to edit: ")
    # Convert input into integer
    choosen = int(choosen)
    # Confirm input matches a displayed recipe
    if choosen not in options:
        print("\n\tOh no, looks like there was no recipe that matched this ID. :(")
        print("\n\tYou'll have to try again.")
        main_menu()
    # Query DB for recipe to be deleted
    to_delete = session.query(Recipe).filter(Recipe.id == choosen).one()
    print("\nAre you sure you'd like to delete the following recipe: ")
    print()
    print(to_delete)
    print("-" * 50)
    # Confirm deletion
    confirmation = str(input("\nEnter 'yes' to delete or 'no' to cancel: ")).lower()
    # Validate that input is either yes or no
    while (not confirmation == "yes") and (not confirmation == "no"):
        print("\n\t*Error - only 'yes' or 'no' are acceptable entries*")
        confirmation = str(input("\nEnter 'yes' to delete or 'no' to cancel: ")).lower()
    # If no answer just return to main menu
    if confirmation == "no":
        print("\n\tClose call...")
        print("\n\t...but nothing was deleted. Phew!")
        main_menu()
    # Delete recipe and return to main menu for yes answer
    else:
        try:
            session.delete(to_delete)
            session.commit()
            print()
            print("\n\tRecipe has been successfully deleted.")
            print()
            main_menu()
        # Error handling
        except Exception as e:
            print("\nThere was an error deleting the recipe...")
            print(e)
            print()
            main_menu()

# MAIN MENU

def main_menu():
    choice = ""
    print()
    print("-" * 50)
    print("\nWelcome to the Recipe App Main Menu!")
    print("\nWhat would you like to do? Pick a choice: ")
    print("\n\t1. Create a Recipe")
    print("\n\t2.  View all Recipes")
    print("\n\t3. Search for a Recipe")
    print("\n\t4. Edit a Recipe")
    print("\n\t5. Delete a Recipe")
    print("\n   Type 'quit' to close application")
    print()
    print("-" * 50)
    # Prompt user to enter choice
    choice = str(input("\nWhat would you like to do? "))
    # While loop to keep menu appearing unless choice is quit
    while choice != "quit":
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        else:
            print(
                "\n\tOh no, looks like there is no option that matches that choice. :("
            )
            print("\n\tYou'll have to try again.")
            main_menu()
    #  Close app
    print("\n\tGoodbye")
    session.close()
    engine.dispose()
    exit()


# Start App wth main menu function
main_menu()