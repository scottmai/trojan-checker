from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

import tt

    
def HomePage(driver: WebDriver):
    tt.clickButtonWithText("Schedule an Appointment or a COVID-19 Test") 
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//mat-checkbox[@formcontrolname='consent']"))
    ) 


def ScheduleTest():
    try:
        options = Options()
        # options.add_argument('--incognito')
        driver = webdriver.Chrome('./chromedriver.exe', options=options)

        driver.get("https://eshc-pncw.usc.edu/home.aspx")

        # driver.find_element_by_xpath('//button[@aria-label="Log in with your USC NetID"]').click()

        time.sleep(1)
        if "login.usc.edu" in driver.current_url:
            print('\nAUTH TIMEEEE\n')
            with open('credentials.txt', 'r') as ifile:
                user = ifile.readline().strip()
                password = ifile.readline().strip()
            driver.find_element_by_id('username').send_keys(user)
            driver.find_element_by_id('password').send_keys(password)
            driver.find_element_by_xpath('//button[@type="submit"]').click()
        print('waiting timee')
        elem = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'submit-button'))
        )
        elem.click()

        # assert "https://eshc-pncw.usc.edu/home.aspx" in driver.current_url 

        fillHomePage(driver)

    finally:
        time.sleep(10)
        driver.close()


ScheduleTest()