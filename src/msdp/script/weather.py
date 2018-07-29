import requests
import json 
import time 
import datetime
                                                                              
class Weather:
    ''' 
        Merged from Dan's previous code in dublinbus/view.py                  
    '''     
    def __init__(self, DEBUG=False):                                          
        self.__weather_api_url = \
            ("http://api.openweathermap.org/data/2.5/forecast/"
            "daily?id=7778677&mode=json&units=metric&cnt=5&APPID=19b104f014c41d11939f615df3a80edf")
        self.__debug = DEBUG                                                  

    @staticmethod
    def get_difference(forecastdate): 
        '''
            Get the different day's number with the given forecast date,
            comparing with the current date
            Return Value:
                    an integer from {0,1,2,3,4}
        '''
        # Default is current day, zero
        if len(forecastdate) == 0:
            return 0
        # calculate the time interval
        m2,d2,y2 = forecastdate.split('/')
        print(y2,m2,d2)
        y1 = datetime.datetime.now().year
        m1 = datetime.datetime.now().month
        d1 = datetime.datetime.now().day
        currenttime = datetime.datetime(y1, m1, d1)
        forecasttime = datetime.datetime(int(y2), int(m2), int(d2))
        time_difference = (forecasttime - currenttime).days
        return time_difference
                                                                              
    def get_weather_info(self, forecastdate):                              
        '''
            get weather information on Rain and Sun                           
                Return Value: [Rain, Sun]                                     
        '''
        time_difference = Weather.get_difference(forecastdate)
        weather = requests.get(self.__weather_api_url).json()                   
        # Default weather values is None-Rain (rain = 0) and                  
        # None-Sunny (sun = 0) day                                            
        rain, sun = 0, 0
        if (time_difference>=0 and time_difference<=4):                       
            #key:weather description; value: rain sun                         
            weather_dic = {'Clouds':[0,0],                                    
                           'Drizzle':[1,0],                                   
                           'Clear':[0,1],
                           'Fog':[0,0],
                           'Mist':[0,0],
                           'Rain':[1,0],
                           'Snow':[1,0],
                           'Thundestorm':[1,0]}                               
            try:
                weather_info = weather['list'][time_difference]['weather'][0]['main']      
                rain, sun = weather_dic.get(weather_info)                     
            except TypeError as e:
                if self.__debug:                                              
                    print(str(e))
                pass
        return [rain, sun]

def main():
    # Temporary testing
    my = Weather(DEBUG=True)
    for mydate in ['2018-07-19', '2018-07-20','2018-07-21','2018-07-22', '2018-07-23']:
        weather = my.get_weather_info(mydate)
        print("day {}: rain: {}, sun:{}".format(mydate, weather[0], weather[1]))

if __name__ == '__main__':
    main()
