import os
import time
from getpass import getpass

class RechargeConstants:

    operators = ["BSNL", "Airtel", "VodafoneIdea (V!)", "Jio"]
    recharge_pack_map = {
        "BSNL": [],
        "Airtel": [],
        "VodafoneIdea (V!)": [],
        "Jio": []
    }
    MENU_STRING = """
            
        1. Postpaid
        2. Prepaid
            
        Select Recharge Type: """

    OPERATOR_SELECTION = """
        1. {0[0]}
        2. {0[1]}
        3. {0[2]}
        4. {0[3]}
        
        Select Operator: """.format(operators)
        
    PAYMENT_METHOD = """
        1. UPI
        2. Credit/ Debit Card
        
        Select payment method: """

    PACKAGE_SELECTION = """        Enter the amount to recharge: """
    GET_MOBILE_NUMBER = """        Enter the mobile number: """
    GET_CARD_NUMBER = """        Enter card number: """
    GET_EXPIRY_DATE = """        Expiry Date: """
    GET_CVV = """        CVV: """
    GET_UPI = """        Enter UPI: """

    INVALID_CHOICE = """        Invalid Choice, Please try again    """
    INVALID_OPERATOR = """        Invalid Operator, Please try again    """
    INVALID_PACKAGE = """        Invalid Package, Please try again    """
    INVALID_PAYMENT_METHOD = """        Invalid Payment method, Please try again    """

    UNDER_PROCESS = """        The recharge amount of {0} is under process please wait..."""
    RECHARGE_COMPLETE = """        Recharge Complete..."""

    MENU_LIST = [
        {
            "menu_string": MENU_STRING,
            "min": 1,
            "max": 2,
            "error_message": INVALID_CHOICE
        },
        {
            "menu_string": OPERATOR_SELECTION,
            "min": 1,
            "max": 4,
            "error_message": INVALID_OPERATOR
        },
        {
            "menu_string": PACKAGE_SELECTION,
            "skip": True,
            "error_message": INVALID_PACKAGE
        },
        {
            "menu_string": PAYMENT_METHOD,
            "min": 1,
            "max": 2,
            "error_message": INVALID_PAYMENT_METHOD
        }
        
    ]

class Animator:

    TERMINAL_SIZE_COLUMN = os.get_terminal_size().columns
    PADDING_CHAR = "*"
    ANIMATION_PATTERN_LIST = [
        "--+++-+--+_=_++_=_+_=",
        ">>>>>--------->>>>>>>>>",
        "------------->>>>>",
        " - - - - - - - - - - - -",
        "-_-_-_________--_-_----__-_-___-_-_-__-___--",
        "<<<<<<<<<<<<<<<<<<<<<<<<<",
        ".........................",
        "############------"
        ".",
        ".    .    .    .   .   .",
        "..."
    ]
    
    # Prints message without
    def endless_print(self, message):
        print(message, end="")
    
    def slow_print(self, message, speed=100, newline=True):
        output = ""
        for letter in message:
            output += letter
            print(output, flush=True, end="\r")
            time.sleep(speed/1000)
        if(newline):
            print()
    
    def print_full_line(self):
        print("".rjust(self.TERMINAL_SIZE_COLUMN, self.PADDING_CHAR), end="")
        return
    
    def print_clear_line(self):
        print("".rjust(self.TERMINAL_SIZE_COLUMN, " "), end="")
        return
    
    def set_padding_character(self, pad_char):
        self.PADDING_CHAR = pad_char

    # Responsible for creating the heading bar
    def print_heading(self, heading, spacing=2):
        heading_length = len(heading) + (2*spacing)
        heading = (" " * spacing) + heading + (" " * spacing)
        no_of_stars = self.TERMINAL_SIZE_COLUMN - heading_length
        left_stars = 0
        right_stars = 0
        if (no_of_stars % 2) == 0:
            left_stars = right_stars = int(no_of_stars/2)
        else:
            left_stars = int((no_of_stars - 1)/ 2)
            right_stars = left_stars + 1
        
        heading = "".rjust(left_stars, self.PADDING_CHAR) + heading + "".rjust(right_stars, self.PADDING_CHAR)
        print(heading)

    def print_processing(self, anim_type=2, limit=10, anim_data=None):
        i = 0
        if(anim_type == 1):
            anim_fun = self.slash_animation
            args = 200
        elif(anim_type == 2):
            anim_fun = self.arrow_animation
            args = 30
        elif(anim_type == 3):
            anim_fun = self.custom_animation
            if anim_data:
                args = anim_data["index"], anim_data["max_char"], anim_data["speed"]
            else:
                args = self.ANIMATION_PATTERN_LIST[6], 5, 10

        while i < limit:
            anim_fun(args)
            i += 1
        self.print_clear_line()

    def custom_animation(self, anim_data):
        message = anim_data[0]
        max_word = anim_data[1]
        speed = anim_data[2]
        i = 0
        j = i + max_word
        l = len(message)
        no_of_times = int(l - j)
        for current_loop in range(no_of_times+1):
            i = current_loop
            j = i + max_word
            self.slow_print((" " * i) + message[i:j] + (" " * (l-j)), speed, False)
        return

    def arrow_animation(self, speed=30):
        self.slow_print("=    ", speed, False)
        self.slow_print("=>   ", speed, False)
        self.slow_print("=>>  ", speed, False)
        self.slow_print(" >>> ", speed, False)
        self.slow_print("  >>>", speed, False)
        self.slow_print("    >", speed, False)
    
    def slash_animation(self, speed=200):
        self.slow_print("\\", speed, False)
        self.slow_print("-", speed, False)
        self.slow_print("/", speed, False)

"""Recharge class holds the functional requirements for the recharge program to work
"""
class Recharge:
    
    recharge_constants = RechargeConstants()
    animator = Animator()
    values = []
    
    
    def final_output(self):
        if len(self.values) > 3:
            amount = self.values[2]
        else:
            amount = 0
        self.animator.slow_print(self.recharge_constants.UNDER_PROCESS.format(amount), 100)

    def execute_error(self, args):
        self.animator.slow_print(args["error_message"])
        self.menu_processing(args)

    def menu_processing(self, args):
        menu_choice = input(args["menu_string"])
        try:
            menu_choice = int(menu_choice)
            if ("skip" in args.keys()):
                return menu_choice
            if (menu_choice in range(args["min"], args["max"] + 1)):
                return menu_choice
            else:
                self.execute_error(args)

        except Exception as e:
            print("Exception: " + str(e))
            self.execute_error(args)

        return menu_choice

    def perform_recharge(self):
        payment_choice = self.values[3]
        # Using getpass the input will be hidden
        if payment_choice == 1:
            upi = getpass(self.recharge_constants.GET_UPI)
        elif payment_choice == 2:
            card_number = getpass(self.recharge_constants.GET_CARD_NUMBER)
            exp_date = getpass(self.recharge_constants.GET_EXPIRY_DATE)
            cvv = getpass(self.recharge_constants.GET_CVV)
        return

    def print_header(self):
        # Heading
        self.animator.set_padding_character("-")
        self.animator.print_full_line()
        self.animator.print_heading("Welcome To Mobile Recharge Platform")
    
    def print_footer(self):
        # End
        print()
        self.animator.print_full_line()

    def process_recharge(self):
        # Gets Mobile number for recharge
        self.mobile_number = input(self.recharge_constants.GET_MOBILE_NUMBER)
        for item in self.recharge_constants.MENU_LIST:
            self.values.append(self.menu_processing(item))
        # Performs recharge
        self.perform_recharge()

    def show_output(self):
        # Final Output and processing
        self.final_output()
        self.animator.print_processing()
        self.animator.slow_print(self.recharge_constants.RECHARGE_COMPLETE)

    def init(self):
        self.print_header()
        self.process_recharge()
        self.show_output()
        self.print_footer()

    
if __name__ == "__main__":
    # Animator().print_processing(3)
    Recharge().init()