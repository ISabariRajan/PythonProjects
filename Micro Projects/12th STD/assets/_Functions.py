from getpass import getpass

def perform_recharge(self, amount, payment_choice):
    if payment_choice == 1:
        upi = input(self.constant.GET_UPI)
    elif payment_choice == 2:
        card_number = getpass(self.constant.GET_CARD_NUMBER)
        exp_date = getpass(self.constant.GET_EXPIRY_DATE)
        cvv = getpass(self.constant.GET_CVV)
    return

def select_payment_method(self, package):
    payment_choice = input(self.constant.PAYMENT_METHOD)
    try:
        payment_choice = int(payment_choice)
        self.perform_recharge(package, payment_choice)
    except:
        print(self.constant.INVALID_PAYMENT_METHOD)
        self.select_payment_method()
    return

# Package/ Recharge amount selection
def select_package(self):
    package = input(self.constant.PACKAGE_SELECTION)
    try:
        package = int(package)
        self.select_payment_method(package)
    except:
        print(self.constant.INVALID_PACKAGE)
        self.select_package()
    return

# Choose the operator user wish to recharge
def operator_selection(self, choice):
    operator = input(self.constant.OPERATOR_SELECTION)
    try:
        operator = int(operator)
        if operator in [1,2,3,4]:
            self.select_package()
    except:
        print(self.constant.INVALID_OPERATOR)
    return

# The Main menu, from here all the actual things start
def main_menu(self):
    choice = input(self.constant.MENU_STRING)
    try:
        choice = int(choice)
        if choice in range(1,2):
            self.operator_selection(choice)
        else:
            self.utils.slow_print(self.constant.INVALID_CHOICE)
            self.main_menu()
    except:
        self.utils.slow_print(self.constant.INVALID_CHOICE)
        self.main_menu()