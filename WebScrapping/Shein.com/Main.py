import requests
from os import getenv
import sys
from concurrent.futures import ThreadPoolExecutor, wait

sys.path.append(getenv("PYUTILS_PATH"))
from Utilities.package import SeleniumUtilities, BS4Utilities


selenium = SeleniumUtilities(botname="WebScrapper - Shein.com")
selenium.set_firefox_driver()
selenium.print_debug_log("Started")
bs4 = BS4Utilities(botname="WebScrapper - Shein.com")
base_url = "https://us.shein.com"
sub_path = "/Women-Beachwear-c-2039.html"
query = "?page={}"
pool = ThreadPoolExecutor(30)
pages = []
futures = []
items = {}

def process_item(item):
    id = item.get("data-expose-id")
    # Meaning It is containing Data
    if id:
        print(f"Checking: {id}")
        item_data_elem = item.find("div", class_="S-product-item__name")
        if item_data_elem:
            item_link = item_data_elem.find("a", class_="S-product-item__link")
        else:
            print(f"Issue: {id}")
            return
        if item_link:
            link = base_url + item_link.get("href")
            sku = item_link.get("data-sku")
            spu = item_link.get("data-spu")
        
        price_elem = item.find("span", class_="normal-price-ctn__sale-price_big")
        if price_elem:
            price = price_elem.text
        else:
            price = 0

        # Capture Review Count
        url = base_url + "/goods_detail_nsw/getCommentInfoByAbc"
        queries = "?_ver=1.1.8&_lang=en&spu={}&goods_id=&page=1&limit=3&offset=0&sort=&size=&is_picture=&rule_id=recsrch_sort:A|recsrch_tag:A&tag_id=&local_site_abt_flag=&shop_id=&query_rank=1"
        link = url + queries.format(spu)
        res = requests.get(link).json()
        data = {
            "name": item_link.get("data-title"),
            "link": link,
            "price": price,
            "sku": sku,
            "spu": spu,
            "review_count": res["info"]["commentInfoTotal"]
        }
        items[data["sku"]] = data
        return True
    


def get_items_from_page(soup):
    print("Get Items")
    elem = soup.find("div", class_="product-list-v2__container")
    the_items_list = elem.find_all("section")
    for item in the_items_list:
        future = pool.submit(process_item, (item))
        futures.append(future)
    return True


def capture_page_as_soup(driver, **kwargs):
    url = kwargs["url"]
    print(f"Capturing page: {url}")
    driver.get(url)
    selenium.WebDriverWait(driver, 10)
    soup = selenium.convert_webpage_to_soup(driver)
    pages.append(soup)
    future = pool.submit(get_items_from_page, (soup))
    futures.append(future)

def get_pages_count(driver):
    url = base_url + sub_path
    capture_page_as_soup(driver, url=url)
    pages_count = driver.find_elements(selenium.By.CLASS_NAME, "sui-pagination__total")[0].text
    pages_count = pages_count.replace("Total", "").replace("Pages", "").strip()
    return int(pages_count)

def pick_item_info(pages_count):
    with ThreadPoolExecutor(2) as pool:
        for i in range(1, int(pages_count) + 1):
            url = base_url + sub_path + query.format(i)
        # selenium.run_function_within_webdriver(capture_page_as_soup, url=url)
        # capture_page_as_soup(driver, url)
            future = pool.submit(selenium.run_function_within_webdriver, capture_page_as_soup, url=url)
            futures.append(future)

def process_soup():
    for soup in pages:
        bs4.generate_bs4(soup)
        get_items_from_page(bs4.soup)
    

def write_data_to_file():
    attribs = [
        "name", "link", "price", "sku", "review_count"
    ]
    with open("output.csv", "w") as f:
        print(f"Writing output to file: ")
        line = ""
        for attrib in attribs:
            line += attrib + ","
        f.write(line + "\n")
        for key in items:
            line = ""
            item = items[key]
            for attrib in attribs:
                line += str(item[attrib]) + ","
                pass
            f.write(line + "\n")

pages_count = selenium.run_function_within_webdriver(function_name=get_pages_count)
pick_item_info(pages_count)

future, _ = wait(futures)
for future in futures:
    result = future.result()
    # if not result:


print(items)
# process_soup()
write_data_to_file()