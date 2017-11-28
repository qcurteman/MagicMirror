# MagicMirror

Magic Mirror Personal Project (Personal Project) Fall 2017

## Description:
- I decided to create this project as a gift for a friend. It is made in Python.
- There is a computer monitor plugged into a Raspberry Pi behind a picture frame. A semi-transparent acrylic screen is placed in front of the monitor as well.
- The Raspberry Pi is programmed to display information like a HUD. Anywhere there is light displaying on the monitor, it shows through the acrylic screen, but anywhere the monitor is black, the acrylic acts as a mirror. 
- The HUD displays:
  - Temperature
  - Weather outside
  - Forecast for the day
  - City and state you are in
  - Time, date, and day of week
  - A compliment that changes every hour

## Process: 
- I purchased a Raspberry Pi and downloaded a Git repository from a couple guys that I found on Youtube.
- I DID NOT write this entire program myself, instead, I found someone that had created a good frame of a program from which I could personalize.
- I created a wooden frame that matched the monitor size and designed it to fit in safely.

## Difficulties Faced: 
- The program displayed the forecast as a string, but the string was sometimes too long to fit in the frame it was housed in and so the words would be cut off.
  - Solution: I created a recursive function that breaks up a string by 25 characters and separates it at a space. It adds a ‘\n’ character to the string, thus shortening the string as a whole to fit within the frame
- I also had issues with it finding my location based on IP address. From my networking class, I learned that private networks, like my school network, uses private IP address. These IP’s don’t actually go out onto the web, instead, when the request gets to a router, it undergoes Network Address Translation (NAT) and a public IP is used to get out onto the internet.
  - Solution: I found the spot in the code that finds the IP address, and I used an if-statement to check if it was the public IP that the school uses. If it was, I changed my location to be my actual location. I didn’t want to have to do this because it doesn’t feel like a permanent solution but it worked for the time being. 

## New Skills Acquired:
- I learned how the Tkinter toolkit in Python works.
- I learned more about Python such as how dictionaries work and list comprehensions.
- I also learned how to work with other people’s code.
- I learned more about event driven programs, as this program is one that is constantly running and changing as time goes on. 
- How to make code display through a GUI that is appealing to the eye. 

Link to original code source: https://github.com/HackerHouseYT/Smart-Mirror

## Pictures!
![final](https://user-images.githubusercontent.com/28938321/33309238-3dee9e96-d3d2-11e7-8eaa-b293548d036b.JPG)
![backside](https://user-images.githubusercontent.com/28938321/33309018-93a15870-d3d1-11e7-962f-359b0cbf152c.JPG)
![stain](https://user-images.githubusercontent.com/28938321/33309002-7f1e575e-d3d1-11e7-8b31-d8d5704d9733.JPG)
![woodglue](https://user-images.githubusercontent.com/28938321/33309274-663a38e2-d3d2-11e7-85fc-ad2b400127c8.JPG)
