    # print(event.keys())
    # print(event["href"], event["title"], event["class"])
# print(event_table["class"])

    # events_parent_div_locator = "//button[text()='Events']"
    # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, button_locator)))
    # events_parent_div = driver.find_element(By.XPATH, events_parent_div_locator)
    # print("Events-> element: " + events_parent_div.get_attribute("class"))
    # events_parent_div = find_nth_ancestors(events_parent_div, 4)
    # print("Events 5th Anc-> element: " + events_parent_div.get_attribute("class"))

    # # event_divs = events_parent_div.find_elements(By.XPATH, ".//child::*")
    # event_divs = events_parent_div.find_elements(By.XPATH, "//following-sibling::*")
    # i = event_divs[0]
    # print(i.tag_name, i.get_attribute("class"))
    # # for i in event_divs[:4]:
    # #     print(i.tag_name, i.get_attribute("class"))
    # # print("Event Table div -> " + event_div.get_attribute("class"))
    # WebDriverWait(driver, 10)

    # # print(button)
    # # button.click()
    # time.sleep(1000)

        soup = 
        print(parent_.get_attribute("class"))
        children = parent_.find_elements(By.XPATH, ".//*")
        for child in children:
            print(child.get_attribute("class"))
        while True:
            pass
        # button = driver.find_element(By.XPATH, button_locator)
        # button_parent = find_nth_ancestors(button, 6)
        # print(button_parent.get_attribute("class"))
        # all_divs = (driver.find_elements(By.XPATH, "//*[@kind='scale']"))
        # print(all_divs)
                
        # while True:
        #     for div in all_divs:
        #         if div.get_attribute("kind") == "scale":
        #             div.click()
        #             driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        #             WebDriverWait(driver, 3)
        #             pass
        #     # button.click()
        #     pass
    # driver.get(url)





















def capture_price_and_write_to_file(soup, title):
    price_map = capture_price_from_soup(soup)
    with open(joinpath(output_folder, title + ".json")) as f:
        for key in price_map:
            f.write(key + ": " + price_map[key] + "\n")

def get_seat_data_from_event(event):
    scroll_locator = "//*[@kind='scale']"
    refresh = False

    with webdriver.Firefox(service=FirefoxService(gecko_driver)) as driver:
        driver.get(event["url"])
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, scroll_locator)))
        cont_element = driver.find_element(By.XPATH, scroll_locator)
        cont_element.click()
        while cont_element:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            try:
                cont_element = driver.find_element(By.XPATH, scroll_locator)
                parent_ = find_nth_ancestors(cont_element, 1)
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, scroll_locator)))
            except NoSuchElementException:
                break
            except TimeoutException:
                break
            except StaleElementReferenceException:
                refresh = True
        if not refresh:
            soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML").encode("utf-8").decode("utf-8"), "html.parser")
            # soup.get
            x = threading.Thread(target=capture_price_and_write_to_file, args=(soup, event["title"], ), daemon=True, name=event).start()
    if refresh:
        get_seat_data_from_event(event)

def capture_price_from_soup(soup):
    price_map = {}
    select_button = soup.find_all("button")
    for b in select_button:
        if b.text.strip() == "Select":
            select_button = b
            break
    select_button_anc = bs4_find_nth_anchestor(select_button, 6)
    ticket_row_divs = select_button_anc.children
    for child in ticket_row_divs:
        try:
            print(child["class"])
            base_element = bs4_find_nth_successor(child,2)
            children = base_element.findChildren()
            print(len(children))
            x1 = children[0]
            x2 = x1.nextSibling
            x3 = x2.nextSibling
            if x3:
                price_div = x3
                row_div = x2
            else:
                price_div = x2
                row_div = x1
            print(row_div["class"])
            print(price_div["class"])
            row_name = row_div.findChildren()[0].get_text()
            ticket_price = price_div.findChildren()[0].nextSibling.get_text()
            price_map[row_name] = ticket_price
        except KeyError:
            break
    return price_map

# def write_price_to_file(title):
#     pass
