# Thermal-Printer-Buttons

After posting a video of my project on TikTok, I got a lot of requests to do a form of HowTo or Project Guide. I believe a project like this can be a great way to begin learning programming and while I will walk through some of my steps, I encourage you to learn more about Python Programming and Raspberry Pi programming on your own.

A couple resources I really recommend are:
* https://automatetheboringstuff.com/
* https://magpi.raspberrypi.org/books/handbook-2021

## Functionality

The project does a couple things. Every morning it prints out a short Daily Digest with information.

Additionally there are 6 buttons attached to the Pi that each have their own functionality.

## The Hardware

My project consists of the following hardware pieces:
* Terow POS5890K Thermal Receipt Printer
* Raspberry Pi
  * No need for a high memory model. Mine is the original 256MB Pi B
* Buttons
  * I used arcade style buttons found online
* Raspberry Pi GPIO Breakout and breadboard
  * Not required per se, but will make your life easier
  * https://www.adafruit.com/product/2028
* Various lengths of wire

## Connecting the hardware

The thermal printer will plug into the USB port of the Raspberry Pi without issue.

The buttons are all wired to GPIO Pins through the breadboard and breakout. They complete the circuit from the pin to ground.

If you are new to adding buttons to the Raspberry Pi through GPIO, I recommend the following guide:
* https://projects.raspberrypi.org/en/projects/physical-computing/5

## The Software

The software I specifically used in my project is in this repo. I'll admit, it's not the best written code, but I never intended putting it out there, so here we are. :-)

The project is written using Python 3 and requires the following packages:
* python-escpos
  * https://github.com/python-escpos/python-escpos
  * For connecting and writing to thermal printer.
  * v3 required
* gpiozero
  * https://gpiozero.readthedocs.io/en/stable/
  * For interfacing with buttons
* requests
  * https://docs.python-requests.org/en/master/
  * For web API calls
* cairosvg
  * https://pypi.org/project/CairoSVG/
  * For converting SVG file from Pixel Monster to png
* Python-PlexAPI
  * https://python-plexapi.readthedocs.io/en/latest/
  * For connecting with Plex Server

## Software Setup

Note: This is for my current configuration setup. Your needs will most likely vary.

### Code Configuration

At the beginning of the funprint.py file there are a few constants that you will need to fill out.

* PROJECT_NAME: A unique project name. Used in User-Agent headers for API calls.
* EMAIL: Your contact email for API calls.
* WEATHER_STATION, WEATHER_X, & WEATHER_Y: Information used for the weather.gov API call.
  * Further info can be found on their api documentation site:
  * https://www.weather.gov/documentation/services-web-api
* PLEX_EMAIL & PLEX_PASSWORD: Your Plex login credentials. Used for getting random movie.

### Buttons Service Setup

Included in a buttons.service file. This is the service file that I use to run the buttons.py application. This small program is what monitors for button presses and takes the appropriate action.

Instructions on Linux Services using systemctl can be found below:
* https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units

## That's it

This is how I have my system setup and configured. Now I encourage you to hack the mess out of it and make it your own. Please review some of the resources I've linked and don't give up. It can be hard at first, but things will start falling into place. I wish you the best.
