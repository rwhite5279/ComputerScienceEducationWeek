#!/usr/bin/env python3
"""
weather_wardrobe.py
This short script requests the text from a webpage that reports the 
weather, then extracts ("scrapes") the information that we're 
interested in from that page and prints it out.
Web scrapers can be finicky to manage--they rely on the webpage 
having a consistent format that they can look at--and there are 
better tools for analyzing text on a page, including Python's 
`re` tool (for looking at regular expressions) and the Beautiful 
Soup package.
This simple script just uses the string method .index() to find 
what we're looking for on a relatively simple page, as a proof 
of concept.

This program also uses Python to send email to someone from a Gmail
account.

This script requires that you log in to your Google account and
enable unsafe operations (like letting a script have access to your
email account). From Google account: 

    My Account > Sign-in & security > Allow less secure apps: ON

Note also that this script requires that the username for your 
Gmail account be placed in a text file called `gmail_username.txt`,
and the password for that Gmail account be placed in a file called 
`gmail_password.txt`, with both of these files located in the
same directory as this file. This is marginally safer than placing 
that information in the script itself, but plaintext passwords are 
still unsafe. There are ways to manage password security for a script, 
but they aren't addressed in this basic script.

For safety, do not use an important Gmail account for this script.
An out-of-control script might cause you to run afoul of Google's
Gmail policies.

"""

__author__ = "Richard White"
__version__ = "2021-03-16"

import smtplib          # Used for sending mail
from email.message import EmailMessage
import urllib.request   # Used to read webpage html
  
def get_credentials():
    gmail_user = ""                     # Enter your Google email here
    gmail_password = ""                 # Include password here (UNSAFE!)
    return gmail_user, gmail_password   

def mail(gmail_user, gmail_password, to, subject, text):
    """gmail_user = the sender
       gmail_password = password for senders Gmail account
       to = the recipient's email
       subject = subject is the subject line of the email
       text = the message that will be delivered in email body
    """
    # Set up Python EmailMessage object as msg
    msg = EmailMessage()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(text)
    # Establish server object for connecting to email server at the
    # indicated port. This object has methods we can use to send emails.
    # Sweigart, in "Automate the Boring Stuff with Python" says that
    # a server may not support TLS on 587. In that case, use 
    # smtplib.SMTP_SSL() and port 465 instead.
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    # Establish a connection with Google's smtp server
    mailServer.ehlo()
    # Use tls encryption
    mailServer.starttls()
    # Log in to the server using credentials
    mailServer.login(gmail_user, gmail_password)
    # Send the email that we composed
    mailServer.send_message(msg)
    # Disconnect from the server
    mailServer.quit()
    
def get_temperature():
    """Get the current temperature based on NOAA data
    
    This function uses information from NOAA's website to read the file 
    for BUR airport's weather, and then parses that data to find the current 
    temperature.
    
    Programs that attempt to parse HTML data are notoriously hacky: they rely on a 
    more-or-less consistent format in that page. If the HTML formatting changes, this 
    script has to be rewritten.
    """
    
    # identify the webpage we'll be reading from
    local_filename, headers = urllib.request.urlretrieve("https://forecast.weather.gov/MapClick.php?lat=34.1475&lon=-118.1443")
    html = open(local_filename)
    
    # read in the entire contents of that page
    # (We could read this in line by line, but we're going to end up parsing
    #  through the whole thing anyway, so this is okay.)
    completeFileContent = "".join(html.readlines())
    
    # Look for the lines that hav the current conditions listed
    # Find these by looking at 
    # at the webpage's html code. You can do that either by using a browser
    # to "View Source" for a page, or by looking through the value of 
    # completeFileContent after this program reads it in.
    
    start = completeFileContent.find('<!-- Graphic and temperatures -->')
    stop = completeFileContent.find('<div id="current_conditions_station">')
    
    text = completeFileContent[start: stop]
    tempstart = text.index('<p class="myforecast-current-lrg">') + 34
    tempstop = text.index('&deg;F')
    temp = text[tempstart : tempstop]
    temp = float(temp)
    return temp

def create_weather_message(temp):
    msg = "The temperature in Pasadena is currently " +  str(temp) + " degrees Fahrenheit.\n"
    if temp < 50:
        msg += "It's going to be chilly this morning!"
    elif temp < 60:
        msg += "Better put on a sweater this morning!"
    elif temp < 70:
        msg += "It's a little cool out but it'll warm up soon."
    elif temp < 80:
        msg += "It's going to be a lovely day."
    else:
        msg += "It's already warm out. Make sure you stay hydrated."
    print(msg)
    return msg

def main():
    gmail_user, gmail_password = get_credentials()
    temp = get_temperature()
    msg = create_weather_message(temp)
    # This function call initiates the function defined above, 
    # with the parameters being the sender, intended recipient, the 
    # subject line, and the body of the message.
    recipient = ""                              # replace with actual email/phone number
    subject = "Wardrobe update"
    body = msg
    mail(gmail_user, gmail_password, recipient, subject, body)


if __name__ == "__main__":
    main()  
