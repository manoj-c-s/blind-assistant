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


option = Options()
# option.add_experimental_option("debuggerAddress","localhost:9222")
# driver=uc.Chrome(use_subprocess=True)
ser = Service("C:\\Users\\manoj\Desktop\\voice-assistant-main\\chromedriver.exe")
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

def recognize_speech():
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
    response = ""
    speak("Identifying speech..")
    try:
        response = recognizer.recognize_google(audio)
    except:
        response = "Error"
    return response
   
time.sleep(3)
speak("Hello master! I am now online..")
while True:
    speak("Speak now")
    voice = recognize_speech().lower()
    print(voice)
    if 'open google' in voice:
        speak('Opening google..')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://google.com')
    elif 'search google' in voice:
        while True:
            speak('I am listening..')
            query = recognize_speech()
            if query != 'Error':
                break
        element =  driver.find_element(By.NAME,'q')
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'open youtube' in voice:
        speak('Opening youtube..')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://youtube.com')
    elif 'open gmail' in voice:
        speak('Opening gmail..')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        # driver.get('https://gmail.com')
        driver.get('http://localhost:3000/')
        while True:
            speak('tell me email..')
            query2 = recognize_speech()
            if query2 != 'Error':
                break
        element =  driver.find_element(By.NAME,'email')
        element.clear()
        element.send_keys(query2)
        while True:
            speak('tell me subject..')
            query = recognize_speech()
            if query != 'Error':
                break
        element =  driver.find_element(By.NAME,'subject')
        element.clear()
        element.send_keys(query)
        while True:
            speak('tell me message..')
            query3 = recognize_speech()
            if query3 != 'Error':
                break
        element =  driver.find_element(By.NAME,'message')
        element.clear()
        element.send_keys(query3)
        submit = driver.find_element(By.NAME,"submit");
        submit.click();
        # wait=WebDriverWait(driver,20)
        # url="https://accounts.google.com/ServiceLogin"
        # driver.get(url)
        # wait.until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}')
        # wait.until(EC.visibility_of_element_located((By.NAME, 'password'))).send_keys(f'{password}\n')
        # print("your in ")
        # time.sleep(99)
        # driver.implicitly_wait(4)
        # driver.find_element_by_name(("//*[@id='Passwd']")).sendKeys("ur password");
        # driver.find_element_by_name(("//*[@id='signIn']")).click();
    elif 'search youtube' in voice:
        while True:
            speak('I am listening..')
            query = recognize_speech()
            if query != 'Error':
                break
        element = driver.find_element(By.NAME,'search_query')
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'tab' in voice:
        num_tabs = len(driver.window_handles)
        cur_tab = 0
        for i in range(num_tabs):
            if driver.window_handles[i] == driver.current_window_handle:
                if i != num_tabs - 1:
                    cur_tab = i + 1
                    break
        driver.switch_to.window(driver.window_handles[cur_tab])
    elif 'close' in voice:
        speak('Closing Tab..')
        driver.close()
    elif 'go back' in voice:
        driver.back()
    elif 'go forward' in voice:
        driver.forward()
    elif 'exit' in voice:
        speak('Goodbye Master!')
        driver.quit()
        break
    else:
        speak('Not a valid command. Please try again.')
    time.sleep(1)
