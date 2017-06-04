import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, float("inf"), poll_frequency=0.1)

# convenience method to load up the website
def go_to_site():
    driver.get("http://typeracer.com")

# method to log in with certain hidden credentials. currently not working
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

# sets up a lobby so you can race your friends
def setup_lobby():
    # sleep before doing this because sometimes need the page to reload after
    # we sign in
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

# convenience method to join a race
# pre-condition: you are in the "race your friends" mode
def join_race():
    join_button = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "join race")))
    join_button.click()

# method to leave a race
# pre-condition: you are in an active race
def leave_race():
    leave_button = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "leave race")))
    leave_button.click()

# start another race
# pre-condition: you are in public race mode and the race has finished
def race_again():
    race_again_button = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Race Again")))
    race_again_button.click()

# method to get the words for typing
def get_words():
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inputPanel")))

    # find all the elements that are "unselectable," i.e. the text
    words = driver.find_elements(By.XPATH, "//span[@unselectable='on']")
    words = list(map(lambda x: x.text, words))

    l = len(words)

    # if the first word is only a single character, e.g. "I," then there our
    # list will only be 2 long. Otherwise it will be 3
    if l == 3:
        return "{}{} {}".format(words[0], words[1], words[2])
    elif l == 2:
        return "{} {}".format(words[0], words[1])

# method to join the public race
# pre-condition: you are on the home page
def join_public():
    join_button = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Enter a typing race")))
    join_button.click()

# method to race
# pre-condition: you are in a race and have not typed anything
#
# text: the words that needed to be typed
# wpm: the speed at which you want to type - 120 is the default
def race(text, wpm=120):
    words = text.split()

    # add a space after each word so that when we type, it allows us to go
    # to the next word
    new_words = [word + " " for word in words]

    # perfectly tuned delay to get you approximately the wpm that you want
    # methodology is to use characters per minute then factor in the time
    # that it takes to send the keys
    delay = 60 / (5 * wpm) / 2

    wait.until_not(EC.presence_of_element_located((By.XPATH, "//input[@disabled]")))

    input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "txtInput")))
    input_box.clear()

    # typing typing
    for c in text:
        input_box.send_keys(c)
        time.sleep(delay)

# method to preview the text if the bot is hosting a lobby
# pre-condition: you are in "race with friends" mode
# currently not finished
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

# close the browser window
def quit():
    driver.close()

# main method, currently just trolling the public races without signing in
if __name__ == "__main__":
    go_to_site()
    join_public()

    while True:
        try:
            race(get_words())
            race_again()
        except KeyboardInterrupt:
            break
    quit()
