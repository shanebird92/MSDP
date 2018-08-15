from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing, time, random, datetime
from selenium.webdriver.firefox.options import Options
import os, sys
import json


def test():
    # Firefox
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    # go to the dublinbus home page
    driver.get("http://137.43.49.51:8000/dublinbus/")
    time.sleep(0.2)

    data_path = os.path.dirname(os.path.abspath(__file__)) + "/../test_data/"
    file = data_path + "data.json"

    with open(file) as f:
        data = json.load(f)

    for key,value in sorted(data.items()):
        f = open("DataUI.report", "a")
        f.write("============ \n".format(key)) 
        f.close()

        for i in range(1, len(value)-1):
            start = str(int(value[i]))
            end = str(int(value[i+1]))
            message = ''

            # find the element that's start
            inputElement = driver.find_element_by_id('start')
            inputElement.clear()

            # send the key
            inputElement.send_keys(start)
            time.sleep(0.5)
            inputElement.send_keys(Keys.DOWN)
            message += "Start:'{:5}'->".format(start)
            time.sleep(0.5)

            # find the element that's destination
            inputElement = driver.find_element_by_id("destination")
            inputElement.clear()
            # input key values
            inputElement.send_keys(end)
            time.sleep(0.5)
            inputElement.send_keys(Keys.DOWN)
            message += "End: '{:5}'->".format(end)
            time.sleep(0.5)

            # find the element that's id is time
            inputElement = driver.find_element_by_id("time")
            # type in the search
            inputElement.send_keys("10:10")
            message += "Time clock '{}'->".format('10:10')
            time.sleep(0.2)

            # find the element that's id is submit
            buttonElement = driver.find_element_by_id("submit")
            buttonElement.click()
            time.sleep(0.2)
            tag = None
            try:
                # we have to wait for the page to refresh, the last thing that seems to be updated is the title
                WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, "route-div"))
                )

                # You should see "Cheers! Got it"
                message += "| Predicted Successfully! | DONE!"
                tag = True
            except:
                #input = driver.find_element_by_id("routes").text
                #print("value:", input.get_attribute('text'))
                #print("value:", input)
                try:
                    WebDriverWait(driver, 6).until(EC.text_to_be_present_in_element((By.ID, "routes"), 'No bus route!!')
                )
                    message += "| No bus route page! | Done"
                    tag = True
                except Exception as e:
                    #print("{}".format(str(e)))
                    message += "| NOT DONE!"
                    tag = False

            finally:
                f = open("DataUI.report", "a")
                f.write("{}: {:3} | {}\n".format(key, message, tag)) 
                #print("{}: {:3}".format(key, message), tag)
              
                f.close()
        #break
    driver.quit()

def main():
    test()


if __name__ == '__main__':
    main()
