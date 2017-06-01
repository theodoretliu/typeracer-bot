import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, float("inf"), poll_frequency=0.1)
WPM = 200

def login():
    driver.get("http://typeracer.com")

    sign_in = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Sign In")))
    sign_in.click()

    username = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    username.clear()
    username.send_keys("swimbot")

    password = driver.find_element_by_name("password")
    password.clear()
    with open("password", "r") as f:
        password.send_keys(f.readline(), Keys.RETURN)

def setup_lobby():
    time.sleep(1)
    lobby_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Race your friends")))
    lobby_link.click()

    invite_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "invite people")))
    invite_link.click()

    link_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "urlTextbox")))
    link = link_box.get_attribute("value")

    OK = driver.find_element_by_link_text("OK")
    OK.click()

    print(link)

def race():
    start = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "join race")))
    start.click()

    preview_text()

    wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "countdownPopup")))

    print(1)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "txtInput")))

    print(2)
    possibilities = driver.find_elements_by_tag_name("span")
    print(3)
    s = ""
    for e in possibilities:
        if re.search(r"nhwMiddlegwt-uid-.*", e.get_attribute("id")) is not None:
            s += e.text
        elif re.search(r"nhwMiddleCommagwt-uid-.*", e.get_attribute("id")) is not None:
            s += e.text + " "
        elif re.search(r'nhwRightgwt-uid-.*',
                       e.get_attribute("id")) is not None:
            s += e.text

    print(4)
    text_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "txtInput")))

    print(5)
    for word in s.split():
        text_input.send_keys(word + " ")
        time.sleep(60 / WPM)

    exit = driver.find_element_by_partial_link_text("leave race")
    exit.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'You will be able')]")))

    wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "join race")))

def preview_text():
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nonHideableWords")))

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
        chat_box.send_keys(s)
        chat_box.send_keys(Keys.RETURN)

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
