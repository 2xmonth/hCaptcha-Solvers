# solver v1
import selenium.common.exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import concurrent.futures
from time import sleep
import pyautogui
import random
import os

from curves.humanclicker import HumanClicker

pyautogui.MINIMUM_DURATION = 0.001
hc = HumanClicker()


def load_cap(driver):
    driver.get("https://maximedrn.github.io/hcaptcha-solver-python-selenium/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/iframe")))


    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/iframe"))
    sleep(0.3)
    pos = pyautogui.position()

    box_dim = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div/div/div[1]")

    box_el_x = box_dim.location["x"]
    box_el_y = box_dim.location["y"]
    box_el_width = box_dim.size["width"] // 2
    box_el_height = box_dim.size["height"] // 2

    box_mid = (box_el_x + box_el_width, box_el_y + box_el_height)

    # todo x and y for above are broken, must be something weird with iframes

    points = hc.get_points(start=pos, end=(1156, 827), knotCounts=0)  # if this part is breaking for you its because these coords are hard coded (duh) and i havent gotten the above x + y coords correct yet


    for point in points:
        pyautogui.moveTo(point)

    sleep(0.08)

    pyautogui.click()
    driver.switch_to.default_content()

    iframe = None
    while iframe is None:
        try:
            iframe = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/iframe")
            sleep(1)
        except selenium.common.exceptions.NoSuchElementException:
            iframe = None



    driver.switch_to.frame(iframe)

    prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span").text
    print(prompt)


def main():
    driver = uc.Chrome(headless=False)  # im using pyautogui for testing, so once thats gone you will be able to use headless
    driver.maximize_window()
    load_cap(driver)


if __name__ == '__main__':
    main()





