from os import getenv
import sys
sys.path.append(getenv("PYUTILS_PATH"))
from StubHub.MLBTickets import MLBTickets

mltb_tickets = MLBTickets()
mltb_tickets.get_seat_data_from_events()