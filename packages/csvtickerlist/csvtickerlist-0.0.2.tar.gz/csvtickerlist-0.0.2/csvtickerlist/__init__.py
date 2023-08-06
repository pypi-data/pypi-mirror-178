from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def GetCSVFile(mainFolder, seconds):
    #Using forward slash breaks chrome
    newPath = mainFolder.replace('/','\\') 
    print("CSV file will save to: ")
    print(newPath)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    prefs={"download.default_directory":newPath}
    options.add_experimental_option("prefs",prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
    options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.nasdaq.com/market-activity/stocks/screener')
    download_button = driver.find_element(By.CSS_SELECTOR, "button[class='nasdaq-screener__form-button--download ns-download-1']")
    print((download_button).text)
    download_button.click()
    time.sleep(seconds)
    driver.close()