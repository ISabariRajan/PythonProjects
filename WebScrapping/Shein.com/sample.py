print(f"Starting")
from datetime import datetime
start_time = datetime.now()
import json
import requests, sys, time
from os import getenv
from os.path import join as joinpath
from concurrent.futures import ThreadPoolExecutor, wait

from Utilities.WebScrapper.SeleniumUtilities import SeleniumUtilities
from Utilities.WebScrapper.BS4Utilities import BS4Utilities
print(f"Import complete@ {datetime.now()-start_time}")
proxy_count = 0
selenium = SeleniumUtilities(botname="WebScrapper - Shein.com")
proxy_count = 0
print("Selenium INit")
selenium.set_firefox_driver()
bs4 = BS4Utilities(botname="WebScrapper - Shein.com")


base_url = "https://us.shein.com"
sub_path = "/Women-Beachwear-c-2039.html"
query = "?page={}"


















def main():
    # pages_count = selenium.run_function_within_webdriver(function_name=get_pages_count)
    pages_count = 1
    selenium.print_debug_log(f"Pages Count completed in: {datetime.now() - start_time}")
    
    selenium.print_debug_log(f"Pick Items (MainThread) completed in: {datetime.now() - start_time}")
    # while len(pages) < pages_count:
    #     print(len(pages), pages_count)
    #     pass
    selenium.print_debug_log(f"Pages Search for Items completed in: {datetime.now() - start_time}")

    selenium.print_debug_log(f"Starting to get items from each page: {datetime.now() - start_time}")

    # count = 1
    # for soup in pages:
    #     get_items_from_page(soup, page=count)
    #     count += 1



# while True:
#     pass
print("ALL COMPLETE")