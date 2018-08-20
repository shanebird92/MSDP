import os, math, time
import csv, json
import pandas as pd
import requests
import urllib
from msdp.script import ann, weather


class ChangeBus:
    def __init__(self, startID, endID, targetTime, rain, sun, DEBUG=False, MODE='fast', SN=1):
        self.__data_path = os.path.dirname(os.path.abspath(__file__)) + "/../../../data"
        self.__startid = startID
        self.__endid = endID
        self.__targettime = targetTime
        self.__rain = rain
        self.__sun = sun
        self.__debug = DEBUG
        self.__mode = MODE
        # The maximum number of solutions
        self.__sn = SN
        # The maximum distance for walking (KM)
        self.__distance_accuracy = 1.5
        # The maximum search number for calling findLine()
        self.__maximum_search = 30

        # stop -> lines
        lines_json_file = '{}/stops.json'.format(self.__data_path)
        self.__all_lines = json.loads(open(lines_json_file).read())
        # stop -> address
        address_json_file = '{}/stopToAddressName.json'.format(self.__data_path)
        self.__all_addresses = json.loads(open(address_json_file).read())
        # stop -> station name
        station_json_file = '{}/stopToStationName.json'.format(self.__data_path)
        self.__all_stations = json.loads(open(station_json_file).read())
        # address -> all stops
        stops_json_file = '{}/addressStops.json'.format(self.__data_path)
        self.__all_stops = json.loads(open(stops_json_file).read())
        # pre-stored solution data
        try:
            solution_json_file = '{}/routesData.json'.format(self.__data_path)
            self.__solutionRoutes = json.loads(open(solution_json_file).read())
        except Exception as e:
            if self.__debug:
                print("Can not init solutionRoutes due to file openning issue")
            self.__solutionRoutes = {}
     

        # non-available stops
        self.__discard_stops = []

    def convertName(self,busline, opposite=False):
        if not opposite:
            busline = busline.replace("_0", "_a")
            busline = busline.replace("_1", "_b")
        else:
            busline = busline.replace("_0", "_b")
            busline = busline.replace("_1", "_a")
        return busline

    @staticmethod
    def __greatcircledist(p1, p2):
        '''This Great-circle distance between 2 positions is just based on
           Latitude and Longitude
           - Input Value: [lat1,long1], [lat2,long2]
           - Return Value: distance (km)
        '''
        R = 6371
        lat1 = math.radians(p1[0])
        lat2 = math.radians(p2[0])
        long1 = math.radians(p1[1])
        long2 = math.radians(p2[1])

        dlon = long2 - long1
        dlat = lat2 - lat1
        a = (math.sin(dlat/2)**2 + \
                math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2)
        c = math.atan2(math.sqrt(a), math.sqrt(1-a)) * 2
        return R * c

    @staticmethod
    def greatcircledist(p1, p2):
        return ChangeBus.__greatcircledist(p1, p2)

    def getDistance(self, start, end):
        stop_file = '{}/stop_latlong.json'.format(self.__data_path)
        stops = json.loads(open(stop_file).read())
        startID = str(int(start))
        endID = str(int(end))
        if startID in stops.keys():
            start_lat, start_lng = stops[startID]
        else:
            if self.__debug:
                print("Start station {} is not in stop keys list".format(startID))
            if startID not in self.__discard_stops:
                self.__discard_stops.append(startID)
            return float("inf")

        if endID in stops.keys():
            end_lat, end_lng = stops[endID]
        else:
            if self.__debug:
                print("End station {} is not in stop keys list".format(endID))
            if endID not in self.__discard_stops:
                self.__discard_stops.append(endID)
            return float("inf")
        return self.__greatcircledist([start_lat, start_lng], [end_lat, end_lng])

    def getSameStops(self, list1, list2):
        return list(set(list1).intersection(list2))

    def getstopids(self,line, start='', end=''):
        time_table_file = '{}/{}_timeTable.csv'.format(self.__data_path, line)
        try:
            df = pd.read_csv(time_table_file, index_col=0)
        except Exception as e:
            if self.__debug:
                print("WARNING: Line {} {}".format(line, str(e)))
            if len(start) > 0 or len(end) > 0:
                return []
            if len(closestStart) > 0 or len(closestEnd) > 0:
                return [], float("inf")
        all_stops = df.ix[0].tolist()

        if len(start) > 0 and float(start) in all_stops:
            return all_stops[all_stops.index(float(start)):]
        elif len(end) > 0 and float(end) in all_stops:
            return all_stops[:all_stops.index(float(end))+1]
        elif len(start) == 0 and len(end) == 0:
            return all_stops
        else:
            return []

    def findClosestStops(self, line1Stops, line2Stops):
        min_distance = float("inf")
        min_distance_stops = []
        for line1_stop in line1Stops:
            if str(int(line1_stop)) in self.__discard_stops:
                continue
            for line2_stop in line2Stops:
                if str(int(line2_stop)) in self.__discard_stops:
                    continue
                distance = self.getDistance(line1_stop, line2_stop)
                #print("findClosestStops():{}".format(distance))
                if distance < min_distance:
                    min_distance = distance
                    min_distance_stops = [int(line1_stop), int(line2_stop)]
        return min_distance, min_distance_stops

    def findLine(self, startID='', endID=''):
        '''
            find out the possible bus lines related to start and end stoppoints
        '''
        if startID == '':
            startID = self.__startid
        if endID == '':
            endID = self.__endid

        if self.__debug:
            print("findLine(): startID={}, endID={}".format(startID, endID))
        json_file = '{}/stops.json'.format(self.__data_path)
        all_lines = json.loads(open(json_file).read())
        if str(startID) in all_lines.keys():
            startID_lines = all_lines[str(startID)]
        else:
            if self.__debug:
                print("Start station {} is not in all line".format(startID))
            return []

        if str(endID) in all_lines.keys():
            endID_lines = all_lines[str(endID)]
        else:
            if self.__debug:
                print("End station {} is not in all line".format(endID))
            return []


        new_startID_lines = []
        new_endID_lines = []
        for id in startID_lines:
            new_startID_lines.append(self.convertName(id))
        for id in endID_lines:
            new_endID_lines.append(self.convertName(id))

        if self.__debug:
            print("findLine(): start ID Lines {}, end ID Lines {}".format(new_startID_lines, new_endID_lines))

        solutions = []
        for start_line in new_startID_lines:
            for end_line in new_endID_lines:
                s_line_ids = self.getstopids(start_line, start=str(float(startID)))
                if len(s_line_ids) == 0:
                    if self.__debug:
                        print("findLine(): start Lines {} can't found {}".format(start_line, startID))
                    break
                e_line_ids = self.getstopids(end_line, end=str(float(endID)))
                if len(e_line_ids) == 0:
                    if self.__debug:
                        print("findLine(): end Lines {} can't found {}".format(end_line, endID))
                    continue
                distance, closestStops = self.findClosestStops(s_line_ids, e_line_ids)
                if self.__debug:
                    print("---"*5)
                    print("findLine():{} {}".format(startID, s_line_ids))
                    print("findLine():{} {}".format(endID, e_line_ids))
                    print("findLine():{} {}".format(distance, closestStops))
                if distance > self.__distance_accuracy:
                    continue

                if not self.verifyPredictionAvailable(startID, closestStops[0]):
                    if self.__debug:
                        print("{} and {} cannot be predicted".format(startID, closestStops[0]))
                    break
                elif not self.verifyPredictionAvailable(closestStops[1], endID):
                    if self.__debug:
                        print("{} and {} cannot be predicted".format(closestStops[1], endID))
                    continue

                if distance != float("inf"):   
                    if self.__mode == 'fast' and self.verifyAvailableLine(startID, closestStops[0], closestStops[1], endID):
                        solutions.append([startID, closestStops[0], closestStops[1], endID, distance])
                        return solutions
                    else:
                        solutions.append([startID, closestStops[0], closestStops[1], endID, distance])
        return solutions

    def verifyPredictionAvailable(self, startID, stopID):
        '''
            Make sure the certain prediction is available
        '''
        targettime = self.__targettime
        rain = self.__rain
        sun = self.__sun
        my = ann.Ann(int(startID),int(stopID),targettime,rain,sun, DEBUG=self.__debug)
        solutions = my.get_all_prediction()
        if len(solutions) == 0:
            return False
        for solution in solutions:
            if solution['isFileExist']:
                return True
        return False

    def verifyAvailableLine(self, startID, stopID, secondStartID, secondStopID):
        targettime = self.__targettime
        rain = self.__rain
        sun = self.__sun
        isAvailable = False
        my1 = ann.Ann(int(startID),int(stopID),targettime,rain,sun, DEBUG=self.__debug)
        solution1 = my1.get_all_prediction()
        if len(solution1) == 0:
            return False
        else:
            for solution in solution1:
                if solution['travelTime'] > 0:
                    isAvailable = True
                    break
        my2 = ann.Ann(int(secondStartID),int(secondStopID),targettime,rain,sun, DEBUG=self.__debug)
        solution2 = my1.get_all_prediction()
        if len(solution2) == 0:
            return False
        else:
            for solution in solution2:
                if solution['travelTime'] > 0:
                    isAvailable = True
                    break
        return isAvailable

    def _sortDistanceByStops(self, ID, stops):
        distance_dict = {}
        for stop in stops:
            distance = self.getDistance(float(stop), float(ID))
            distance_dict[distance] = stop
        sorted_stops = []
        sorted_distance = []
        for distance in sorted(distance_dict.keys()):
            sorted_distance.append(distance)
            sorted_stops.append(distance_dict[distance])
        return sorted_stops, sorted_distance
        
    def getCloserRoute(self):
        startID = self.__startid
        endID = self.__endid
        all_stops = self.__all_stops
        all_lines = self.__all_lines
        all_addresses = self.__all_addresses
        all_stations = self.__all_stations

        # Search start point from area closer to startID
        if str(startID) in all_addresses.keys() and all_addresses[str(startID)] in all_stops:
            start_stops = all_stops[all_addresses[str(startID)]]
            sorted_start_stops, sorted_start_distance = self._sortDistanceByStops(startID, start_stops)
        else:
            if self.__debug:
                print("WARNING: startID {} not in address dict".format(startID))
            sorted_start_stops = [startID]
            sorted_start_distance = [0]

        # Search end point from area closer to endID
        if str(endID) in all_addresses.keys() and all_addresses[str(endID)] in all_stops:
            end_stops = all_stops[all_addresses[str(endID)]]
            sorted_end_stops, sorted_end_distance = self._sortDistanceByStops(endID, end_stops)
        else:
            if self.__debug:
                print("WARNING: endID {} not in address dict".format(endID))
            sorted_end_stops = [endID]
            sorted_end_distance = [0]

        other_solutions = []
        is_available = False
        maximum_search = self.__maximum_search
        for i in range(len(sorted_start_stops)):
            if sorted_start_distance[i] > self.__distance_accuracy:
                if self.__debug:
                    print("Walk {} KM from {} to {} taking first bus is too long".format(round(sorted_start_distance[i],3), sorted_start_stops[i], sorted_start_stops[0]))
                continue
            # walking time from somewhere to start station (second)
            startWalkTime = (sorted_start_distance[i]/5)*3600
            for j in range(len(sorted_end_stops)):
                if sorted_end_distance[j] > self.__distance_accuracy:
                    if self.__debug:
                        print("Walk {} KM from {} to {} to arrive dest is too long".format(round(sorted_end_distance[j],3), sorted_end_stops[j], sorted_end_stops[0]))
                    continue
                # walking time from some station to end station(second)
                endWalkTime = (sorted_end_distance[j]/5)*3600
                solutions = self.getRoute(startID=sorted_start_stops[i], endID=sorted_end_stops[j], startWalkTime=startWalkTime, endWalkTime=endWalkTime)    
              
                if len(solutions) > 0:
                    other_solutions.append([startID, sorted_start_stops[i], round(sorted_start_distance[i],3), solutions, sorted_end_stops[j], sorted_end_stops[0], round(sorted_end_distance[j],3)])
                    # Update routes Data file with the first calculation
                    key = "{},{}".format(startID, endID)
                    value = [[int(startID), int(sorted_start_stops[i]),
                              int(solutions[0]['firstLineTransferStop']),
                              int(solutions[0]['secondLineTransferStop']),
                              int(sorted_end_stops[j]),
                              int(sorted_end_stops[0])],
                              round(sorted_start_distance[i],3),
                              round(solutions[0]['transferDistance'],3),
                              round(sorted_end_distance[j],3)]
                  
                    ret = self.updateData(key, value)
                    if ret:
                        print("Updated Routes Data File!")
                    else:
                        print("Fail to Routes Data File!")
                if self.__mode == 'fast' and len(other_solutions) >= self.__sn:
                    return other_solutions
                maximum_search -= 1
              
            if is_available or maximum_search <= 0:
                break
        return other_solutions

    def getRoute(self, startID='', endID='', startWalkTime=0, endWalkTime=0):
        candidateLines = self.findLine(startID=startID, endID=endID)
        isSolutionAvailable = False
        min_distance = float("inf")
        targettime = self.__targettime + startWalkTime
        rain = self.__rain
        sun = self.__sun
        solutions = []
        min_first_endID, min_second_startID = 0,0
        for Line in candidateLines:
            first_startID = Line[0]
            first_endID = Line[1]
            second_startID = Line[2]
            second_endID = Line[3]
            distance = Line[4]
            solution = {}

            if distance > self.__distance_accuracy:
                min_distance = min(min_distance, distance)
                min_first_endID, min_second_startID = first_endID, second_startID
                continue
            # First Line
            solution['firstLineTransferStop'] = int(first_endID)
            my1 = ann.Ann(int(first_startID),int(first_endID),targettime,rain,sun, DEBUG=self.__debug)
            my1_results = my1.get_all_prediction()
            solution['firstLines'] = []
            for result in my1_results:
                if result['travelTime'] > 0:
                    solution['firstLines'].append(result)
                    targettime = result['pairArrTime'][-1]
                    break
            if len(solution['firstLines']) == 0:
                continue
      
            # Second Line
            solution['secondLineTransferStop'] = int(second_startID)
            my2 = ann.Ann(int(second_startID),int(second_endID),targettime,rain,sun, DEBUG=self.__debug)
            my2_results = my2.get_all_prediction()
            solution['secondLines'] = []
            for result in my2_results:
                if result['travelTime'] > 0:
                    solution['secondLines'].append(result)
                    break
            if len(solution['secondLines']) == 0:
                continue

            solution['transferDistance'] = distance
            solutions.append(solution)
            isSolutionAvailable = True

            if self.__mode == 'fast' and len(solutions) >= self.__sn:
                break
                
        if not isSolutionAvailable and len(candidateLines) > 0:
            if self.__debug:
                print("Walking distance from {} -> {} is too long when transferring Buses: {} KM".format(first_endID, second_startID, round(min_distance, 3)))
        return solutions

    def dataSearchRoute(self, route):
        startWalkTime = (route[1]/5) * 3600
        transferWalkTime = (route[2]/5) * 3600
        endWalkTime = (route[3]/5) * 3600
        targettime = self.__targettime + startWalkTime
        rain = self.__rain
        sun = self.__sun

        first_startID = route[0][1]
        first_endID = route[0][2]
        second_startID = route[0][3]
        second_endID = route[0][4]

        solutions = []
        solution = {}
        # First Line
        solution['firstLineTransferStop'] = int(first_endID)
        my1 = ann.Ann(int(first_startID),int(first_endID),targettime,rain,sun, DEBUG=self.__debug)
        my1_results = my1.get_all_prediction()
        solution['firstLines'] = []
        for result in my1_results:
            if result['travelTime'] > 0:
                solution['firstLines'].append(result)
                targettime = result['pairArrTime'][-1] + transferWalkTime
                break
        
        # Second Line
        solution['secondLineTransferStop'] = int(second_startID)
        my2 = ann.Ann(int(second_startID),int(second_endID),targettime,rain,sun, DEBUG=self.__debug)
        my2_results = my2.get_all_prediction()
        solution['secondLines'] = []
        for result in my2_results:
            if result['travelTime'] > 0:
                solution['secondLines'].append(result)
                break

        solution['transferDistance'] = route[2]
        solutions.append(solution)

        if len(solutions) > 0:
            return [[route[0][0], first_startID, route[1], solutions, second_endID, route[0][5], route[3]]]
        return []

    def updateData(self, key, value):
        solution_json_file = '{}/routesData.json'.format(self.__data_path)
        if key not in self.__solutionRoutes:
            self.__solutionRoutes[key] = value
            try:
                print(key, self.__solutionRoutes[key])
                with open(solution_json_file, 'w') as fp:
                    json.dump(self.__solutionRoutes, fp)
            except Exception as e:
                if self.__debug:
                    print("Cannot update routeData file! {}".format(str(e)))
                return False
        return True
        

    def getFinalRoute(self):
        '''
            Return the possible solution routes, which will search routes based on
            following strategy:
            1. Walk from station A to somewhere (assume station B)
            2. Take a bus from station B and get off on somewhere (assume station C)
            3. Walk from station C to somewhere (assume station D)
            4. Take the second bus from station D and get off on somewhere (assume station E)
            5. Walk from station E to station F
        '''
        startID = self.__startid
        endID = self.__endid
        pairedStations = "{},{}".format(startID, endID)
        if pairedStations in self.__solutionRoutes:
            route = self.__solutionRoutes[pairedStations]
            startTime = time.time()
            solutions = self.dataSearchRoute(route)
            stopTime = time.time()
        else:
            # Enhanced algorithm
            startTime = time.time()
            solutions = self.getCloserRoute()
            stopTime = time.time()
        return solutions[0]

    def showRoute(self):
        '''
            Display the possible solution routes, which will search routes based on
            following strategy:
            1. Walk from station A to somewhere (assume station B)
            2. Take a bus from station B and get off on somewhere (assume station C)
            3. Walk from station C to somewhere (assume station D)
            4. Take the second bus from station D and get off on somewhere (assume station E)
            5. Walk from station E to station F
        '''
        startID = self.__startid
        endID = self.__endid
        #route = [[1913,1908,335,7591,1751,1728],0.038,0.229,0.029]
        pairedStations = "{},{}".format(startID, endID)
        if pairedStations in self.__solutionRoutes:
            route = self.__solutionRoutes[pairedStations]
            startTime = time.time()
            solutions = self.dataSearchRoute(route)
            stopTime = time.time()
        else:
            # Enhanced algorithm
            startTime = time.time()
            solutions = self.getCloserRoute()
            stopTime = time.time()

        for solution in solutions:
            print("====="*5)
            print("*** Walk {} KM from {} to {} to get Line A".format(solution[2], solution[0], solution[1]))
            print("Line A:")
            print("\t {}".format(solution[3][0]['firstLines']))
            print("*** Walk from station {} to {} distance: {} km".format(solution[3][0]['firstLineTransferStop'],
                                                                          solution[3][0]['secondLineTransferStop'],
                                                                          solution[3][0]['transferDistance']))
            print("Line B:")
            print("\t {}".format(solution[3][0]['secondLines']))
            print("*** Walk {} KM from {} to {} to arrive dest".format(solution[6], solution[4], solution[5]))
        print("Algorithm 2 Running Time: {} seconds".format(round(stopTime-startTime,3)))
        
def main():
    # failed: 2,6
    # passed: 0, 1,3,4,5,7,8,9,10,11,12,13,14
    test_id = 15
    testplate = [[342, 1913],
                 [768, 4056],
                 [877, 7612],
                 [2048, 4978],
                 [1913, 1728],
                 [1913, 187],
                 [877, 7612],
                 [768, 4550],
                 [768, 7266],
                 [768, 37],
                 [768, 3665],
                 [768, 7149],
                 [768, 2557],
                 [1642, 3198],
                 [4568, 1018],
                 [776,3898],
                 [342,1946]]

    # mode can be 'fast' or 'normal'
    mode = 'fast'
    # DEBUG can be True or False
    debug = False
    #debug = True
    # Maxinum number of solutions
    sn = 1

    '''
    for i in [0,1,3,4,5,7,8,9,10,11,12,13,14,15]:
        my = ChangeBus(testplate[i][0], testplate[i][1], 36000, 1, 0, DEBUG=debug, MODE=mode, SN=sn)
        my.showRoute()
    '''
    i = 16
    my = ChangeBus(testplate[i][0], testplate[i][1], 36000, 1, 0, DEBUG=debug, MODE=mode, SN=sn)
    my.showRoute()
    #my.getFinalRoute()
    
    #print(my.findOppositeLine())
    #print(my.getRoute())
    #print(my.getRoute2())
    #pairedStations = '1913,1628'
    #data = [[1913,1908,335,7591,1751,1728],0.038,0.229,0.029]
   
    #my.updateData(pairedStations, data)


if __name__ == '__main__':
    main()
