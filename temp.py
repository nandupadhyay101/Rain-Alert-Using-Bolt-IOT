import config, requests, time # import config file so we can fetch credentials related to bolt and twilio.
from boltiot import Sms, Bolt  # importing Sms and Bolt from boltiot.
from apscheduler.schedulers.background import BlockingScheduler # Here we are using apscheduler to schedule the script so we dont have to run the script maually.

mybolt = Bolt(config.api_key, config.device_id) # init bolt.
response = mybolt.isOnline()
print (response)
sms = Sms(config.SID, config.AUTH_TOKEN, config.TO_NUMBER, config.FROM_NUMBER) # init twilio.

# Sample Format Of Base Url - lat=33.44&lon=-94.04&exclude=hourly,daily&appid={API key}  
 
lat = "Your Location"      
lat = str(lat)

long = "Your Location"     
long = str(long)

complete_url = config.weather_base_url + "lat=" + lat + "&lon=" + long + "&exclude=current,minutely,hourly,alerts" + "&appid=" + config.weather_api_key

def operate():
          
        response = requests.get(complete_url)
        # get method of requests module
        # return response object
        
        x = response.json()
        # json method of response object
        # convert json format data into python format data.
   
        daily = x["daily"]
        weather = daily[0]["weather"]
        main = weather[0]["main"] 
        """ 
            Here [0] is used to select weather of first day out of the cluster of 7 days data that the api provides. 
            "Main" is the field which we are intrested in because it provides different types of weather conditions.
            But in order to access main we have to travel in this "daily -> weather -> main" fashion which you can see in the openweathermap api documentation. 
        """
      
        if main == "Clouds" or main == "Drizzle" or main == "Snow" or main == "Rain":
                print("Take umbrella and raincoat with you.")
                response = mybolt.digitalWrite('0', 'HIGH')
                print("Making request to Twilio to send a SMS")
                res = sms.send_sms("Rainfall Expected. Take umbrella and raincoat with you.")
                print("Response from twilio is" + str(res))
                print("status of sms at twilio is :" + str(res.status))
                time.sleep(3)
                response = mybolt.digitalWrite('0', 'LOW')

        else:
                print(main)
                response = mybolt.digitalWrite('0', 'LOW')

scheduler = BlockingScheduler()   # BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.add_job(operate, 'cron', hour='11-12', minute='*/1') # Here we have pass the operate function which will schdeule everyday at desired time. 
scheduler.start()
