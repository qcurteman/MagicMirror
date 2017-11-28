# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

# I (Quentin) went through and made some minor adjustments through this program.
# I created a class and a few functions to do make the program do what I wanted it to do as well.

from Tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
import os

from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
news_country_code = 'us'
weather_api_token = '5115c104f8f54f4fdb973e6a570af23c' # create account at https://darksky.net/dev/
weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'us' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
#latitude = '38.752125' # Set this if IP location lookup does not work for you (must be a string)
#longitude = '-121.288010' # Set this if IP location lookup does not work for you (must be a string)
latitude = None
longitude = None
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18


@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}


class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()
        

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            todays_date = self.date1
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black", justify=LEFT)
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text) 
            return ip_json['ip'] 
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)
                if location_obj['ip'] == '104.220.244.75':
                    lat = '38.752125'
                    lon = '-121.288010'
                    location2 = "%s, %s" % ('Rocklin', location_obj['region_code'])
                else:
                    lat = location_obj['latitude'] 
                    lon = location_obj['longitude']
                    location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                forecastTemp = self.checkForecastLength(forecast2)
                self.forecast = forecastTemp
                self.forecastLbl.config(text=forecastTemp)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    if location2 == "Olivehurst, CA":
                        location2 = "Yuba City, CA"
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()
            print "Error: %s. Cannot get weather." % e
    
        self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32
    
    # I (Quentin) wrote this function
    def checkForecastLength(self, forecast2, finalWord = None):
        if finalWord == None:
            finalWord = ""
        if forecast2 != '' and forecast2[0] == ' ':
                templist = list(forecast2)
                del templist[0]
                forecast2 = ''.join(templist)
        if len(forecast2) <= 25:
            for letter in forecast2:
                finalWord += str(letter)
            return finalWord
        else:
            count = 25
            temp = list(forecast2)
            while count < len(temp) and temp[count] != ' ':
                count+=1
                if count == ( 1 + len(forecast2)):
                    for letter in forecast2:
                        finalWord += str(letter)
                    return finalWord
                
            for index in range(count):
                finalWord += str(forecast2[index])
                
            del temp[0:count]
            finalWord += str("\n")
            forecast2 = ''.join(temp)
            return self.checkForecastLength(forecast2, finalWord)

#I (Quentin) created this class
class Welcome(Frame):
    def __init__(self, parent, eventName=""):
        Christmas = "Dec 25"
        ValentinesDay = "Feb 14"
        PIDay = "Mar 14"
        Today = time.strftime("%b %d")
        self.comment_bank = ["Are you made of Copper and Tellurium?\nBecause you're CuTe!",
                             "Have a great day!", "You are smart and successful!",
                             "You are amazing. Remember that.",
                             "It's bananas how good you look!", ]
        self.index = 0
        Frame.__init__(self, parent, bg='black')
        
        if Today == ValentinesDay:
            self.setEventName("Happy Valentines Day!")
        elif Today == Christmas:
            self.setEventName("Merry Christmas!\nSpend the day with the people you love:)")
        elif Today == PIDay:
            self.setEventName("It's PI day! 3.14159265359") 
        else:
            self.setEventName(self.comment_bank[0])
            self.getWelcome()
        
    def setEventName(self, event):
        self.eventName = event
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=BOTTOM, anchor=E)
        
    def getWelcome(self):
        if self.index > (len(self.comment_bank) - 1):
            self.index = 0
        self.eventName = self.comment_bank[self.index]
        self.index = self.index + 1
        self.eventNameLbl.config(text=self.eventName)
        self.eventNameLbl.after(3600000, self.getWelcome)

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.bottomFrame.pack(side=BOTTOM)
        
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # welcome
        self.welcome = Welcome(self.bottomFrame)
        self.welcome.pack( side=BOTTOM, anchor=S, padx=100, pady=200)
        

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
