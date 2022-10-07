# solver v1

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from colorama import Style, Fore, init
import undetected_chromedriver as uc
import selenium.common.exceptions
from time import sleep
import pyautogui
import random
import torch
import os

from curves.humanclicker import HumanClicker

pyautogui.MINIMUM_DURATION = 0.001
init(autoreset=True)
hc = HumanClicker()

yellow = f"{Style.BRIGHT}{Fore.YELLOW}"
green = f"{Style.BRIGHT}{Fore.GREEN}"
purple = f"{Style.BRIGHT}{Fore.MAGENTA}"


def load_model():
    model = torch.hub.load("WongKinYiu/yolov7", "custom", path_or_model="best.pt")
    model.conf = 0.15

    return model


def predict(model, path):
    results = model(path, size=128)

    return results


def refresh(driver):
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div[2]")).click().perform()
    print("Refreshed")  # todo if prompt in supported prompt list then dont refresh


def load_cap(driver):
    driver.get("https://maximedrn.github.io/hcaptcha-solver-python-selenium/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/iframe")))

    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/iframe"))

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[1]/div/div/div[1]")))
    sleep(0.3)

    # box_dim = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div/div/div[1]")
    #
    # box_el_x = box_dim.location["x"]
    # box_el_y = box_dim.location["y"]
    # box_el_width = box_dim.size["width"] // 2
    # box_el_height = box_dim.size["height"] // 2
    #
    # box_mid = (box_el_x + box_el_width, box_el_y + box_el_height)

    # todo x and y for above are broken, must be something weird with iframes

    points = hc.get_points(start=pyautogui.position(), end=(1156, 827), knotCounts=0)  # if this part is breaking for you its because these coords are hard coded (duh) and i havent gotten the above x + y coords correct yet

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
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span")))
    prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span").text[35:]
    print(f"{yellow}Prompt: {prompt}")


def solve(driver, model, prompt):
    img_els = driver.find_elements(By.CLASS_NAME, "border-focus")
    correct_images = set()

    for img_el in img_els:
        path = f"elements/{random.random()}.png"

        img_el.screenshot(path)

        results = predict(model, path)
        os.remove(path)
        df = results.pandas().xyxy[0]

        for detection in df.loc[:, "name"].values:
            if detection in prompt:
                print(f"{yellow}Detected {prompt}")
                correct_images.add(img_el)
                break


    for img_el in correct_images:
        #points = hc.get_points(start=pyautogui.position(), end=(img_el.location["x"] + random.randint(20, 30), img_el.location["y"] + random.randint(20, 30)), knotCounts=0)  # todo fix element locations

        # for point in points:
        #     pyautogui.moveTo(point)

        actions = ActionChains(driver)
        actions.click(img_el).perform()
        sleep(0.2)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[8]")))

    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.XPATH, "/html/body/div[2]/div[8]")).perform()
    sleep(0.0765)
    actions.click().perform()


def main():
    attempts = 1
    model = load_model()
    driver = uc.Chrome(headless=False)  # im using pyautogui for testing, so once thats gone you will be able to use headless
    driver.maximize_window()

    print("\n\n")

    load_cap(driver)


    while True:
        sleep(2)
        print(f"{yellow}Solving. Attempt: {attempts}")
        try:
            prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span").text[35:]
            print(prompt)
        except:
            break

        button_txt = solve(driver, model, prompt)

        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/iframe"))
            checked = driver.find_element(By.ID, "checkbox").get_attribute("aria-checked")
            if checked == "true":
                break
        except:
            pass

        attempts += 1

        if button_txt == "Skip" and attempts > 3:
            refresh(driver)

    driver.switch_to.default_content()
    token = driver.execute_script("return hcaptcha.getResponse()")
    print("Finished")
    print(f"Token: {token}")


    sleep(5)


if __name__ == '__main__':
    main()
