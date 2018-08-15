from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing, time, random, datetime
from selenium.webdriver.firefox.options import Options

def randomSelection(stations):
    '''
        randomly select stations
    '''
    num = len(stations)
    start = random.randint(0, num-5)
    end = random.randint(start+1, num-1)
    return stations[start], stations[end]

def singleOpen(browser):
    message = ''

    start_t = datetime.datetime.now()
    stations = [767,768,769,770,771,772,773,774,775,776,777,779,780,781,782,783,784,785,786,793,7576,7586,7587,7588,328,1443,1444,1445,1647,1648,1649,1911,1913,1914,1805,1806,1660,1661,1662,1664,1665,1666,1807,7167,1808,7389,7025,4464,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1899,6107,6108,6109,6110,7020,7029,7038,7011,2171,7160,7047,7161,7162]

    if browser is 'firefox':
        # Firefox
        options = Options()
        #options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options)
    elif browser is 'chrome':
        # Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=options)
        driver.set_window_size(1920, 1080)
    elif browser is 'safari':
        # Safari
        #options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        driver = webdriver.Safari()
        driver.set_window_size(1920, 1080)

    start, end = randomSelection(stations)


    # go to the dublinbus home page
    driver.get("http://137.43.49.51:8000/dublinbus/")

    # the page is ajaxy so the title is originally this:
    time.sleep(0.2)

    # find the element that's start
    inputElement = driver.find_element_by_id('start')

    # send the key
    inputElement.send_keys(start)
    time.sleep(0.5)
    inputElement.send_keys(Keys.DOWN)
    message += "Start point on '{}' ->".format(start)
    time.sleep(1.2)

    # find the element that's destination
    inputElement = driver.find_element_by_id("destination")
    # input key values
    inputElement.send_keys(end)
    time.sleep(0.5)
    inputElement.send_keys(Keys.DOWN)
    message += "End point on '{}'->".format(end)
    time.sleep(1.2)

    '''
    # find the element that's id is datepicker
    inputElement = driver.find_element_by_id("datepicker")
    # type in the search
    inputElement.send_keys("8/1/2018")
    time.sleep(1)
    '''

    # find the element that's id is time
    inputElement = driver.find_element_by_id("time")
    # type in the search
    
    if browser is 'firefox':
        timeStr = "10:10"
    elif browser is 'chrome':
        timeStr = "10:10AM"
    elif browser is 'safari':
        timeStr = "10:10"
    try:
        inputElement.send_keys(timeStr)
        message += "Time clock '{}'->".format('10:10')
        time.sleep(0.2)
    except:
        print("Fail to input Time")

    # find the element that's id is submit
    buttonElement = driver.find_element_by_id("submit")
    buttonElement.click()
    message += "Clicked Submit Button"
    time.sleep(0.2)
    tag = None
    try:
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "route-div"))
        )

        # You should see "Cheers! Got it"
        message += "| Find out the detail page! | Done"
        tag = True
    except:
        #input = driver.find_element_by_id("routes").text
        #print("value:", input.get_attribute('text'))
        #print("value:", input)
        try:
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "routes"), 'No bus route!!')
        )
            message += "| Find out the No bus route page! | Done"
            tag = True
        except Exception as e:
            print("{}".format(str(e)))
            message += "| NOT DONE!"
            tag = False

    finally:
        end_t = datetime.datetime.now()
        timeTaken = (end_t - start_t).seconds
        driver.quit()
        message = "Time: {} seconds | ".format(timeTaken) + message
        return ["{}: {}".format(browser, message), tag]


def main():
    #browser = 'firefox'
    #browser = 'chrome'
    browser = 'safari'
    result = singleOpen(browser)
    print(result)

if __name__ == '__main__':
    main()
