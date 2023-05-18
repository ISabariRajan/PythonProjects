import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager

url = "https://www.youtube.com/watch?v=pd2wZSbGiJM"
data = []
# driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
with webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install())) as driver:
    driver.get(url)
    wait = WebDriverWait(driver,15)
    time.sleep(5)

    try:
        cont_element = driver.find_element(By.ID, "contents").find_element(By.XPATH, ".//ytd-continuation-item-renderer")
        # .find_element(By.TAG_NAME, "ytd-continuation-item-renderer")
        last_element = None
        while cont_element:
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(5)
            cont_element = driver.find_element(By.ID, "contents").find_element(By.XPATH, ".//ytd-continuation-item-renderer")
            all_comments = driver.find_element(By.ID, "contents").find_elements(By.TAG_NAME, "ytd-comment-thread-renderer")
            if last_element:
                if last_element == all_comments[-1]:
                    break
                else:
                    last_element = all_comments[-1]
            else:
                last_element = all_comments[-1]
    except NoSuchElementException as e:
        print(e)
        pass
    

    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        data.append(comment.text)


print(data)