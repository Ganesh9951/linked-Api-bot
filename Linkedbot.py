from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LinkedInBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def go_to_profile_and_connect(self, profile_url):
        self.driver.get(profile_url)
        time.sleep(5)
        try:
            connect_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Connect')]")
            connect_button.click()
            time.sleep(2)
            send_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
            send_button.click()
        except Exception as e:
            print("Connect error:", e)

    def check_connection_and_message(self, profile_url, message):
        self.driver.get(profile_url)
        time.sleep(5)
        try:
            message_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Message')]")
            message_button.click()
            textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            textarea.send_keys(message)
            textarea.send_keys(Keys.ENTER)
        except Exception as e:
            print("Message error:", e)

    def close(self):
        self.driver.quit()
