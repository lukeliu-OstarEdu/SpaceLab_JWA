import csv
import codecs
import urllib.request
import sys
import json
from datetime import datetime
from datetime import timedelta
import json
from time import sleep

#get time , latitude, longtitude and name of photo file 
def parse_time_location_photofile(line): 
    list_time_loc_pho = line.strip().split() # split time,location,photo to list
    time = list_time_loc_pho[0] # get time
    lat = list_time_loc_pho[1] #get latitude
    long = list_time_loc_pho[2] #get Longitude
    photoname = 'photo_' + list_time_loc_pho[3] +'.jpg' # get photo_count and format it as photo_xxx.jpg
    return time, lat, long, photoname

#the photo_data file that has location, date/time and photoname
filename = r'D:\F\Home\CodingTutorial\astropi\2022\jwl\photo_data3.txt' 



#URL that used to query weather
BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?'
DateParam ='&aggregateHours=24&startDateTime=2022-05-06T00:00:00&endDateTime=2022-05-06T00:00:00&unitGroup=uk'
DataContent = '&contentType=json'
Key = '&key=HUF7UQTQR83A872KKSWZFH8AZ'


# open file to store the weather and photo name, location

weather_location_file = open('weather_location.txt','a')

with open (filename) as f:
    for line in f:
        #get time, location and photoname from data file
        time1, latitude, longtitude,photoname = parse_time_location_photofile(line)
        print(time1, latitude, longtitude,photoname)
        
        #time2 is end time for weather querying, increase 10 minuntes from time1.
        time2 = datetime.strptime(time1, "%H:%M:%S")
        time2 = time2 + timedelta(minutes=10)
        time2 = time2.strftime('%H:%M:%S')

        #contruct the Time section
        Time ='&dayStartTime='+ time1  + '&dayEndTime=' + time2
        #contruct the location section
        Location = '&location=' + latitude + ',' + longtitude
        # Full URL that used to query weather data
        Full_URL =  BaseURL+ DateParam +  Time + Location + Key
        print(Full_URL)

        #query weather data
        try:
            response = urllib.request.urlopen(Full_URL)
    
        except urllib.error.HTTPError  as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code, ErrorInfo)
            sys.exit()
        except  urllib.error.URLError as e:
            ErrorInfo= e.read().decode() 
            print('Error code: ', e.code,ErrorInfo)
            sys.exit()
    

        #format the weather data
        CSVText = csv.reader(codecs.iterdecode(response, 'utf-8'))

        RowIndex = 0
        RowList = []

        for Row in CSVText:
            RowList.append(Row)
        print(RowList)

        if len(RowList) > 1:
            Weather = {}
            for i in range(len(RowList[0])):
    
                 Weather[RowList[0][i]] = RowList[1][i]
                
            print(Weather['Cloud Cover'])
            print(Weather['Conditions'])
            
            #parase the weather data, change it to dictionary data type
            str_Weather = json.dumps(Weather)
            weather_location_detail_file.write(photoname+','+ str_Weather + '\n')
            
            #save weather condition to file
            if Weather['Conditions'] !='':
                weather_location_file.write(photoname+',' +  latitude + ',' + longtitude + ',' + Weather['Conditions'] + '\n')
            sleep(2)
#     close file       
weather_location_detail_file.close()
weather_location_file.close()