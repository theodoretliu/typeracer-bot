import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, float("inf"), poll_frequency=0.1)

def go_to_site():
    driver.get("http://typeracer.com")

def login():
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

def join_race():
    join_button = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "join race")))
    join_button.click()

def leave_race():
    leave_button = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "leave race")))
    leave_button.click()

def race_again():
    race_again_button = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Race Again")))
    race_again_button.click()

def get_words():
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inputPanel")))
    words = driver.find_elements(By.XPATH, "//span[@unselectable='on']")

    words = list(map(lambda x: x.text, words))

    l = len(words)

    if l == 3:
        return "{}{} {}".format(words[0], words[1], words[2])
    elif l == 2:
        return "{} {}".format(words[0], words[1])

def join_public():
    join_button = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Enter a typing race")))
    join_button.click()

def race(text, wpm=120):
    words = text.split(" ")
    new_words = [words[i] + " " for i in range(len(words) - 1)]
    new_words.append(words[-1])

    delay = 2 * 60 / wpm
    count = 1

    delay = 60 / (5 * wpm) / 2
    wait.until_not(EC.presence_of_element_located((By.XPATH, "//input[@disabled]")))

    input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "txtInput")))
    input_box.clear()

    for c in text:
        input_box.send_keys(c)
        time.sleep(delay)

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

# go_to_site()
# setup_lobby()
# join_race()
# race(get_words(), 150)

if __name__ == "__main__":
    login()
    setup_lobby()

    while True:
        try:
            race()
        except KeyboardInterrupt:
            break
    quit()
