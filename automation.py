""" 
Google authentication not possible for third party apps
https://support.google.com/accounts/answer/6010255?sjid=7775547259714085257-AP#zippy=%2Cif-less-secure-app-access-is-off-for-your-account
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import speech_recognition as sr
import time
import pyttsx3
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from playsound import playsound
from gtts import gTTS
from email.header import decode_header
import re


from CONSTANTS import EMAIL_ID, PASSWORD, LANGUAGE

option = Options()
# option.add_experimental_option("debuggerAddress","localhost:9222")
# driver=uc.Chrome(use_subprocess=True)
ser = Service("C:\\Users\\manoj\\Desktop\\blind-assistant\\chromedriver.exe")
# op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=option)

driver.maximize_window()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def speak(query):
    engine.say(query)
    engine.runAndWait()

def speech_to_text():
    """
    Speech to text

    Returns:
        str: Returns transcripted text
    """
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            print("You said: "+MyText)
            return MyText

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None

    except sr.UnknownValueError:
        print("unknown error occured")
        return None

def gmail():
    speak("Opening gmail...")
    driver.execute_script("window.open('');")
    window_list = driver.window_handles
    driver.switch_to.window(window_list[-1])
    # driver.get('https://gmail.com')
    driver.get('http://localhost:3000')
    speak("Please wait while Gmail loads")
    element =  driver.find_element(By.ID,'email')
    element.clear()
    element.send_keys(EMAIL_ID)
    element =  driver.find_element(By.ID,'password')
    element.clear()
    element.send_keys(PASSWORD)
    submit = driver.find_element(By.ID,"login")
    submit.click()
    time.sleep(6)
    while True:
        speak("Choose and speak out the option number for the task you want to perform. Say 1 to compose new mail. Say 2 to read inbox mails. Say 3 to read sent mails. Say exit to quit mail")
        speak("Speak now")
        choice = speech_to_text()

        if choice:

            if choice == '1' or choice.lower() == 'one':
                speak("Your choice is 1. To compose mail")
                composeMail()
            
            elif choice == '2' or choice.lower() == 'too' or choice.lower() == 'two' or choice.lower() == 'to' or  choice.lower() == 'tu' or choice.lower() == 'inbox':
                speak("Your choice is 2. To read inbox mails")
                readInbox()
                
            elif choice == '3' or choice.lower() == 'tree' or choice.lower() == 'three'or choice.lower()=='free':
                speak("Your choice is 3. To read sent mails")
                readSentMail()

            elif choice == 'exit':
                return None
            
            else: speak("Wrong choice. Please say only the number")

def composeMail():
    element = driver.find_element(By.CLASS_NAME, 'sidebar__compose')
    element.click()

    element = driver.find_element(By.CLASS_NAME, 'composeRecipients')
    element.clear()
    speak("Mention the gmail ID of the persons to whom you want to send a mail.")
    speak("speak")
    receivers = speech_to_text()
    em=''
    if receivers:  
      for email in receivers:
         em =em+email.replace(" ", "")
      em=em+"@gmail.com"
      speak("The mail will be send to " +(em.lower()) )
      element.send_keys(em.lower())
    else :
        speak("email not valid , please try from 1st step")


    element = driver.find_element(By.CLASS_NAME, 'composeSubject')
    element.clear()
    speak("Tell me the subject...")
    speak("Speak")
    sub = speech_to_text()
    speak("You said  " + sub)
    element.send_keys(sub)
    element = driver.find_element(By.CLASS_NAME, 'composeMsg')
    element.clear()
    speak("Say your message")
    speak("Speak")
    msg = speech_to_text()
    speak("You said  " + msg)
    element.send_keys(msg)
    submit = driver.find_element(By.CLASS_NAME,"compose__btn");
    submit.click()
    speak("Message sent")
    return 0

def readSentMail():
     element = driver.find_element(By.ID, 'sent')
     element.click()
     speak("sent message page is displaying ")
     element = driver.find_element(By.ID, "2")
     while element:
        #  speak("select number of senders name to read out")
        #  num= 5
        #  for i in range(int(num)): 
        #     element = driver.find_element(By.ID, 'subject')
        #     speak(element.text)
        #     i=i+1
        #  element = driver.find_element(By.ID, 'subject')
         ele=element.text.split('- ')
         speak("reciever email is "+ele[1]+"@gmail.com")
         speak("subject is "+ele[2])
         speak("message is "+ele[3])
         speak("Date and time when it sent is "+ele[4])
         return 0

def readInbox():
     element = driver.find_element(By.ID, 'inbox')
     element.click()    
     speak("inbox page is displaying ")
     speak("Which day mail do you want to read Out")
     num= "2"
     element = driver.find_element(By.ID, num)
     while element:
        #  speak("select number of senders name to read out")
        #  num= 5
        #  for i in range(int(num)): 
        #     element = driver.find_element(By.ID, 'subject')
        #     speak(element.text)
        #     i=i+1
        #  element = driver.find_element(By.ID, 'subject')
         ele=element.text.split('- ')
         speak("sender email is "+ele[0]+"@gmail.com")
         speak("subject is "+ele[2])
         speak("message is "+ele[3])
         speak("Date and time when it recieved is "+ele[4])
         return 0


time.sleep(3)
speak("Hello master! I am now online..")
if EMAIL_ID == "" and PASSWORD == "":
    speak("Email ID and password of your account should be feeded into the constants file, until then system cannot be accessed.")
    speak("Shutting down...")
else:
    while True:
        speak("What do you want to do?")
        speak("Speak")
        app = speech_to_text()
        if app:    
            app = app.lower()
            
            if "open gmail" in app:
                gmail()
                
            elif "close" in app: 
                speak("Closing tab...")
                driver.close()

            elif "go back" in app:
                driver.back()

            elif "go forward" in app:
                driver.forward()

            elif "exit" in app:
                speak("Goodbye Master!")
                driver.quit()
                break
            else:
                speak("Not a valid command. Please try again")
        
        time.sleep(1)
    

    
    
        
