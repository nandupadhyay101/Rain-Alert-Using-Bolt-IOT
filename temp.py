import config, requests, time
from boltiot import Sms, Bolt  # bolt init
from apscheduler.schedulers.background import BlockingScheduler

mybolt = Bolt(config.api_key, config.device_id)
response = mybolt.isOnline()
print (response)
sms = Sms(config.SID, config.AUTH_TOKEN, config.TO_NUMBER, config.FROM_NUMBER)

# Sample Format Of Base Url - lat=33.44&lon=-94.04&exclude=hourly,daily&appid={API key}  
 
lat = "Your Location"      
lat = str(lat)

long = "Your Location"     
long = str(long)

complete_url = config.weather_base_url + "lat=" + lat + "&lon=" + long + "&exclude=current,minutely,hourly,alerts" + "&appid=" + config.weather_api_key

# get method of requests module
# return response object

def operate():
          
        response = requests.get(complete_url)
        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()

        daily = x["daily"]
        weather = daily[0]["weather"]
        main = weather[0]["main"]
        print(main)

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

scheduler = BlockingScheduler()   #BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.add_job(operate, 'cron', hour='11-12', minute='*/1')
scheduler.start()