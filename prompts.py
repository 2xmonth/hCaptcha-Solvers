from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import concurrent.futures
from time import sleep
import random
import os

workers = 1


# one thing that hcaptcha might be doing is making it so each ip can only get a couple prompts out of the whole list within a time period. the sleep tries to combat that, but its only 80 seconds

def extract():
    while True:
        print("Loading driver")
        driver = uc.Chrome(headless=False)
        driver.maximize_window()

        actions = ActionChains(driver)
        driver.get("https://maximedrn.github.io/hcaptcha-solver-python-selenium/")
        sleep(1)
        driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/iframe"))

        actions.move_to_element(driver.find_element(By.ID, "checkbox")).click().perform()
        sleep(3)
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/iframe"))
        prompt_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span")
        prompt = prompt_element.text

        final_list = [word for word in prompt.split() if word not in ["Please", "click", "each", "image", "containing"]]  # just in case the prompt gets weird
        prompt = " ".join(final_list)

        image_elements = driver.find_elements(By.CLASS_NAME, "border-focus")
        try:
            os.mkdir(f"hcaptcha-imgs/{prompt}")
        except:
            pass

        for element in image_elements:
            if len(os.listdir(f"hcaptcha-imgs/{prompt}/")) <= 200:
                element.screenshot(f"hcaptcha-imgs/{prompt}/{random.random()}.png")
                print(f"Prompt \"{prompt}\" now has {len(os.listdir(f'hcaptcha-imgs/{prompt}/'))} possible images.")

        with open("prompts.txt", "r") as r:
            prompt = f"{prompt}, hyperrealistic\n"
            lines = set(r.readlines())
            if prompt not in lines:
                with open("prompts.txt", "a") as a:
                    print(f"Encountered new prompt \"{prompt}\"")
                    a.write(prompt)

        driver.quit()

        sleep(80)  # delay so that you can just leave this running while you are doing something else and you will hopefully get new prompts


with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
    for i in range(workers):
        executor.submit(extract)
