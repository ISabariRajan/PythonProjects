print("Program Started")
from datetime import datetime
start_time = datetime.now()

# Import Default Pacakges
import json, requests, sys, time
from os import getenv
from os.path import join as joinpath
from concurrent.futures import ThreadPoolExecutor, wait
sys.path.append(getenv("PYUTILS_PATH"))
from Utilities.WebScrapper.SeleniumUtilities import SeleniumUtilities
# from Utilities.WebScrapper.BS4Utilities import BS4Utilities
print(f"{SeleniumUtilities.time_elapsed()} Imports completed")

# utilities = SeleniumUtilities()

class UploadPDF(SeleniumUtilities):

    def __init__(self, **kwargs):
        kwargs["botname"] = "PDFHost.io"
        super().__init__(**kwargs)
        self.print_debug_log("Initialized")
    
    def run(self):
        url = "https://pdfhost.io/"
        driver = self.get_firefox_driver()
        driver.get(url)
        self.WebDriverWait(driver, 10).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "sui-pagination__total")))
        pass


uploadPdf = UploadPDF()
# uploadPdf.find_working_proxies()
time.sleep(10)
uploadPdf.set_firefox_driver()
# uploadPdf.enable_proxy()
uploadPdf.run()
# print(f"Proxies: {len(uploadPdf.proxies)}")
# time.sleep(10)
# print(f"Proxies: {len(uploadPdf.proxies)}")