from os import getenv
import sys
from threading import Thread, Timer

sys.path.append(getenv("PYUTILS_PATH"))
from StubHub import Events
import json
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailUtils:

    port = 465
    sender_email = "admin@meimai.in"
    password = "Cl0v6h3@d."
    smtp_url = "server79.dnsbootclub.com"

    def send_email(self, receiver, subject, body):
        mail = MIMEMultipart()
        mail["From"] = self.sender_email
        mail["To"] = receiver
        mail["Subject"] = subject
        mail.attach(MIMEText(body, "plain"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_url, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver, mail.as_string())


class PriceAlerter:

    event_url = "https://www.stubhub.com/atlanta-braves-atlanta-tickets-6-9-2023/event/150522621/?quantity=2"
    no_of_seats = 2
    price_alert = 1800
    notify_email = "iamsabarirajan@gmail.com"
    email = EmailUtils()

    def get_event_details(self):
        print("RUNNNING")
        self.seat_details = Events.get_event_details(self.event_url)["Items"]
        with open("output.json", "w") as f:
            f.write(json.dumps(self.seat_details, indent=2))
        self.find_price_alert()
        Timer(60 * 5, self.get_event_details).start()
    
    def get_user_info(self):
        self.event_url = input("Enter Event URL: ")
        # self.event_url, queries = self.event_url.split("?")
        # thread = Thread(target=self.get_event_details)
        # thread.daemon = True
        # thread.start()
        self.no_of_seats = int(input("Enter Number of Seats: "))
        self.price_alert = float(input("Enter Price Alert: "))
        self.notify_email = input("Enter Email to notify: ")
        self.get_event_details()

    def find_price_alert(self):
        print("Price Alert")
        for item in self.seat_details:
            # print(f"{item['RawPrice'] <= self.price_alert} ...... {item['RawPrice']} ... {self.price_alert}")
            if item["MaxQuantity"] >= self.no_of_seats:
                if item["RawPrice"] <= self.price_alert:
                    print("Found a Match")
                    data = f"Section: {item['Section']}, Row: {item['Row']}, No. of Seats: {self.no_of_seats} Available for Price: {item['RawPrice']}"

                    self.email.send_email(
                        receiver="mailme@isabarirajan.com",
                        body=data, subject="Price Alert for StubHub"
                    )


alerter = PriceAlerter()
alerter.get_user_info()
# alerter.get_event_details()


