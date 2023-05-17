import MenuItems as menuitems
from Restaurant import Restaurant as restaurant

item = menuitems.MenuItems

RUPEE_SYMBOL = str(u"\u20B9" + str(" "))

RESTAURANT_LIST = [
    restaurant("Mugal Biriyani", menuitems.BIRIYANI_ITEMS),
    restaurant("Dindugul Thalappakatti", menuitems.BIRIYANI_ITEMS),
    restaurant("Madurai Kadai", menuitems.SOUTH_INDIAN_BREAKFAST),
    restaurant("Abrooz Meshi", menuitems.NORTH_INDIAN_DISHES)
]

PAYMENT_METHOD = """
1. UPI
2. Credit/ Debit Card
    
Select payment method: """
INVALID_PAYMENT_METHOD = """Invalid Payment method, Please try again    """
GET_CARD_NUMBER = """Enter card number: """
GET_EXPIRY_DATE = """Expiry Date: """
GET_CVV = """CVV: """
GET_UPI = """Enter UPI: """
UNDER_PROCESS = """The payment of amount {0}{1} is under process please wait..."""
TRANSACTION_COMPLETE = """Payment Complete..."""