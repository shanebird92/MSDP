from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing, time, random, datetime
from selenium.webdriver.firefox.options import Options


# Create a new instance of the Firefox driver
#fp = webdriver.FirefoxProfile('./firefoxProfile/')

def randomSelection(stations):
    '''
        randomly select stations
    '''
    num = len(stations)
    start = random.randint(0, num-5)
    end = random.randint(start+1, num-1)
    return stations[start], stations[end]

def singleOpen(pid):
    message = ''

    start_t = datetime.datetime.now()
    #stations = [767,768,769,770,771,772,773,774,775,776,777,779,780,781,782,783,784,785,786,793,7576,7586,7587,7588,328,1443,1444,1445,1647,1648,1649,1911,1913,1914,1805,1806,1660,1661,1662,1664,1665,1666,1807,7167,1808,7389,7025,4464,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1899,6107,6108,6109,6110,7020,7029,7038,7011,2171,7160,7047,7161,7162]
    stations = [395,396,397,398,399,400,4522,1934,2310,2311,2312,2313,2314,2315,2094,1406,1407,1409,2095,2096,2097,2099,2101,2102,2103,2332,2333,2334,4662,2335,2336,2337,2339,2420,2421,2423,2424,2447,5133,2596,2611,2602,2613,2614,2615,2535,2536,2616,2617,2557,4436,5008,4640,4347,2349,2351,2558,2559,2560,2561,2562,2564,4927,4928,2352,2573,2574,2575,4929,7460,4930,4931,7459]

    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    start, end = randomSelection(stations)


    # go to the google home page
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
    inputElement.send_keys("10:10")
    message += "Time clock '{}'->".format('10:10')
    time.sleep(0.2)

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
            print("{}: {}".format(pid, str(e)))
            message += "| NOT DONE!"
            tag = False

    finally:
        end_t = datetime.datetime.now()
        timeTaken = (end_t - start_t).seconds
        driver.quit()
        message = "Time: {} seconds | ".format(timeTaken) + message
        return ["PID {} {}".format(pid, message), tag]


def main():
    num = 10
    pass_count, fail_count = 0,0
    for i in range(num):
        single_test = singleOpen(i)
        if single_test[1] is True:
            pass_count += 1
        else:
            fail_count += 1
        print(single_test[0])
    print("Pass:{}, Fail: {}".format(pass_count, fail_count))

if __name__ == '__main__':
    main()
