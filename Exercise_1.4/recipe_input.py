import pickle

# creating recipe dictionary
def take_recipe():
    name = str(input("Enter the recipe name: "))
    cooking_time = int(input("Enter the cooking time (min): "))
    ingredients = str(input("Enter ingredients, each seperated by a comma: ")).split(
        ", "
    )
    ingredients = [i.title() for i in ingredients]

    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe = {
        "name": name.capitalize(),
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty,
    }
    return recipe

# difficulty calculation based on cooking time and number of ingredients
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    if cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    if cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    if cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    return difficulty


# user enters name of file
filename = input("Enter filename to save your recipes to: ")

# open file and load, if name doesn't exist then create a new file
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")

# display this error if the file name is not found
except FileNotFoundError:
    print("No file found. - creating a new file")
    data = {"recipes_list": [], "all_ingredients": []}

# If any other errors, inform the user
except:
    print("Oops, something went wrong. Please try again")
    data = {"recipes_list": [], "all_ingredients": []}

# close the file
else:
    file.close()

# extract data into ingredient and recipe lists
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# user provides number of recipes to input
n = int(input("How many recipes would you like to enter: "))

# Add each recipe ingredients to ingredents list
for i in range(0, n):
    recipe = take_recipe()
    # checks for ingredient in ingredient list to not duplicate
    for element in recipe["ingredients"]:
        if element not in all_ingredients:
            all_ingredients.append(element)
    # adds recipe to recipe list
    recipes_list.append(recipe)
    print("Recipe added successfully!")

# Update dictionary with new data
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

# Open file and update with new data
updated_file = open(filename, "wb")
# update
pickle.dump(data, updated_file)
# close
updated_file.close()
print("Recipe file has been updated.")