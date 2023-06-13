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
    page_down_times = 0

    def __init__(self, **kwargs):
        kwargs["botname"] = "PDFHost.io"
        super().__init__(**kwargs)
        self.print_debug_log("Initialized")

    def make_string_single_line(self, string):
        return string.replace("\n", " ").replace("\t", " ").replace("  ", " ").strip()
    
    def capture_details_from_soup(self, soup, value):
        text_set = [value[-2:]]
        for child in soup.select("span[class='fonteva-slds-text']"):
            val = self.make_string_single_line(child.text)
            if (val and  (val != "Billing State/Province")):
                text_set.append(val)

        with open("output.csv", "a") as f:
            line = " | ".join(text_set)
            f.write(line + "\n")

    def capture_details_from_record(self, record, value, driver):
        while True:
            try:
                self.ActionChains(driver).move_to_element(record).click(record).perform()
                break
            except self.exceptions.MoveTargetOutOfBoundsException as e:
                driver.execute_script("arguments[0].scrollIntoView()", record)
                self.sleep(5)
                continue
            except self.exceptions.StaleElementReferenceException as e:
                break

        self.WebDriverWait(driver, 100).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "slds-text-heading_medium")))
        soup = self.convert_webpage_to_soup(driver)
        
        thread = Thread(target=self.capture_details_from_soup, args=(soup,value,))
        thread.daemon = True
        thread.start()
        buttons = driver.find_elements(self.By.CLASS_NAME, "slds-button")
        for button in buttons:
            if button.get_attribute("innerText") == "Back to Results":
                self.ActionChains(driver).move_to_element(button).click(button).perform()
                break
        self.records_read.append(value)

    def click_every_row_in_directory(self, driver):
        self.WebDriverWait(driver, 100).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "fonteva-record")))
        self.sleep(10, "Waiting for PAGE LOAD")
        records = driver.find_elements(self.By.CLASS_NAME, "fonteva-record")

        if len(self.records_read) >= len(records):
            return
        for record in records:
            value = self.make_string_single_line(record.get_attribute("innerText"))
            if value not in self.records_read:
                print(len(self.records_read), len(records), value)
                self.click_next_page_until_n(driver)
                self.capture_details_from_record(record, value, driver)
                break
            else:
                continue
        self.click_every_row_in_directory(driver)

    def click_next_page_until_n(self, driver):
        self.WebDriverWait(driver, 100).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "fonteva-record")))
        for i in range(1, self.page_no):
            self.print_debug_log(f"Page: {i}/{self.page_no}")
            buttons = driver.find_elements(self.By.CSS_SELECTOR, "button.slds-button_icon-bare")
            for button in buttons:
                title = button.get_attribute("title")
                disabled = button.get_attribute("disabled")
                if title:
                    if title == "Next Page":
                        if not disabled:
                            driver.execute_script("arguments[0].scrollIntoView()", button)
                            self.sleep(5)
                            self.ActionChains(driver).move_to_element(button).click(button).perform()
                            self.records_read = []
                            return True
                        else:
                            return False
                            break
    def run(self):
        url = "https://contractpackaging.my.site.com/LightningMemberPortal/s/searchdirectory?id=a2n4P0000003FHH"
        driver = ""
        driver = self.get_firefox_driver()
        self.print_debug_log("Loading Directory Url")
        driver.get(url)
        self.print_debug_log("Click Every Row in directory Table")
        can_loop = True
        self.WebDriverWait(driver, 100).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "fonteva-record")))
        max_page = int(driver.find_elements(self.By.CSS_SELECTOR, "span.fonteva-slds-text.slds-m-left--x-small")[1].get_attribute("innerText"))
        # print(test.get_attribute("innerText"))
        self.page_no = 1
        for self.page_no in range(max_page):
            self.sleep(5)
            self.click_every_row_in_directory(driver)
            self.page_no += 1
            # can_loop = self.click_next_page_until_n(driver, page_no)



uploadPdf = DirectoryScrapping()
uploadPdf.set_log_type("ERROR")
uploadPdf.enable_secure_proxy()
uploadPdf.find_working_proxies()
time.sleep(10)
uploadPdf.set_firefox_driver()
uploadPdf.run()