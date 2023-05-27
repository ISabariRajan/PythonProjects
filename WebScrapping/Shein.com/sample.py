        # # print(html)
        # with open("test.html", "w") as f:
        #     f.write(str(html))
        # # html.content
        # bs4.generate_bs4(html)
        # soup = bs4.soup
        # review_elem = soup.find("span", class_="product-intro__head-reviews-text")
        # print(f"Getting Review {review_elem}")
        # if review_elem:
        #     item["review"] = review_elem.get("data-review-num")
        # else:
        #     item["review"] = 0

    # selenium.set_firefox_driver()
    # driver = selenium.driver
    # with selenium.driver as driver:
    #     for key in items:
    #         item = items[key]
    #         driver.get(item["link"])
    #         print(f"Getting Review from: {item['link']}")
    #         driver.get(item["link"])
    #         selenium.WebDriverWait(driver, 5)
    #         soup = selenium.convert_webpage_to_soup(driver)
    #         review_elem = soup.find("span", class_="product-intro__head-reviews-text")
    #         print(f"Getting Review {review_elem}")
    #         if review_elem:
    #             item["review"] = review_elem.get("data-review-num")
    #         else:
    #             item["review"] = 0
        # driver.close()