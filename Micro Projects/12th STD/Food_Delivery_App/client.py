import Animator
import Restaurant
import constants
from getpass import getpass


class Order:
    dishes = []
    
    def __init__(self):
        self.total_price = 0
    
    def add_dish(self, dish):
        self.total_price += (dish.price * dish.quantity)
        self.dishes.append(dish)
    
    def __str__(self):
        return "Total Price: " + str(self.total_price) + "\nDishes: " + str(self.dishes)

def print_header():
    animator.set_padding_character(".")
    animator.print_full_line()
    animator.set_padding_character("|")
    animator.print_heading("Food booking app", spacing=40)
    animator.set_padding_character(".")
    animator.print_full_line()
    animator.reset_padding_character()

def print_menu():
    choice = 0
    while(choice not in [1,2,3]):
        print("1. View nearby restaurants")
        print("2. View order")
        # print("3. Pay order")
        try:
            choice = int(input("Enter Selection: "))
        except:
            pass
    return choice

def print_restaurants():
    index = 0
    length = len(constants.RESTAURANT_LIST)
    choice = 0
    while(choice not in range(1,length + 1)):
        print()
        for restaurant in constants.RESTAURANT_LIST:
            index += 1
            print(str(index) + ". " + restaurant.name)
        index = 0
        try:
            choice = int(input("Select Restaurant: "))
           
        except:
            canLoop = True
            pass
    return choice


def print_restaurant_menu(restaurant):
    index = 0
    length = len(restaurant.dishes)
    choice = 0
    canLoop = True
    while(canLoop):
        print()
        for dish in restaurant.dishes:
            index += 1
            print(str(index) + ". " + dish.name.ljust(50, " ") + "- " + constants.RUPEE_SYMBOL + str(dish.price))
        index = 0
        try:
            choice = int(input("Select Dish: "))
            if(choice not in range(1,length + 1)):
                canLoop = True
                print("Invalid Selection, Please select again.")
            else:
                dish = restaurant.dishes[choice - 1]    
                no_of_dishes = int(input("Enter no.of " + dish.name + " : "))
                dish.quantity = no_of_dishes
                order.add_dish(dish)
                canLoop = not((input("Finish Orders? Y/N: ").lower() == "y"))
        except:
            pass
    
    return choice

def print_order():
    animator.print_full_line()
    animator.print_heading("BILL INVOICE")
    animator.print_full_line()
    index = 0
    for dish in order.dishes:
        index += 1
        message = str(index) + ". " + dish.name.ljust(30, " ") + " - " + \
            str(constants.RUPEE_SYMBOL + str(dish.price)).rjust(10, " ") + " X " + \
                str(str(dish.quantity) + "ps").ljust(10, " ") + " : " + constants.RUPEE_SYMBOL + str(dish.quantity * dish.price)
        print(message)
    print("Total Price" + str(": " + constants.RUPEE_SYMBOL + str(order.total_price)).rjust(56, " "))

def perform_transaction():
    select_payment_method()
    show_output()

def process_payment(payment_choice):
    if payment_choice == 1:
        upi = input(constants.GET_UPI)
    elif payment_choice == 2:
        card_number = getpass(constants.GET_CARD_NUMBER)
        exp_date = getpass(constants.GET_EXPIRY_DATE)
        cvv = getpass(constants.GET_CVV)
    return

def select_payment_method():
    payment_choice = input(constants.PAYMENT_METHOD)
    try:
        payment_choice = int(payment_choice)
        process_payment(payment_choice)
    except:
        print(constants.INVALID_PAYMENT_METHOD)
        select_payment_method()
    return

def show_output():
    # Final Output and processing
    animator.slow_print(constants.UNDER_PROCESS.format(constants.RUPEE_SYMBOL,order.total_price), 100)
    animator.print_processing(anim_type=1)
    animator.slow_print(constants.TRANSACTION_COMPLETE)


def main(order):
    print_header()
    canLoop= True
    while(canLoop):
        choice = print_menu()
        if(choice == 1):
            order = Order()
            restaurant = constants.RESTAURANT_LIST[print_restaurants() -1]
            print_restaurant_menu(restaurant)
            print_order()
            perform_transaction()
        elif(choice == 2):
            if(order and order.total_price > 0):
                print_order()
            else:
                print("No Order Found")
        # elif(choice==3):
        #     perform_transaction()
        
        canLoop = not(input("Exit? (Y/N)").lower() == "y")
    animator.print_full_line()
        

    pass

if __name__ == "__main__":
    animator = Animator.Animation()
    order = Order()
    main(order)