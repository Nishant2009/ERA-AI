import os, datetime, time, sys, psutil, subprocess, pyautogui, platform, operator, webbrowser, random
# pip install SpeechRecognition pyttsx3 requests bs4 speedtest-cli PyPDF2 pywhatkit pywikihow instadownloader psutil translate PyQt5
import speech_recognition, pyttsx3, requests, speedtest, PyPDF2, pywhatkit, pywikihow, instaloader, wikipedia
from translate import Translator
from bs4 import BeautifulSoup
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from screen import Ui_Dialog



# Selecting voice for It
"""It get voice by this command for more voices change voice[0].id to voice[1].id or more """
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices",voices[0].id)

# Translator
def hindi_to_english(hindi_text):
    translator = Translator()
    translated = translator.translate(hindi_text, src='hi', dest='en')
    return translated.text



# For relative path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Speak command
def speak(audio):
    """Speaking the command by the help of pyttsx3 module and the above selected voice"""
    engine.say(audio)
    print(audio)
    typetext(audio)
    engine.runAndWait()

# Listening user input in INDIAN-English
say_it = ["Say that again please","","Sir, I didn't understand, may you speak again","", "ERA"]

# Listening user input
def takecommand(lang="en-in"):
    """It listens our command in INDIAN-English language , allow a phrase to continue before 5 seconds and returning the part of the phrase processed before 5 seconds and return the command in string format."""
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("listening ...")
        typetext("listening ...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, phrase_time_limit=5)

    # Converting speech to string
    try:
        print("Recognising ...")
        typetext("Recognising ...")
        if lang != "en-in":
            translator = Translator(to_lang="en", from_lang='hi')
            MainThread.query = recognizer.recognize_google(audio, language="hi")
            print(f"user said (in Hindi): {MainThread.query}")
            MainThread.query = translator.translate(MainThread.query)
            print(f"Translated to English: {MainThread.query}")
            typetext(f"Translated to English: {MainThread.query}")
        else:
            MainThread.query = recognizer.recognize_google(audio, language=lang)
            print(f"user said: {MainThread.query}")
            typetext(f"user said: {MainThread.query}")
    except Exception as e:
        speak(say_it[0])
        if say_it[0] == "":
            print("Say that again please")
        return "none"
    return MainThread.query



# tasks AI can do
"""AI can perfon those following tasks when you say ai to do them"""
specifications =["I can tell temperature, Battery percentage", "i can open notepad, calculator, control panel, magnifier, on screen keyboard, steps recorder, task manager, about windows, microsoft edge, and google chrome","I can close notepad, calculator, control panel, about windows, microsoft edge, and google chrome", "I can shutdown the system, restart the system, and sleep the system","I can volume up, volume down, also do mute and unmute", "I can check internet speed", "I can tell about system information", "I can take screenshots", "I can do calculations", "I can read books aloud for you", "I can hide and unhide the folder from where you start me", "I can open youtube, facebook, instagram, github, stackoverflow, amazon, flipkart, twitter, Shri Vishwakarma Skill University Site, Linkedin, google collab, and gmail", "I can search anything on google, play any song and video on youtube", "I can send whatsapp messages", "I can tell your IP Address", "I can Serach for something on wikipedia", "I can tell our current location", "I can give some advice useful in day to day life", "I can tell joke", "I can tell how to do anything, when how to do mode is activated", "I can fetch and tell news from internet", "I can view instagram profile of anyone and can also download his or her profile picture.", "That is all what I can do"]


# calculator function
def get_operator_fn(op):
                return {
                '+' : operator.add, #plus
                "plus" :  operator.add, #plus
                '-' : operator.sub, #minus
                "minus" : operator.sub, #minus
                'x' : operator.mul, #multiplied by
                'X' : operator.mul, #multiplied by
                'multiply' : operator.mul, #multiplied by
                'divided' :operator.__truediv__, #divided
                }[op]
def eval_binary_expr(op1, oper, op2): # 5 plus 8
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(oper)(op1, op2)


def hide_file():
    speak("sir please tell me you want to hide this folder or make it visible for everyone")
    condition = takecommand().lower()
    if "hide" in condition :
        os.system("attrib +h /s /d")
        speak("Sir, all the files in this folder are now hidden.")
    elif "visible" in condition :
        os.system("attrib -h /s /d")
        speak("Sir, all the files in this folder are now visible to everyone . i wish you are taking this decision in your own peace.")
    elif "leave it" in condition or "leave for now" in condition :
        speak("Ok sir")


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    speak(res['slip']['advice'])

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    speak(res['joke'])

def how_to_mode() :
    how = takecommand()
    max_resu1ts = 1
    how_to = pywikihow.search_wikihow(how, max_resu1ts)
    assert len(how_to) == 1
    speak(how_to[0].summary)

def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey=5a48fb92a6aa49ad88d0b927ddce3129&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    newses = news_headlines[:5]
    for news in newses :
        speak(news)

def where_am_i():
    try :
        ip = requests.get("https://api.ipify.org").text
        print(ip)
        typetext(ip)
        url = "https://get.geojs.io/v1/ip/geo/"+ip+'.json'
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        city = geo_data['city']
        country = geo_data['country']
        if 'region' in geo_data :
            state = geo_data['region']
            speak(f"Sir I am not sure, but I think WE are in {city} city of {state} state of {country} country")
        else :
            speak(f"Sir I am not sure, but I think WE are in {city} city of {country} country")
    except Exception as e:
        speak("sorry sir, Due to network issue i am not able to find where we are")
        pass

def insta_profile():
    btn_clk()
    time.sleep(2)
    username = get_str()
    read_mod()
    webbrowser.open(f"www.instragram.com/{username}")
    speak(f"Sir here is the profile of user {username}")
    time.sleep(4)
    speak("Sir would you like to download profile picture of this account.")
    command = takecommand().lower()
    if "yes" in command :
        instaloader.Instaloader().download_profile(username, profile_pic_only=True)
        speak("I am done Sir profile picture saved in our main folder. Now I am ready for next command")
    else:
        pass
        






class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
    
    def run(self):
        self.wishme()
        self.Task_Execution()




    # Wishme function of te starting
    def wishme(self):
        """ This function executes in the starting ,our AI wish us ,tell the current time and ask for command"""
        hour = int(datetime.datetime.now().hour)
        say_time = time.strftime("%I:%M %p")
        if hour >=4 and hour < 12:
            speak(f"Good Morning Sir it's {say_time}")
        elif hour >=12 and hour < 18:
            speak(f"Good Afternoon Sir it's {say_time}")
        else :
            speak(f"Good Evening Sir it's {say_time}")
        speak(f"Sir, I am ERA, Please tell me how may i help you")


    def Task_Execution(self,lang = "en-in"):
        """in this function there is code for all the tasks our AI can perform """
        commands = {
            'hello': [
                'Hello! How can I assist you today?',
                'Hi there! What can I do for you?',
                'Good morning! How can I help?',
                'Hey! What can I assist you with?',
                'Greetings! How may I assist you today?',
                'Hiya! What can I help you with?',
                'Hello there! How can I assist you today?'
                "hello sir, may i help you with something."
            ],
            "how are you": [
                "I'm doing well, thank you for asking. How can I assist you?",
                "I'm feeling great today, thanks for asking. How can I help you?",
                "I'm doing fine, thanks for asking. How can I assist you?",
                "I'm feeling good today, thanks for asking. How can I help you?",
                "I'm doing well, thanks for asking. How can I assist you?",
                "I'm feeling great today, thanks for asking. How can I help you?",
                "I'm doing fine, thanks for asking. How can I assist you?"  ],
            "what's up?": [
                "Nothing much, how about you?" ,
                "Just helping people out here. What can I help you with?" , 
                "Not much, just waiting to help you. What can I do for you?" , 
                "Nothing much, just here to help. What do you need?" , 
                "Nothing much, just waiting to help you out. What can I do for you?" , 
                "Nothing much, just waiting for your self.query. What can I help you with?" , 
                "Nothing much, just here to assist you. What do you need help with?"
                ],
            "good morning": [
                "Good morning to you too! How can I help you today?" , 
                "Good morning! What brings you here today?" , 
                "Good morning! What do you need help with today?" , 
                "Good morning! How can I assist you today?" , 
                "Good morning! What can I do for you today?" , 
                "Good morning! What brings you to me today?" , 
                "Good morning! How may I assist you today?"],
            "good night": [
                "Good night, sleep tight! See you soon." , 
                "Good night! Sweet dreams." , 
                "Good night! Have a peaceful sleep." , 
                "Good night! Sleep well." , 
                "Good night! See you tomorrow." , 
                "Good night! Rest well." , 
                "Good night! See you soon."
                ],
            "thanks": [
                "You're welcome! Happy to help." , 
                "My pleasure! Let me know if you need anything else." , 
                "Glad I could assist you! Do come back if you need help." , 
                "No problem! Let me know if you need further help." , 
                "Anytime! Just let me know if you need more help." , 
                "No worries! Do come back if you need further assistance." , 
                "Not a problem! I'm always here to help."
                ],
            "search": [
                "What would you like me to search for?", 
                "What keyword or phrase should I search for?", 
                "I can search for anything you want, just tell me what you're looking for"]
            
        }
        while True:
            self.query = takecommand(lang).lower()

            if "hello" in self.query or "hey" in self.query or "are you there" in self.query :
                response = random.choice(commands["hello"])
                speak(response)

            elif "how are you" in self.query :    
                response = random.choice(commands["how are you"])
                speak(response)

            elif "good morning" in self.query :    
                response = random.choice(commands["good morning"])
                speak(response)
            
            elif "good night" in self.query :    
                response = random.choice(commands["good night"])
                speak(response)

            elif "thank" in self.query :    
                response = random.choice(commands["thanks"])
                speak(response)

            elif "also good" in self.query or "fine" in self.query :
                speak("that's great to hear from you.")

            elif "do" in self.query and "thing" in self.query :
                speak("yes sir tell what to do")
                self.Task_Execution()

            elif "who" in self.query and "are" in self.query and "you" in self.query :
                speak(f"Sir , I am your a i assistant ERA.")
                speak("I am here to make your life easier. You can command me to perform various tasks such as calculating sums or opening applications etcetra")

            elif ("hindi" in self.query and "listen" in self.query) or ("hindi" in self.query and "mod" in self.query):
                self.Task_Execution(lang = "hi")
                speak("Hindi listening mode on ")
                
            elif "what can you do" in self.query or "what are your features" in self.query or "what are your specifications" in self.query :
                speak(f"Sir, I can do the following tasks")
                for spec in specifications :
                    speak(spec)

            elif "silent" in self.query and "mod" in self.query:
                say_it[0], say_it[1], say_it[3], say_it[2]= say_it[1], say_it[0], say_it[2], say_it[3]

            elif "temperature" in self.query or 'weather' in self.query:
                search= self.query.split()[-1]
                url = f"https://www.google.com/search?q= temperature in {search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text,"html.parser")
                current_temperature = data.find("div",class_="BNeawe").text
                speak(f"current temperature in {search} is {current_temperature}")

            elif "battery" in self.query :
                battery = psutil.sensors_battery()
                percentage = battery.percent
                is_connected = battery.power_plugged
                con = "connected to charging" if is_connected else "not connected to charging"
                speak(f"sir our system have {percentage} percent battery, and system is {con}")
                if is_connected != True :
                    if percentage>=75:
                        speak("we have enough power to continue our work")
                    elif percentage>=40 and percentage<=75:
                        speak("we should connect our system to charging point to charge our battery")
                    elif percentage<=15 and percentage<=30:
                        speak("we don't have enough power to work, please connect to charging")
                    elif percentage<=15:
                        speak("we have very low power, please connect to charging the system will shutdown very soon")
                else:
                    pass

            elif "open" in self.query and "c drive" in self.query :
                os.startfile("C:")

            elif "open" in self.query and "notepad" in self.query :
                speak("Ok Sir, opening notepad")
                os.startfile("C:/Windows/System32/notepad.exe")

            elif "open" in self.query and "calculator" in self.query :
                speak("Ok Sir, opening calculator")
                os.startfile("C:/Windows/System32/calc.exe")

            elif "open" in self.query and "control panel" in self.query :
                speak("Ok Sir, opening control panel")
                os.startfile("C:/Windows/System32/control.exe")

            elif "open" in self.query and "magnifier" in self.query :
                speak("Ok Sir, opening magnifier")
                os.startfile("Magnify.exe")

            elif "open" in self.query and "on" in self.query and "screen" in self.query and "keyboard" in self.query :
                speak("Ok Sir, opening on screen keyboard")
                os.startfile("C:/Windows/System32/osk.exe")

            elif "open" in self.query and "step" in self.query and "recorder" in self.query :
                speak("Ok Sir, opening steps recorder")
                os.startfile("C:/Windows/System32/psr.exe")      

            elif "open" in self.query and "task manager" in self.query :
                speak("Ok Sir, opening task manager")
                os.startfile("C:/Windows/System32/Taskmgr.exe")     

            elif "open" in self.query and "about windows" in self.query :
                speak("Ok Sir, opening winver for about windows")
                os.startfile("C:/Windows/System32/winver.exe")  

            elif "open" in self.query and "edge" in self.query :
                speak("Ok Sir, opening microsoft edge")
                try :
                    os.startfile("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
                except Exception:
                    speak("Sir, I am unable to perform this function due to some error")

            elif "open" in self.query and "chrome" in self.query :
                speak("Ok Sir, opening google chrome")
                try :
                    os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
                except Exception:
                    speak("Sir, I am unable to perform this function due to some error")

            elif "close" in self.query and "notepad" in self.query :
                speak("Ok Sir , closing notepad")
                subprocess.call("taskkill /f /im notepad.exe" , shell = True)

            elif "close" in self.query and "calculator" in self.query :
                speak("Ok Sir , closing calculator")
                subprocess.call("taskkill /f /im CalculatorApp.exe" , shell = True)

            elif ("close" in self.query and "control panel" in self.query) or ("close" in self.query and "manager" in self.query) :
                speak("Ok Sir, closing control panel")
                os.system("wmic process where name='explorer.exe' delete")

            elif "close" in self.query and "about window" in self.query or "close" in self.query and "winver" in self.query :
                speak("Ok Sir , closing winver")
                subprocess.call("taskkill /f /im winver.exe" , shell = True)

            elif "close" in self.query and "edge" in self.query :
                speak("Ok Sir , closing Microsoft edge")
                try:
                    subprocess.call("taskkill /f /im msedge.exe" , shell = True)
                except Exception:
                    speak("Sir, I am unable to perform this function due to some error")

            elif "close" in self.query and "chrome" in self.query :
                speak("Ok Sir , closing Google chrome")
                try :
                    subprocess.call("taskkill /f /im chrome.exe" , shell = True)
                except Exception:
                    speak("Sir, I am unable to perform this function due to some error")

            elif 'close' in self.query and 'magnifier' in self.query:
                speak("Ok Sir, closing magnifier")
                os.system("wmic process where name='magnify.exe' delete")

            elif "shut down" in self.query and "system" in self.query or "shutdown" in self.query and "system" in self.query :
                speak("Ok Sir , system will shutdown will start in few seconds")
                os.system("shutdown /s /t 5")

            elif "restart system" in self.query and "restart the system" in self.query :
                speak("Ok Sir , system will restart will start in few seconds")
                os.system("shutdown /r /t 5")

            elif "sleep system" in self.query or "sleep the system" in self.query :
                speak("Ok Sir , system will sleep will start in few seconds")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif 'volume up' in self.query :
                pyautogui.press("volumeup")

            elif 'volume down' in self.query :
                pyautogui.press("volumedown")

            elif 'volume' in self.query and 'mute' in self.query :
                pyautogui.press("volumemute")

            elif "check" in self.query and "internet" in self.query and "speed" in self.query :
                speak("Sir I am checking the internet speed, It may take 1 or 2 minutes")
                st = speedtest.Speedtest()
                d1 = st.download()
                up = st.upload()
                spdn = int((int(d1)/8)/1024)
                spdup = int((int(up)/8)/1024)
                speak(f"sir we have {spdn} KB per second downloading speed, and {spdup} KB per second uploading speed")


            elif "system information" in self.query :
                uname = platform.uname()
                speak(f"System: {uname.system}")
                speak(f"Node Name: {uname.node}")
                speak(f"Release: {uname.release}")
                speak(f"Version: {uname.version}")
                speak(f"Machine: {uname.machine}")
                speak(f"Processor: {uname.processor}")

            elif "screenshot" in self.query :
                speak("Sir, Please tell me the name of this screenshot file")
                img_name  = takecommand().lower()
                speak("Sir, hold the screen for few seconds, I am taking Screenshot in 5 seconds")
                time.sleep(4)
                img = pyautogui.screenshot()
                img.save(f"{img_name}.png")
                os.rename(resource_path(f"{img_name}.png"), f'C:/Users/{os.listdir("c://users")[4]}/Pictures/{img_name}.png')
                speak("I am done sir ,screenshot is saved in our Pictures folder. Now I am ready for next command")

            elif "calculat" in self.query :
                speak("Say what you want to calculate, example: 3 plus 3")
                my_eqn = takecommand()
                speak("your result is " + str(eval_binary_expr(*(my_eqn.split()))))

            elif "read book" in self.query :
                speak("Sir, Please enter the pdf name")
                btn_clk()
                time.sleep(2)
                book_name = get_str()
                read_mod()
                try :
                    book = open(f"{book_name}.pdf", "rb")
                    pdfReader = PyPDF2.PdfFileReader(book)
                    pages = pdfReader.numPages
                    speak(f"Total numbers of Pages in this book {pages}")
                    speak("Sir please enter the page number I have to read")
                    pg = takecommand().lower()
                    page = pdfReader.getPage(pg)
                    text = page.extractText()
                    speak(text)
                except Exception:
                    speak("Sir, I am unable to perform this function due to some error")

            elif "hide all files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query :
                hide_file()

            elif "open youtube" in self.query :
                speak("OK Sir, Opening Youtube")
                webbrowser.open("www.youtube.com")

            elif "open facebook" in self.query :
                speak("OK Sir, Opening facebook")
                webbrowser.open("www.facebook.com")

            elif "open insta" in self.query and "profile" not in self.query:
                speak("OK Sir, Opening instagram")
                webbrowser.open("www.instagram.com")
            
            elif "open github" in self.query :
                speak("OK Sir, Opening github")
                webbrowser.open("github.com")

            elif "open stackoverflow" in self.query or "stack" in self.query and "over" in self.query and "flow" in self.query :
                speak("OK Sir, Opening Stackoverflow")
                webbrowser.open("https://stackoverflow.com/")

            elif "open amazon" in self.query :
                speak("OK Sir, Opening amazon")
                webbrowser.open("www.amazon.in")

            elif "open flipkart" in self.query :
                speak("OK Sir, Opening flipkart")
                webbrowser.open("www.flipkart.com")

            elif "open twitter" in self.query:
                speak("OK Sir, opening twitter")
                webbrowser.open("https://twitter.com/")

            elif "open" in self.query and "skill university" in self.query or "open" in self.query and "svsu" in self.query:
                speak("Ok Sir, Opening shri vishwakarma skill university site")
                webbrowser.open("https://svsu.ac.in")

            elif "open linkedin" in self.query :
                speak("OK Sir, Opening Linkedin")
                webbrowser.open("https://in.linkedin.com/")

            elif "open colab" in self.query :
                speak("OK Sir, Opening Google colab")
                webbrowser.open("https://colab.research.google.com/notebooks/intro.ipynb#recent=true")

            elif "open" in self.query and "gmail" in self.query :
                speak("OK Sir, Opening Gmail")
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

            elif "open google" in self.query :  
                response = random.choice(commands["search"])
                speak(response)
                srch = takecommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={srch}")

            elif "song" in self.query and "youtube" in self.query :
                speak("Sir, which song will I play ?")
                song_name = takecommand().lower()
                pywhatkit.playonyt(song_name)

            elif "video" in self.query and "youtube" in self.query :
                speak("Sir, which video will I play ?")
                video_name = takecommand().lower()
                pywhatkit.playonyt(video_name)

            elif "whatsapp" in self.query :
                speak("Sir, Please type the number to send message")
                btn_clk()
                time.sleep(2)
                number = get_str()
                print(number)
                read_mod()
                speak("Sir, Please tell the message to send")
                message = takecommand().lower()
                speak(f"Sir your message is, {message} for the number {number}")
                speak("Sir, is it correct, Will I send it, reply in yes or no?")
                msg = takecommand().lower()
                if "yes" in msg:
                    speak("OK Sir, your message will be sent in 15 seconds")
                    pywhatkit.sendwhatmsg_instantly(f"+91{number}", message,wait_time=7)
                    speak("I am done Sir, your message has been sent, Now I am ready for next command")
                else:
                    speak("ok sir, cancelling message")

            elif "ip address" in self.query:
                ip = requests.get("https://api.ipify.org").text
                speak(f"Your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("OK sir, searching on wikipedia ...")
                self.query = self.query.replace("wikipedia","")
                results = wikipedia.summary(self.query,sentences=5)
                speak("according to wikipedia")
                speak(results)

            elif "switch" in self.query and "window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "where we are" in self.query or "where am i" in self.query or "location" in self.query:
                speak("wait sir let me check")
                where_am_i()

            elif "give" in self.query and "advice" in self.query or "tell" in self.query and "advice" in self.query :
                get_random_advice()

            elif "tell" in self.query and "joke" in self.query :
                get_random_joke()

            elif "how to" in self.query and "mod" in self.query :
                speak("Sir, How to do mode is activated please tell me what you want to know?")
                how_to_mode()

            elif "news" in self.query :
                speak("OK Sir, I am fetching news from internet")
                get_latest_news()

            elif "instagram profile" in self.query or "profile on instagram" in self.query:
                speak("Sir please enter the username correctly")
                insta_profile()

            elif "no thanks" in self.query or "quit now" in self.query or "good bye" in self.query or "goodbye" in self.query or "you can sleep" in self.query or "sleep now" in self.query or "shutdown" in self.query or "shut down" in self.query:
                speak("okay sir, i am going to sleep.")
                exit_now()
                    
            else :
                if self.query != "none" and ("what" in self.query or "when" in self.query or "how" in self.query or "where" in self.query):
                    speak("I don't find it in my data may I search it on google")
                    ans = takecommand().lower()
                    if "yes" in ans or "ok" in ans:
                        speak("Sir, I am searching on google")
                        url = f"https://www.google.com/search?q= {self.query}"
                        r = requests.get(url)
                        data = BeautifulSoup(r.text,"html.parser")
                        result = data.find("div",class_="BNeawe").text.replace("( listen);","")
                        speak(f"{result}")
                    else:
                        speak("OK Sir, I am not searching it")
                else :
                    pass


start_Eecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("ERA")
        # self.setWindowIcon(QIcon(resource_path("logo.png")))
        self.ui.textBox.setReadOnly(True)
        self.ui.textBox.setText("HELLO ERA HERE")
        self.ui.btn_i.clicked.connect(self.input_value)
        self.ui.btn_j.clicked.connect(self.read_on)

    def startTask(self):
        start_Eecution.start()

    def input_value(self):
        self.ui.textBox.clear()
        self.ui.textBox.setReadOnly(False)
        self.ui.textBox.setFocus()

    def read_on(self):
        self.ui.textBox.clear()
        self.ui.textBox.setReadOnly(True)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    era = Main()
    scrn = Ui_Dialog()
    era.setFixedHeight(818)
    era.setFixedWidth(1158)
    era.startTask()

    def btn_clk():
        era.ui.btn_i.click()
        time.sleep(9)

    def get_str():
        number = era.ui.textBox.toPlainText()
        return number

    def read_mod():
        era.ui.btn_j.click()

    def typetext(abc):
        era.ui.textBox.append(abc)
        era.ui.textBox.moveCursor(QtGui.QTextCursor.End)

    def exit_now():
        era.close()

    era.show()
    sys.exit(app.exec())