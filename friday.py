from tkinter import *
import cv2
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import webbrowser as wb
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import urllib.request
import urllib.parse 
import requests,json

chrome_path="C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

engine=pyttsx3.init('sapi5') #Speech Application Programming Interface (SAPI) is an API developed by Microsoft to allow the use of speech recognition
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
#print(voices[1].id) #female voice(2 voices available, male and female)

window=Tk()

global var
global var1
var=StringVar()
var1=StringVar()

def speak(audio): #For speaking whatever is passed as an audio 
    engine.say(audio)
    engine.runAndWait()


def wish_user(): #Wishing user according to the time of the day on clicking the WISH ME button
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        var.set("Good Morning! I am FRIDAY! How may I help you?") 
        window.update()
        speak("Good Morning! I am FRIDAY! How may I help you?")
    elif hour>=12 and hour<18:
        var.set("Good Afternoon! I am FRIDAY! How may I help you?")
        window.update()
        speak("Good Afternoon! I am FRIDAY! How may I help you?")
    else:
        var.set("Good Evening! I am FRIDAY! How may I help you?")
        window.update()
        speak("Good Evening! I am FRIDAY! How may I help you?")


def takeCommand(): #Takes microphone input from user and returns a string output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()
        print("Listening...")
        r.pause_threshold=2   #seconds of non-speaking audio before a phase
        audio=r.listen(source)  #Records a single phrase from ``source`` into an ``AudioData`` instance, which it returns.
    try:
        var.set("Recognizing...")
        window.update()
        print("Recognizing")
        query=r.recognize_google(audio) #Uses google engine

    except Exception as e:
        return "None"
    var1.set(query)
    window.update()
    return query


def sendEmail(to, content): #For sending mails  
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('shefalisharma289@gmail.com', 'sheefu99') #enable less secure apps of account
    server.sendmail('shefalisharma289@gmail.com', to, content)
    server.close()
    

def play(): #Initiate speech recognition on clicking the PLAY button 
    btn1.configure(bg='orange')

    wish_user()

    while True:
        btn1.configure(bg='orange')
        query=takeCommand().lower()
        if 'exit' in query:
            var.set("Bye... Have a nice day!")
            btn1.configure(bg='#5C85FB')
            btn2['state']='normal'
            btn0['state']='normal'
            window.update()
            speak("Bye... Have a nice day!")
            break

        elif 'pause' in query:
            var.set("Pausing...")
            btn1.configure(bg='#5C85FB')
            btn2['state']='normal'
            btn0['state']='normal'
            window.update()
            speak("Pausing...")
            break

        #TASKS BASED ON QUERY

            #APPLICATIONS/SONGS/SENDING MAILS/GOOGLE/DATE & TIME

        elif 'wikipedia' in query:
            if 'open wikipedia' in query:
                var.set('Opening Wikipedia')
                window.update()
                speak('Opening Wikipedia')
                webbrowser.open('wikipedia.com')
            else:
                try:
                    speak("Searching Wikipedia")
                    query=query.replace("wikipedia", "")
                    result=wikipedia.summary(query, sentences=1)
                    speak("According to wikipedia")
                    var.set(result)
                    window.update()
                    speak(result)
                except Exception as e:
                    var.set('Sorry.. Could not find any results')
                    window.update()
                    speak('Sorry.. Could not find any results')

        elif 'open youtube' in query:
            var.set('Opening YouTube')
            window.update()
            speak('Opening YouTube')
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            var.set('Opening Google')
            window.update()
            speak('Opening Google')
            webbrowser.open("google.com")
			
        elif 'open facebook' in query:
            var.set('Opening Facebook')
            window.update()
            speak('Opening Facebook')
            webbrowser.open('facebook.com')

        elif ('songs' in query) or ('play music' in query) or ('next song' in query) or ('change music' in query):
            var.set('Playing your songs')
            window.update()
            speak('Playing your songs')
            music_dir='C:\\Users\\HP\\Desktop\\songs' 
            songs=os.listdir(music_dir)
            ch=random.randint(0, 62)
            os.startfile(os.path.join(music_dir, songs[ch]))

        elif 'click photo' in query:
            stream=cv2.VideoCapture(0)
            grabbed, frame=stream.read()
            if grabbed:
                cv2.imshow('pic', frame)
                cv2.imwrite('pic.jpg',frame)
            stream.release()

        elif 'record video' in query:
            cap = cv2.VideoCapture(0)
            out = cv2.VideoWriter('output.mp4', -1, 20.0, (640,480))
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret:
                    
                    out.write(frame)

                    cv2.imshow('frame',frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()

        elif 'the time' in query:
            time=datetime.datetime.now().strftime("%H:%M:%S")
            var.set("The time is %s" % time)
            window.update()
            speak("The time is %s" %time)

        elif 'the date' in query:
            date=datetime.datetime.today().strftime("%d %m %y")
            var.set("Today's date is %s" %date)
            window.update()
            speak("Today's date is %s" %date) 

        elif 'news' in query:
            try:
                news_url="https://news.google.com/news/rss"
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:5]:
                    var.set(news.title.text.encode('utf-8'))
                    window.update()
                    speak(news.title.text.encode('utf-8'))
            except Exception as e:
                    var.set('Sorry.. Could not find any results')
                    window.update()
                    speak('Sorry.. Could not find any results')

        elif "what is the weather in" in query:
            api_key="b4b313e7003170e60e98e837009b64ab"
            weather_url="http://api.openweathermap.org/data/2.5/weather?"
            data=query.split(" ")
            location=str(data[5])
            url=weather_url+"appid="+api_key+"&units=metric"+"&q="+location 
            js=requests.get(url).json() 
            if js["cod"] != "404": 
                weather=js["main"] 
                temp=weather["temp"] 
                hum=weather["humidity"] 
                desc=js["weather"][0]["description"]
                resp_string="It is "+str(temp)+" degree celsius."+" The humidity is " + str(hum)+"%"+" and the weather description is "+ str(desc)
                var.set(resp_string)
                window.update()
                speak(resp_string)
            else: 
                var.set("City Not Found") 
                window.update()
                speak("City Not Found")

        elif 'open vs code' in query:
            var.set("Opening VS Code")
            window.update()
            speak("Opening VS Code")
            path="C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\_\\Code.exe" 
            os.startfile(path)

        elif 'open media player' in query:
            var.set("Opening VLC Media Player")
            window.update()
            speak("Opening V L C Media Player")
            path="C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe" 
            os.startfile(path)

        elif 'open notepad' in query:
            var.set("Opening Notepad")
            window.update()
            speak("Opening Notepad")
            path="C:\\Windows\\System32\\notepad.exe"
            os.startfile(path)

        elif 'open chrome' in query:
            var.set("Opening Google Chrome")
            window.update()
            speak("Opening Google Chrome")
            path = "C:\Program Files (x86)\Google\Chrome\Application\\chrome.exe" 
            os.startfile(path)

        elif 'open internet explorer' in query:
            var.set("Opening Internet Explorer")
            window.update()
            speak("Opening Internet Explorer")
            path = "C:\\Program Files\\Internet Explorer\\iexplore.exe"
            os.startfile(path)

        elif '.com' in query:
            try:
                var.set("Searching Google...")
                window.update()
                speak("Searching Google...")
                wb.get(chrome_path).open(query)
            except Exception as e:
                speak("Search failed. Please try again!")

        elif 'youtube' in query:
            expr=re.search('youtube (.+)', query)
            if expr:
                domain=query.split("youtube",1)[1] 
                query_string=urllib.parse.urlencode({"search_query" : domain})
                html_content=urllib.request.urlopen("http://www.youtube.com/results?"+query_string) 
                search_results=re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
                pass

        elif 'send mail' in query:
            try:
                var.set("Leave a message..")
                window.update()
                speak('Leave a message..')
                content=takeCommand()
                to='shefali.22899@gmail.com'
                sendEmail(to, content)
                var.set('Email sent!')
                window.update()
                speak('Email sent!')
            except Exception as e:
                print(e)
                var.set("Email can not be sent!")
                window.update()
                speak('Email can not be sent!')    


            #INFORMAL CONVERSATION

        elif 'are you human' in query:
            var.set("I'm really personable.")
            window.update()
            speak("I'm really personable.")

        elif 'who are you' in query:
            var.set("I'm a voice activated desktop assistant, named after F.R.I.D.A.Y., an A.I from the Marvel Comics")
            window.update()
            speak("I'm a voice activated desktop assistant, named after FRIDAY, an artificial intelligence from the Marvel Comics.")

        elif 'self-destruct' in query:
            var.set("Self-destructing in 3!. 2!. 1!...")
            window.update()
            speak("Self-destructing in 3!. 2!. 1!...")
            var.set("Actually, I think I'll stick around. ha ha.")
            window.update()
            speak("Actually, I think I'll stick around. ha ha.")
    
        elif 'hello' in query:
            var.set('Hello! How are you?')
            window.update()
            speak('Hello! How are you?')

        elif 'hi' in query:
            var.set('Hi! How are you?')
            window.update()
            speak('Hi! How are you?')

        elif 'how are you' in query:
            var.set('I am great! And at your service!')
            window.update()
            speak('I am great! And at your service!')

        elif 'thank you' in query:
            var.set("You're most welcome!")
            window.update()
            speak("You're most welcome!")

        elif 'your name' in query:
            var.set("I am F.R.I.D.A.Y!")
            window.update()
            speak('I am FRIDAY!')

        elif 'creator' in query:
            var.set('My Creator is Shefali Sharma')
            window.update()
            speak('My Creator is Shefali Sharma')

        else:
            var.set("Could not understand that.. Please try again.")
            window.update()
            speak('Could not understand that.. Please try again.')
            break


def update(ind): #Update the window frames after every change
    frame=frames[(ind)%100]
    ind+=1
    label.configure(image=frame)
    window.after(100, update, ind)

label2=Label(window, textvariable=var1, bg='#FAB60C')
label2.config(font=("Courier", 20))
var1.set('User Said:')
label2.pack()

label1=Label(window, textvariable=var, bg='#ADD8E6')
label1.config(font=("Courier", 20))
var.set('Welcome!')
label1.pack()

frames=[PhotoImage(file='Assistant.gif', format='gif -index %i' %(i)) for i in range(100)]
window.title('F.R.I.D.A.Y')

label=Label(window,width=500,height=500)
label.pack()
window.after(0,update,0)

btn0=Button(text='WISH ME', width=20, command=wish_user, bg='#5C85FB')
btn0.config(font=("Courier", 12))
btn0.pack()
btn1=Button(text='PLAY', width=20, command=play, bg='#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2=Button(text='EXIT', width=20, command=window.destroy, bg='#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()

window.mainloop()
