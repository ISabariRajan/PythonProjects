from MenuItems import MenuItems as item
class Restaurant:
    
    name = ""
    dishes = []
    
    def __init__(self, name, dishes):
        self.name = name
        self.dishes = dishes
    
    def add_dish_collection(self, collection):
        self.dishes.extend(collection)
    
    def add_single_dish(self, dish):
        self.dishes.append(self)
    
    
    def __str__(self):
        return "Name: " + self.name + "\nDishes: " + str(self.dishes)
    
    def __repr__(self):
        return "Name: " + self.name + "\nDishes: " + str(self.dishes)