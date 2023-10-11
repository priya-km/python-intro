import pickle


def display_recipe(recipe):
    print("")
    print("Recipe: ", recipe["name"])
    print("Cooking Time (mins): ", recipe["cooking_time"])
    print("Ingredients: ")
    for element in recipe["ingredients"]:
        print("- ", element)
    print("Difficulty: ", recipe["difficulty"])
    print("")


# Function to search ingredients
def search_ingredients(data):
    # Add number to each element in list
    lst = enumerate(data["all_ingredients"])
    # Structure data into a list
    numbered_lst = list(lst)
    print("Ingredients List: ")
    # Prints number and ingredient name for each element in list

    for ele in numbered_lst:
        print(ele[0], ele[1])
    try:
        num = int(input("Enter the number for the ingredients you would like to search: "))
        ingredient_searched = numbered_lst[num][1]
        print("Searching for...", ingredient_searched, "...")
    # if user enters string not number
    except ValueError:
        print("Only Intergers accepted")
    # other input error
    except:
        print(
            "Oops, your input didn't match the allowed options. Make sure you choose a number that matches an ingredient on the list"
        )
    else:
        # Loops through recipe list to check ingredients, prints recipe if ingredient included
        for element in data["recipes_list"]:
            if ingredient_searched in element["ingredients"]:
                print(element)



filename = input("Enter file name of where your recipes are: ")
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")
# if file not found then inform the user
except FileNotFoundError:
    print("No files match that name - please try again")
# if any other error, inform the user
except:
    print("Oops, there was an unexpected error")
else:
    file.close()
    search_ingredients(data)