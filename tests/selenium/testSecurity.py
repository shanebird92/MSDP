import time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By

def test():
    # Open a browser and access analytics first
    firefox = webdriver.Firefox()
    firefox.get("http://137.43.49.51:8000/analytics/")

    ret = False
    # Verify that the without login, data analytics page can not be found
    elements = firefox.find_elements_by_tag_name("h2")
    for e in elements:
        if e.text == "Page not found":
            ret = True
        else:
            print("FAIL: the secure analytics page can be found without login!")
            sys.exit()
    time.sleep(1)
    # Verify that the 404 page will be displayed if accessing the page with
    # incorrect url
    firefox.get("http://137.43.49.51:8000/dublinbbs/")
    elements = firefox.find_elements_by_tag_name("h2")
    for e in elements:
        if e.text == "Page not found":
            ret = True
        else:
            print("FAIL: 404 page can not be found!")
            sys.exit()

    # Enter login page and input username/password to enter the analytics page
    firefox.get("http://137.43.49.51:8000/dublinbus/")
    element = firefox.find_element_by_xpath('//a/strong[text()="Data Analytics"]')
    element.click()

    # Login and enter analytics page
    username_element = firefox.find_element_by_id("id_username")
    username_element.send_keys("MSDP")
    time.sleep(1)
    password_element = firefox.find_element_by_id("id_password")
    password_element.send_keys("MSDPUCD123")
    time.sleep(1)
    login_element = firefox.find_element_by_xpath('//button[text()="Login"]')
    login_element.click()

    # Verify entered analytics page successfully
    element = firefox.find_element_by_xpath('//div[@class="relative"]/form[@class="form1"]/h3')
    if "Display all Trip IDs with given month" in element.text:
        ret = True
    else:
        print("FAIL: can not enter analytics page with login")

    if ret:
        print("PASS: Page Security Testing is completed")

    time.sleep(1)
    firefox.quit()


if __name__ == '__main__':
    test()
