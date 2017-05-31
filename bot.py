import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.implicitly_wait(10)

def login():
    driver.get("http://typeracer.com")

    sign_in = driver.find_element_by_link_text("Sign In")
    sign_in.click()

    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys("swimbot")

    password = driver.find_element_by_name("password")
    password.clear()
    with open("password", "r") as f:
        password.send_keys(f.readline(), Keys.RETURN)

def setup_lobby():
    lobby_link = driver.find_element_by_link_text("Race your friends")
    lobby_link.click()

    link_box = driver.find_element_by_class_name("urlTextbox")
    link = link_box.get_attribute("value")

    OK = driver.find_element_by_link_text("OK")
    OK.click()

    print("URL: {}".format(link))

def race():
    start = driver.find_element_by_partial_link_text("join race")
    start.click()

    time.sleep(0.5)
    preview_text()

    while True:
        try:
            driver.find_element_by_class_name("countdownPopup")
        except:
            break

    exit = driver.find_element_by_partial_link_text("leave race")
    exit.click()

def preview_text():
    possibilities = driver.find_elements_by_tag_name("span")

    s = ">> "

    for e in possibilities:
        if re.search(r'nhwMiddlegwt-uid-.*', e.get_attribute("id")) is not None:
            s += e.text + " "
        elif re.search(r'nhwRightgwt-uid-.*',
                       e.get_attribute("id")) is not None:
            s += e.text

    chat_box = driver.find_element_by_class_name("AdvancedTextBox")

    split_s = [s[i:i + 500] for i in range(0, len(s), 500)]

    for s in split_s:
        chat_box.send_keys(s, Keys.RETURN)

def quit():
    driver.close()

if __name__ == "__main__":
    login()
    setup_lobby()

    while True:
        try:
            race()
        except KeyboardInterrupt:
            break
    quit()
