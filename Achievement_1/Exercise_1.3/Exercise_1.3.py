recipes_list = []
ingredients_list = []

def take_recipe(name="No name found.", cooking_time="Unknown", ingredients="No ingredients found.", difficulty="Unknown", recipe="Recipe not found."):
    name = input("Enter the name of your recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients for your recipe (use commas to separate): ").split(", ")
    recipe = {
        "Name": name,
        "Cooking_Time": cooking_time,
        "Ingredients": ingredients,
        "Difficulty":difficulty
    }
    return recipe

n = int(input("How many recipes would you like to enter?: "))

# call the take_recipe function whichever amount of times the user entered in n

for i in range(n):
    recipe = take_recipe()
    for ingredient in ["Ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if int(recipe["Cooking_Time"]) < 10 and len(recipe["Ingredients"]) < 4:
        difficulty = "Easy"
    elif int(recipe["Cooking_Time"]) < 10 and len(recipe["Ingredients"]) >= 4:
        difficulty = "Medium"
    elif int(recipe["Cooking_Time"]) >= 10 and len(recipe["Ingredients"]) < 4:
        difficulty = "Intermediate"
    elif int(recipe["Cooking_Time"]) >= 10 and len(recipe["Ingredients"]) >= 4:
        difficulty = "Hard"

    print("==============================")
    print("Recipe: ", recipe["Name"])
    print("Cooking_Time (min): ", recipe["Cooking_Time"])
    print("Ingredients: ")
    for ingredient in recipe["Ingredients"]:
        print(ingredient)
    print("Difficulty Level: ", difficulty)


print("Ingredients Available Across All Recipes")
print("----------------------------------------")
ingredients_list = []
for recipe in recipes_list:
    for ingredient in recipe["Ingredients"]:
        ingredients_list.append(ingredient)
    sorted_ingredients = [i for i in sorted(ingredients_list)]
    for i in sorted_ingredients:
        print(i)