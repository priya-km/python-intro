class ShoppingList(object):
    # Defining method
    def __init__(self, list_name):
    # initializing data attributes
        shopping_list = []
        self.list_name = list_name
        self.shopping_list = shopping_list

     # add an item to self.shopping_list   
    def add_item(self, item):
        self.item = item
    # If the item is already in the list display the first message, if not, append the item to the list and display the second message 
        if item in self.shopping_list:
            print("Item is already in the list")
        else:
            self.shopping_list.append(item)
            print("Item added to the list!")

    # remove an item from the list
    def remove_item(self, item):
        self.item = item
    # If the item is already in the list display the first message, if not, append the item to the list and display the second message 
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print("Item has been removed from the list")
        else:
            self.shopping_list.append(item)
            print("Item is not in the list")

    # view shopping list

    def view_list(self):
        print("Shopping List: ", self.list_name)
        print("--------------------")
        for item in self.shopping_list:
            print(item)
