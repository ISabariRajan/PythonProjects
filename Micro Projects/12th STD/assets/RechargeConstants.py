
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