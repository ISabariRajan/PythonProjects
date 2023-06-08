print("Program Started")
from datetime import datetime
start_time = datetime.now()

# Import Default Pacakges
import json, requests, sys, time
from os import getenv
from os.path import join as joinpath
from concurrent.futures import ThreadPoolExecutor, wait

from Utilities.WebScrapper.SeleniumUtilities import SeleniumUtilities
from Utilities.WebScrapper.BS4Utilities import BS4Utilities
print(f"{SeleniumUtilities.time_elapsed()} Imports completed")

class SheinScrapper(SeleniumUtilities, BS4Utilities):

    base_url = "https://us.shein.com"
    sub_path = "/Women-Beachwear-c-2039.html"
    query = "?page={}"

    pool = ThreadPoolExecutor(100)
    pages = []
    futures = []
    items = {}

    failed_items = []

    def __init__(self, **kwargs):
        kwargs["botname"] = "SheinScrapper"
        super().__init__(**kwargs)
        self.print_debug_log(f"Initialized")
        print("HIT")
    
    def print_proxies(self):
        print(self.proxies)

    def capture_review_count(self, item):
        # self.print_info_log(f"Capturing Review count for {item['spu']}")
        queries = "?_ver=1.1.8&res=en&spu={}&goods_id=&page=1&limit=3&offset=0&sort=&size=&is_picture=&rule_id=recsrch_sort:A|recsrch_tag:A&tag_id=&local_site_abt_flag=&shop_id=&query_rank=1"
        # Capture Review Count
        url = self.base_url + "/goods_detail_nsw/getCommentInfoByAbc"
        link = url + queries.format(item['spu'])
        res = self.net.proxy_request(url=link, error=item['sku'])
        if res:
            with open(joinpath("Output", item["sku"] + ".json")) as f:
                f.write(json.dumps(res, indent=2))
            # item["review_count"] = res["info"]["commentInfoTotal"]
            # items[item["sku"]] = item
        else:
            self.failed_items.append(item)

    def process_item(self, item, **kwargs):
        self.print_info_log(f"Pocessing Item {kwargs['item_no']} in Page {kwargs['page']}")
        item_data_elem = item.find("div", class_="S-product-item__name")
        if item_data_elem:
            item_link = item_data_elem.find("a", class_="S-product-item__link")
        else:
            # self.print_info_log(f"Issue: {id}")
            return
        if item_link:
            link = self.base_url + item_link.get("href")
            sku = item_link.get("data-sku")
            spu = item_link.get("data-spu")
        
        price_elem = item.find("span", class_="normal-price-ctn__sale-price_big")
        if price_elem:
            price = price_elem.text
        else:
            price = 0

        data = {
            "name": item_link.get("data-title"),
            "link": link,
            "price": price,
            "sku": sku,
            "spu": spu,
        }
        # pool.submit(capture_review_count, data)

    def get_items_from_page(self, soup, **kwargs):
        elem = soup.find("div", class_="product-list-v2__container")
        the_items_list = elem.find_all("section")
        count = 1
        for item in the_items_list:
            id = item.get("data-expose-id")
            # Meaning It is containing Data
            if id:
                self.process_item(item, **kwargs, item_no=count)
                count += 1
        return True

    def capture_page_as_soup(self, driver, **kwargs):
        try:
            url = kwargs["url"]
            self.print_info_log(f"Capturing page: {kwargs['page']}")
            driver.get(url)
            self.WebDriverWait(driver, 10).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, "sui-pagination__total")))
            soup = self.convert_webpage_to_soup(driver)
            # with open("test.html", "w") as f:
            #     f.write(str(soup))
            # get_items_from_page(soup, page=1)
            # pages.append(soup)

        except self.exceptions.TimeoutException:
            # capture_page_as_soup(driver, **kwargs)
            pass

    def write_data_to_file(self):
        self.print_info_log("Write Output to file")
        attribs = [
            "name", "link", "price", "sku", "review_count"
        ]
        with open("output.csv", "w") as f:
            line = ""
            for attrib in attribs:
                line += attrib + ","
            f.write(line + "\n")
            for key in self.items:
                line = ""
                item = self.items[key]
                for attrib in attribs:
                    line += str(item[attrib]) + ","
                    pass
                f.write(line + "\n")

    def pick_item_info(self, pages_count):
        with ThreadPoolExecutor(5) as pool:
            for i in range(1, int(pages_count) + 1):
                url = self.base_url + self.sub_path + self.query.format(i)
                future = pool.submit(self.run_function_within_webdriver, self.capture_page_as_soup, url=url, page=i)
                self.futures.append(future)

    def get_pages_count(self, driver):
        self.print_debug_log("Getting Pages Count")
        url = self.base_url + self.sub_path
        self.capture_page_as_soup(driver, url=url, page="Initial")
        pages_count = driver.find_element(self.By.CLASS_NAME, "sui-pagination__total").get_attribute("innerHTML")
        pages_count = pages_count.replace("Total", "").replace("Pages", "").strip()
        return int(pages_count)
    
    def scrape_content(self):
        pages_count = self.run_function_within_webdriver(function_name=self.get_pages_count)
        self.pick_item_info(pages_count)
        self.print_debug_log(f"Completed Single thread, waiting for other threads to complete: {datetime.now() - start_time}")
        future, _ = wait(self.futures)
        for future in self.futures:
            result = future.result()
        self.print_debug_log(f"All Threads Complete@: {datetime.now() - start_time}")
        self.print_debug_log(f"Checking {len(self.failed_items)} Failed Items: {datetime.now() - start_time}")

        while len(self.failed_items) > 0:
            # capture_review_count(failed_items.pop())
            future = self.pool.submit(self.capture_review_count, self.failed_items.pop())
            self.print_info_log(f"Total Fails: {len(self.failed_items)}")
            self.futures.append(future)
            future, _ = wait(self.futures)
            for future in self.futures:
                result = future.result()
        self.print_info_log(f"{pages_count} Pages searched and found {len(self.items.keys())} Items..")
        self.write_data_to_file()
        end_time = datetime.now()
        self.print_debug_log(f"All Ended: {datetime.now() - start_time}")
        pass

shein = SheinScrapper()
shein.find_working_proxies()
shein.set_firefox_driver()
shein.enable_proxy()
# pages_count = shein.run_function_within_webdriver(function_name=shein.get_pages_count)
# shein.print_proxies()
# shein.scrape_content()
# for i in range(100):
#     print(shein.proxy())