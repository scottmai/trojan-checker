import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.message import EmailMessage

QR_CODE_PATH = './qrcode.png'


def clickButtonWithText(driver: WebDriver, text):
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{text}')]"))
    )
    elem.click()


def typeInput(driver: WebDriver, name, text):
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f'//input[@formcontrolname="{name}"]'))
    )
    print(elem)
    elem.send_keys(text)


def fillVaccinatedPage(driver: WebDriver):
    clickButtonWithText(driver, 'Yes')

    clickButtonWithText(driver, 'Next')


def fillIsolationPage(driver: WebDriver):
    clickButtonWithText(driver, 'No')

    clickButtonWithText(driver, 'Next')


def fillFirstPage(driver: WebDriver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), 'No')]"))
    )
    nos = driver.find_elements_by_xpath("//*[contains(text(), 'No')]")
    for no in nos:
        no.click()

    clickButtonWithText(driver, 'Next')


def fillSecondPage(driver: WebDriver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), 'No')]"))
    )
    nos = driver.find_elements_by_xpath("//*[contains(text(), 'No')]")
    for no in nos:
        no.click()

    clickButtonWithText(driver, 'Next')


def fillReviewPage(driver: WebDriver, guest):
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//mat-checkbox[@formcontrolname='consent']"))
    )
    elem.click()

    button_text = 'Next' if guest else 'Submit'

    # while button is disabled, click elem
    while not driver.find_element_by_xpath(f"//button[contains(@class, 'btn-submit')]").is_enabled():
        elem.click()
        time.sleep(.5)

    clickButtonWithText(driver, button_text)


def getQRCode(driver: WebDriver):
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'day-pass'))
    )
    elem.screenshot(QR_CODE_PATH)


def fillVisitorInfoPage(driver: WebDriver):
    typeInput(driver, "firstName", "Troy")

    typeInput(driver, "lastName", "Galicia")

    typeInput(driver, "phone", "7205604040")

    # with open('email.txt', 'r') as ifile:
    #     email = str(int(ifile.read()) + 1)

    # with open('email.txt', 'w') as ofile:
    #     print(email, end='', file=ofile)

    # email += '@urmom.com'
    email = "maiscottie@gmail.com"

    typeInput(driver, "email", email)

    typeInput(driver, "location", "SAL")

    clickButtonWithText(driver, 'Submit request')


def send_email():
    # Create the container for the image
    msg = EmailMessage()
    msg['Subject'] = 'Your QR Code'
    msg['From'] = 'trojancheckbot@ur.mom'
    msg['To'] = 'scottmai702@gmail.com'

    # with open(QR_CODE_PATH, 'rb') as f:
    #     file_data = f.read()
    # msg.add_attachment(file_data, maintype='image', subtype=imghdr.what(None, file_data))

    with smtplib.SMTP('localhost', 1025, 'localhost') as s:
        s.send_message(msg)


def guestLogin():
    try:
        options = Options()
        options.add_argument('--incognito')
        driver = webdriver.Chrome('./chromedriver.exe', options=options)

        driver.get("https://trojancheck.usc.edu/")

        assert "https://trojancheck.usc.edu/" in driver.current_url

        clickButtonWithText(driver, "Continue as a Guest")

        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'submit-button'))
        )
        elem.click()

        clickButtonWithText(driver, 'Start screening')

        fillVaccinatedPage(driver)

        fillFirstPage(driver)

        fillSecondPage(driver)

        fillReviewPage(driver, guest=True)

        fillVisitorInfoPage(driver)

        getQRCode(driver)

    finally:
        time.sleep(10)

        driver.close()


def USCLogin():
    try:
        options = Options()
        options.add_argument('--incognito')
        # options.add_argument(
        #     "user-data-dir=C:\\Users\\Scottie\\AppData\\Local\\Google\\Chrome\\User Data")
        # options.add_argument('profile-directory=Profile 3')
        driver = webdriver.Chrome('./chromedriver.exe', options=options)

        driver.get("https://trojancheck.usc.edu/")

        assert "https://trojancheck.usc.edu/" in driver.current_url

        driver.find_element_by_xpath(
            '//button[@aria-label="Log in with your USC NetID"]').click()

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

        driver.find_element_by_xpath(
            '//button[@aria-label="Begin wellness assessment"]').click()

        clickButtonWithText(driver, 'Start screening')

        fillVaccinatedPage(driver)

        fillIsolationPage(driver)

        fillFirstPage(driver)

        # fillSecondPage(driver)
        # fillSecondPage(driver)

        fillReviewPage(driver, guest=False)

        # fillVisitorInfoPage(driver)

        code = getQRCode(driver)
        print(code)

    finally:
        time.sleep(10)
        driver.close()


if __name__ == '__main__':
    USCLogin()
    # guestLogin()
    # send_email()
