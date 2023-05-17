class MenuItems:
    name = ""
    price = ""
    dish_type = ""
    quantity = 1
    
    def __init__(self, name, price, dish_type=None):
        self.name = name
        self.price = price
        self.dish_type = dish_type
        pass

    def __str__(self):
        return "{Dish name: " + self.name + ", Price: " + str(self.price) + \
    ", Quantity: " + str(self.quantity) +"}" 
    
    def __repr__(self):
        return self.__str__()

    pass


NORTH_INDIAN_DISHES = [
    MenuItems("Tandoori Chiken half",150),
    MenuItems("Tandoori Chiken full",300),
    MenuItems("Pulka",10),
    MenuItems("Roti",10),
    MenuItems("Butter Roti",15),
    MenuItems("Naan",12),
    MenuItems("Butter Naan",20),
    MenuItems("Garlic Naan",18),
]

SOUTH_INDIAN_BREAKFAST = [
    MenuItems("Oothappam",10),
    MenuItems("Kal Dosa",10),
    MenuItems("Plain Dosa",15),
    MenuItems("Onion Dosa",20),
    MenuItems("Ghee Dosa",25),
    MenuItems("Chicken Dosa",35),
    MenuItems("Masala Dosa",25),
    MenuItems("Idly (Per piece)",8),
    MenuItems("Podi Idly (Per Piece)",10),
    MenuItems("Pongal",30),
]

BIRIYANI_ITEMS = [
    MenuItems("Kuska",40),
    MenuItems("Chicken Biriyani",150),
    MenuItems("Egg Biriyani",120),
    MenuItems("Mutton Biriyani",180),
    MenuItems("Beef Biriyani",200),
        
]