import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

print(f"Using Python Version: {sys.version}")

# print selenium version
print("Selenium Version: " + webdriver.__version__)

service = Service(executable_path='chromedriver')

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--log-level=3')

# Provide the path of chromedriver present on your system.
driver = webdriver.Chrome(options=options)
driver.set_window_size(1280, 800)

# Send a get request to the url
driver.get('https://zaubara.com')
time.sleep(10)
driver.quit()
print("Done")
