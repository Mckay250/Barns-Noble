import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from gmail import search_message, get_message

RESET_PASSWORD_SUBJECT = "Your Request to Reset Your Barnes & Noble Password"

def main(user_email : str) -> None:

    PATH = 'C:\\chromedriver.exe'
    
    driver = webdriver.Chrome(PATH)

    # navigate to the website url
    driver.get("https://www.barnesandnoble.com/h/books/browse")

    # maximize the browser window
    driver.maximize_window()

    # over on the "My Account dropdown"
    account_dropdown = driver.find_element_by_class_name("dropdown")
    ActionChains(driver).move_to_element(account_dropdown).perform()

    # click on the sign in button
    driver.find_element_by_class_name('rhf-sign-in').click()

    # switch to the sign in frame
    time.sleep(2)
    sign_in_iframe_path = '/html/body/div[6]/div/iframe'
    driver.switch_to.frame(driver.find_element_by_xpath(sign_in_iframe_path))

    # click on the forgot password link
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#loginForgotPassword"))).click()

    # switch back to the default/main frame
    driver.switch_to.parent_frame()

    # switch to the password reset frame
    time.sleep(2)
    password_reset_xpath = '/html/body/div[7]/div/iframe'
    driver.switch_to.frame(driver.find_element_by_xpath(password_reset_xpath))

    # fill in the email field and submit the form
    driver.find_element_by_id('email').send_keys(user_email)
    driver.find_element_by_id('resetPwSubmit').submit()

    try:
        # print error message if there is an error        
        time.sleep(2)
        res = driver.find_element_by_class_name('emphasis').text
        print("ERROR: ", res)
    except NoSuchElementException:
        # server did not return an error

        # switch back to the parent frame
        driver.switch_to.parent_frame()

        # confirm the password reset sumbition
        time.sleep(2)
        confirm_password_reset_xpath = '/html/body/div[8]/div/iframe'
        driver.switch_to.frame(driver.find_element_by_xpath(confirm_password_reset_xpath))
        driver.find_element_by_id('resetPwSubmit').submit()
        print("Check your email for the reset link")

        # close the browser
        driver.quit()

def print_email_message(search_string : str) -> str:
    """
        Returns first the email body of the search string
        input -> search_string (str)
        output -> str
    """

    # get list message ids with the search phrase
    messages_result = search_message(search_string=search_string)

    # return the first message in the list if messages exist
    if messages_result:
        return get_message(messages_result[0])
    else:
        return 'No messages found'


if __name__=='__main__':
    email = input('Enter email here: ')
    main(email)
    time.sleep(20)
    print(print_email_message(RESET_PASSWORD_SUBJECT))
