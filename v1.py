# solver v1

import selenium.common.exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from difflib import SequenceMatcher
import concurrent.futures
from time import sleep
import pyautogui
import random
import torch
import os

from curves.humanclicker import HumanClicker

pyautogui.MINIMUM_DURATION = 0.001
hc = HumanClicker()


def load_model():
    model = torch.hub.load("WongKinYiu/yolov7", "custom", path_or_model="best.pt")
    model.conf = 0.15

    return model


def predict(model, path):
    results = model(path, size=128)

    return results


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def refresh(driver):
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div[2]")).click().perform()


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

    points = hc.get_points(start=pos, end=(1156, 827),
                           knotCounts=0)  # if this part is breaking for you its because these coords are hard coded (duh) and i havent gotten the above x + y coords correct yet

    for point in points:
        pyautogui.moveTo(point)

    sleep(0.08)

    pyautogui.click()
    driver.switch_to.default_content()

    iframe = None
    while iframe is None:
        try:
            iframe = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/iframe")
            sleep(2)
        except selenium.common.exceptions.NoSuchElementException:
            iframe = None

    driver.switch_to.frame(iframe)

    prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span").text[35:]
    print(prompt)


def solve(driver, model, prompt):
    img_els = driver.find_elements(By.CLASS_NAME, "border-focus")
    pairs = []

    for img_el in img_els:
        path = f"elements/{random.random()}.png"

        img_el.screenshot(path)
        pairs.append(f"{path}:{img_el}")

    for pair in pairs:
        path, img_el = pair.split(":")
        results = predict(model, path)
        os.remove(path)
        df = results.pandas().xyxy[0]

        for detection in df.loc[:, "name"].values:
            print(detection)
            sim = similar(prompt, detection)
            if sim >= 0.50:
                print(f"Detected {prompt}")

                points = hc.get_points(start=pyautogui.position(), end=(img_el.location["x"] + random.randint(20, 30), img_el.location["y"] + random.randint(20, 30)), knotCounts=0)  # todo check if this works

                for point in points:
                    pyautogui.moveTo(point)

                sleep(0.08)
                pyautogui.click()
                sleep(0.75)
            else:
                print(sim)

    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.XPATH, "/html/body/div[2]/div[8]")).perform()
    sleep(0.0765)
    actions.click().perform()

    sleep(0.75)

    try:
        button_txt = driver.find_element(By.XPATH, "/html/body/div[2]/div[8]/div").text
    except selenium.common.exceptions.NoSuchElementException:
        button_txt = "Done"

    return button_txt



def main():
    attempts = 0
    model = load_model()  # this model is not the full one, this one only can do toy rabbits, running horses, and rabbits in grass. i will train the full one once this is closer to done and i make the full dataset
    driver = uc.Chrome(headless=False)  # im using pyautogui for testing, so once thats gone you will be able to use headless
    driver.maximize_window()

    print("\n\n")

    load_cap(driver)
    button_txt = driver.find_element(By.XPATH, "/html/body/div[2]/div[8]/div").text
    while button_txt == "Skip" or "button_txt" == "Verify" and attempts <= 6:
        button_txt = solve(driver, model, driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span").text[35:])
        attempts += 1

        if button_txt == "Skip" and attempts > 2:
            refresh(driver)



    sleep(5)


if __name__ == '__main__':
    main()
