print("Program Started")
from datetime import datetime
start_time = datetime.now()

# Import Default Pacakges
import json, requests, sys, time
from os import getenv
from os.path import join as joinpath
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Thread
# Custom Path For PyUtils Library
sys.path.append(getenv("PYUTILS_PATH"))
from Utilities.WebScrapper.BS4Utilities import BS4Utilities
from Utilities.WebScrapper.SeleniumUtilities import SeleniumUtilities
print(f"{SeleniumUtilities.time_elapsed()} Imports completed")


class DirectoryScrapping(SeleniumUtilities, BS4Utilities):

    records_read = []

    def __init__(self, **kwargs):
        kwargs["botname"] = "PDFHost.io"
        super().__init__(**kwargs)
        self.print_debug_log("Initialized")
    
    def capture_details_from_soup(self, soup):
        parent = soup.find(id="fontevaDetailFields")
        with open("output.csv", "w") as f:
            line = ""
            for child in parent.children:
                line += child.text + "|"
            f.write(line + "\n")
        pass

    def click_every_row_in_directory(self, driver):
        self.WebDriverWait(driver, 10).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "fonteva-record")))
        self.sleep(10, "Waiting for PAGE LOAD")
        records = driver.find_elements(self.By.CLASS_NAME, "fonteva-record")
        if len(records) >= len(self.records_read):
            return
        for record in records:
            value = record.get_attribute("innerText")
            if value not in self.records_read:
                self.records_read.append(value)
                self.ActionChains(driver).move_to_element(record).click(record).perform()
                self.WebDriverWait(driver, 10).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "slds-text-heading_medium")))
                soup = self.convert_webpage_to_soup(driver)
                thread = Thread(target=self.capture_details_from_soup, args=(soup,))
                thread.daemon = True
                thread.start()
                buttons = driver.find_elements(self.By.CLASS_NAME, "slds-button")
                for button in buttons:
                    if button.get_attribute("innerText") == "Back to Results":
                        self.ActionChains(driver).move_to_element(button).click(button).perform()
                        break
            else:
                continue
        self.click_every_row_in_directory(driver)

    def run(self):

        url = "https://contractpackaging.my.site.com/LightningMemberPortal/s/searchdirectory?id=a2n4P0000003FHH"
        driver = self.get_firefox_driver()
        driver.get(url)
        self.print_debug_log("TEST")
        self.WebDriverWait(driver, 10).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "fonteva-record")))
        self.print_debug_log("TEST")
        self.click_every_row_in_directory(driver)
        # records = driver.find_elements(self.By.CLASS_NAME, "fonteva-record")
        # for record in records:
        #     record.click()
        #     self.WebDriverWait(driver, 10).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "slds-text-heading_medium")))
        #     soup = self.convert_webpage_to_soup(driver)
        #     name = record.find_element(self.By.CLASS_NAME, "slds-text-heading_medium").get_attribute("innerText")
        #     print(record)
        # records = driver.find_elements(self.By.CLASS_NAME, "slds-button")
        # for record in records:
        #     print(record.get_attribute("title"), record.get_attribute("disabled"))
        # .get_attribute("innerHTML")
        pass


uploadPdf = DirectoryScrapping()
uploadPdf.set_log_type("ERROR")
uploadPdf.enable_secure_proxy()
uploadPdf.find_working_proxies()
time.sleep(10)
uploadPdf.set_firefox_driver()
uploadPdf.run()
# print(f"Proxies: {len(uploadPdf.proxies)}")
# time.sleep(10)
# print(f"Proxies: {len(uploadPdf.proxies)}")