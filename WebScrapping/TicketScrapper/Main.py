import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
# from multiprocessing.pool import ThreadPool
from os.path import join as joinpath

def find_nth_ancestors(element, n):
    for i in range(n):
        element = element.find_element(By.XPATH, "./..")
    return element

def find_nth_sibling(element, n):
    for i in range(n):
        element = element.find_element(By.XPATH, ".//following-sibling::*")
        print(element.tag_name)
        print(element.get_attribute("tag"))
    return element


def bs4_find_nth_anchestor(element, n):
    for i in range(n + 1):
        element = element.parent
    return element

def bs4_find_nth_sibling(element, n):
    for i in range(n + 1):
        element = element.nextSibling
    return element

def bs4_find_nth_successor(element, n):
    for i in range(n + 1):
        element = element.findChildren()[0]
    return element

pool = ThreadPoolExecutor(10)
gecko_driver = GeckoDriverManager().install()
output_folder = "output"
base_url = "https://www.stubhub.com/"
def get_all_events_from_game():
    url = base_url + "mlb-tickets/grouping/81/"
    soup = ""
    # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    with webdriver.Firefox(service=FirefoxService(gecko_driver)) as driver:
        driver.get(url)
        button_locator = "//*[text()='See More']"
        print("Clicking See More, Until nothing left")
        while True:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, button_locator)))
                button = driver.find_element(By.XPATH, button_locator)
                button.click()
                # soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML").encode("utf-8").decode("utf-8"), "html.parser")
                # break
            except TimeoutException:
                break
        
        time.sleep(5)
        soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML").encode("utf-8").decode("utf-8"), "html.parser")

    events_button = soup.find_all("button")
    for b in events_button:
        if b.text.strip() == "Events":
            events_button = b
            break
    events_button_anc = bs4_find_nth_anchestor(events_button, 3)
    event_table = bs4_find_nth_sibling(events_button_anc, 2)
    all_events = event_table.findChildren("a")

    all_events_link = []

    print(f"Total Events: {len(all_events)}")
    for a in all_events:
        event = a.get("href").split("/")
        id = event[-2:][0]
        title = event[-4:][0] + " - " + id
        all_events_link.append({
            "url": base_url + a.get("href"),
            "title": title,
            "id": id,
            "status": "new"
        })
    return all_events_link

def get_seat_data_from_event(event):
    print("Getting Seat details from : ", event["title"])
    response = requests.post(event["url"]).json()
    # with open(joinpath("output", event["title"] + ".json"), "w") as f:
    #     f.write(json.dumps(response, indent=2))
    obj_keys = [
        "Section", "Row", "Price"
    ]
    try:
        with open(joinpath("output", event["title"] + ".csv"), "w") as f:
            f.write("Section, Row, Price, SeatsRemaining\n")
            for data in response["Items"]:
                # print(data)
                line = ""
                for key in obj_keys:
                    val = data[key]
                    if val == None:
                        val = " - "
                    val= val.replace(",", "")
                    line += val + ", "

                val = data["TicketsLeftInListingMessage"]
                if val == None:
                    val = 0
                else:
                    val = val["Message"]
                    if val == None:
                        val = 0
                    else:
                        val = val.split(" ")[0]

                line += str(val) + "\n"
                f.write(line)
    except Exception as e:
        print(e)


all_events_link = get_all_events_from_game()
for event in all_events_link:
    pool.submit(get_seat_data_from_event, (event))

print("OUT")