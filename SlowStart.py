#!
#CarpeDiem.py
#press button to start the day - display clock current weather, top news stories,


import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import datetime, requests,bs4, webbrowser, platform
from PIL import ImageTk, Image
try:
    import os
except:
    import subprocess


daysOfWeek=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
newsStoryLabelList=[]
linklist=[]
headlineList=[]
linklistGlobe=[]
headlineListGlobe=[]
openTimes=True
openGlobe=False
currentSource='New York Times:'

#House Keeping portion

def smart_truncate(content, length=69, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

#Clock Portion
    
def clock():
    global daysOfWeek
    dateTime=datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S/%p")
    date,time1=dateTime.split()
    time2,time3=time1.split('/')
    hour,minutes,seconds=time2.split(':')
    day = datetime.datetime.today().weekday()
    if int(hour)>12 and int(hour)<24:
        time=str(int(hour)-12)+':'+minutes+':'+seconds+' '+time3
    else:
        time=time2+' '+time3
    for i in range(7):
        if i==day:
            day=daysOfWeek[i]
    date=date+'  '+day
    dateLabel.config(text=date)
    clockLabel.config(text=time)
    clockLabel.after(1000, clock)
    
#Hyperlink Command Portion

def callback(label):
    global headlineList, headlineListGlobe, linklist, linklistGlobe
    try:
        if openTimes==True:
            for entry in headlineList:
                if entry==label['text']:
                    index=headlineList.index(entry)
            webbrowser.open_new(linklist[index])
        if openGlobe==True:
            for entry in headlineListGlobe:
                if entry==label['text']:
                    index=headlineListGlobe.index(entry)
            webbrowser.open_new(linklistGlobe[index])
    except:
        return
       
#Calender App Command

def openCal():
    if platform.system()!='Windows':
        os.system(' open /System/Applications/Calendar.app')
    else:
        try:
            webbrowser.open('https://calendar.google.com/calendar')
        except:
            return

        
#Weather Scrapper and Parser Command Portion

def weatherParser():
    global styleWeatherNum
    try:
        weatherDotCom=requests.get('https://weather.com/weather/today/l/471ac387b9d9b7d5f177db994944383904c34ee39a5c8074e587521005254553')
        weatherDotCom.raise_for_status()
        weatherSoup=bs4.BeautifulSoup(weatherDotCom.text,'html.parser')
        tempElems=weatherSoup.find_all("span",{"class":"CurrentConditions--tempValue--3KcTQ"})
        descElems=weatherSoup.find_all("div",{"class":"CurrentConditions--phraseValue--2xXSr"})
        skyElems=weatherSoup.find_all("svg",{"class":"CurrentConditions--wxIcon--2cDUg Icon--icon--2AbGu Icon--fullTheme--3jU2v"})
        highLowElems=weatherSoup.find_all("div",{"class":"CurrentConditions--tempHiLoValue--A4RQE"})
        sky='  '+skyElems[0].getText()
        highLow=highLowElems[0].getText()
        temp=tempElems[0].getText()
        temp=temp+'F'
        desc=descElems[0].getText()+'     '
        weatherDescLabel.config(text=desc)
        if "sunny" in skyElems[0].getText().lower().split():
            weatherSkyLabel.config(image=sunImage)
        elif "cloudy" in skyElems[0].getText().lower().split():
            weatherSkyLabel.config(image=cloudyImage)
        elif "snow" in skyElems[0].getText().lower().split() or 'mix' in skyElems[0].getText().lower().split() :
            weatherSkyLabel.config(image=snowImage)
        elif "rain" in skyElems[0].getText().lower().split() or 'showers' in skyElems[0].getText().lower().split():
            weatherSkyLabel.config(image=rainImage)
        elif "night" in skyElems[0].getText().lower().split():
            weatherSkyLabel.config(image=nightImage)
        elif "windy" in skyElems[0].getText().lower().split() or "wind" in skyElems[0].getText().lower().split():
            weatherSkyLabel.config(image=windyImage)
        else:
            weatherSkyLabel.config(text=sky)
            print(skyElems[0].getText().split())
        weatherHighLowLabel.config(text=highLow)
        weatherTempLabel.config(text=temp)
        if int(temp[0:-2]) >= 90:
            styleWeatherNum.configure("wn.TLabel",foreground='red')
        elif int(temp[0:-2]) >= 80 and int(temp[0:-2]) < 90:
            styleWeatherNum.configure("wn.TLabel",foreground='orange')
        elif int(temp[0:-2]) >= 70 and int(temp[0:-2]) < 80:
            styleWeatherNum.configure("wn.TLabel",foreground='yellow')
        elif int(temp[0:-2]) >= 45 and int(temp[0:-2]) < 70:
            styleWeatherNum.configure("wn.TLabel",foreground='green')
        elif int(temp[0:-2]) >= 20 and int(temp[0:-2]) < 45:
            styleWeatherNum.configure("wn.TLabel",foreground='blue')
        elif int(temp[0:-2]) < 20:
            stlyeWeatherNum.configure(foreground='#A5F2F3')
    except:
        weatherSkyLabel.config(text='Cannot access weather')

#News Scrapper and Parser Command Portion

def timeNewsParser():
    global headlineList,linklist
    try:
        times=requests.get('https://www.nytimes.com')
        timesSoup=bs4.BeautifulSoup(times.text,'html.parser')
        links=timesSoup.find_all("a",{"class":"css-kej3w4"})
        i=0
        while (len(linklist)<=8):
            if linklist==[] and links[i].string!=None:
                links[i].find('a',href=True)
                linklist.append(links[i]['href'])
                headlineList.append(smart_truncate(links[i].getText()))
            if i!=0:
                links[i].find('a',href=True)
                if links[i]['href'] != linklist[-1] and links[i].string!=None:
                    linklist.append(links[i]['href'])
                    headlineList.append(smart_truncate(links[i].getText()))
            i+=1
    except:
        for i in range(0,8):
            if i ==0:
                headlineList.append('Cannot access news')
                linklist.append('')
            else:
                headlineList.append('')
                linklist.append('')

#Globe Scrapper and Parser Command Portion

def globeNewsParser():
    global headlineListGlobe, linklistGlobe
    try:
        globe=requests.get('https://www.bostonglobe.com')
        globeWebsite='https://www.bostonglobe.com'
        globeSoup=bs4.BeautifulSoup(globe.text,'html.parser')
        headlinesGlobe=globeSoup.find_all("h2",{"class":"headline | bold border_box font_secondary margin_bottom"})
        linksGlobe=globeSoup.find_all("a",{"class":"card color_inherit"})
        y=0
        while (len(linklistGlobe)<8):
            if linklistGlobe==[] and headlinesGlobe[y].string!=None:
                linksGlobe[y].find('a',href=True)
                linklistGlobe.append(globeWebsite+linksGlobe[y]['href'])
                headlineListGlobe.append(smart_truncate(headlinesGlobe[y].getText()))
            if y!=0:
                linksGlobe[y].find('a',href=True)
                if linksGlobe[y]['href'] != linklistGlobe[-1] and headlinesGlobe[y].string!=None:
                    linklistGlobe.append(linksGlobe[y]['href'])
                    headlineListGlobe.append(smart_truncate(headlinesGlobe[y].getText()))
            y+=1
    except:
        for i in range(0,8):
            if i ==0:
                headlineListGlobe.append('Cannot access news')
                linklistGlobe.append('')
            else:
                headlineListGlobe.append('')
                linklistGlobe.append('')

globeNewsParser()
timeNewsParser()

#News Selection Button Globe Portion

def selectGlobe():
    global linklistGlobe, headlineListGlobe, openTimes, openGlobe
    openTimes=False
    openGlobe=True
    currentSource='The Boston Globe:'
    topStoriesLabel.config(text="Today's top stories "+currentSource)
    if plusButton['text']=='-':
        PlusMinus()
    newsLabel1.config(text=headlineListGlobe[0])
    newsLabel2.config(text=headlineListGlobe[1])
    newsLabel3.config(text=headlineListGlobe[2])
    newsLabel4.config(text=headlineListGlobe[3])
    newsLabel5.config(text=headlineListGlobe[4]+'\n')
    newsLabel6.config(text=headlineListGlobe[5])
    newsLabel7.config(text=headlineListGlobe[6])
    newsLabel8.config(text=headlineListGlobe[7])

#News Selection Button Times Portion

def selectTimes():
    global linklistGlobe, headlineListGlobe, openTimes, openGlobe,currentSource
    openTimes=True
    openGlobe=False
    currentSource='The New York Times:'
    topStoriesLabel.config(text="Today's top stories "+currentSource)
    if plusButton['text']=='-':
        PlusMinus()
    newsLabel1.config(text=headlineList[0])
    newsLabel2.config(text=headlineList[1])
    newsLabel3.config(text=headlineList[2])
    newsLabel4.config(text=headlineList[3])
    newsLabel5.config(text=headlineList[4]+'\n')
    newsLabel6.config(text=headlineList[5])
    newsLabel7.config(text=headlineList[6])
    newsLabel8.config(text=headlineList[7])


    
#Plus Minus Button Command Portion

def PlusMinus():
    global linklistGlobe, headlineListGlobe, openTimes, openGlobe,currentSource
    if plusButton['text']=='+':
        if openTimes==True:
            newsLabel6.config(text=headlineList[5])
            newsLabel7.config(text=headlineList[6])
            newsLabel8.config(text=headlineList[7]+'\n')
            newsLabel5.config(text=headlineList[4])
            newsLabel6.pack(anchor='center',fill='both')
            newsLabel6.bind("<Button-1>", lambda e: callback(newsLabel6))
            newsLabel7.pack(anchor='center',fill='both')
            newsLabel7.bind("<Button-1>", lambda e: callback(newsLabel7))
            newsLabel8.pack(anchor='center',fill='both')
            newsLabel8.bind("<Button-1>", lambda e: callback(newsLabel8))
        if openGlobe==True:
            newsLabel6.config(text=headlineListGlobe[5])
            newsLabel7.config(text=headlineListGlobe[6])
            newsLabel8.config(text=headlineListGlobe[7]+'\n')
            newsLabel5.config(text=headlineListGlobe[4])
            newsLabel6.pack(anchor='center',fill='both')
            newsLabel6.bind("<Button-1>", lambda e: callback(newsLabel6))
            newsLabel7.pack(anchor='center',fill='both')
            newsLabel7.bind("<Button-1>", lambda e: callback(newsLabel7))
            newsLabel8.pack(anchor='center',fill='both')
            newsLabel8.bind("<Button-1>", lambda e: callback(newsLabel8))
        plusButton.config(text='-')
    elif plusButton['text']=='-':
        newsLabel6.pack_forget()
        newsLabel7.pack_forget()
        newsLabel8.pack_forget()
        plusButton.config(text='+')
    
#Window configuration portion

now=datetime.datetime.now()
if int(now.hour)>21 or int(now.hour)<5:
    themeCurrent='equilux'
else:
    themeCurrent='yaru'
window=ThemedTk(theme=themeCurrent)
window.title("Slow Start")
             
#Style Portion

styleClock=ttk.Style()
styleClock.configure("clock.TLabel",font='calibri 50 bold',borderwidth=20,padding=10,anchor=tk.CENTER)
styleDate=ttk.Style()
styleDate.configure("date.TLabel",font='calibri 30 underline',borderwidth=25,anchor=tk.CENTER)
styleLabels=ttk.Style()
styleLabels.configure("labels.TLabel",font='calibri 24 bold',borderwidth=5, padding=10, anchor=tk.CENTER)
styleWeatherNum=ttk.Style()
styleWeatherNum.configure("wn.TLabel",font='calibri 40 bold',borderwidth=15)
styleWeatherOth=ttk.Style()
styleWeatherOth.configure("wo.TLabel",font='calibri 30',borderwith=15)
styleNews=ttk.Style()
styleNews.configure("news.TLabel",font='calibri 18',borderwidth=10,padding=5,anchor=tk.LEFT)
styleBlank=ttk.Style()
styleBlank.configure("blank.TLabel",borderwidth=10,anchor=tk.CENTER,width=60)
styleFrame=ttk.Style()
styleFrame.configure("frame.TFrame",anchor=tk.CENTER,borderwidth=25)
styleButton=ttk.Style()
styleButton.configure("buttonB.TButton",anchor=tk.CENTER)


#Widgets and Packing/Grid Portion

clockLabel=ttk.Label(master=window,style="clock.TLabel")
dateLabel=ttk.Label(master=window,style="date.TLabel")

weatherTitleLabel=ttk.Label(master=window,text="Today's local weather:",style="labels.TLabel")
weatherFrame=ttk.Frame(master=window)
weatherFrame.rowconfigure([0],weight=1)
weatherFrame.columnconfigure([0,1,2,3,4,5,6],weight=1)

weatherTempLabel=ttk.Label(master=weatherFrame,style="wn.TLabel")
weatherDescLabel=ttk.Label(master=weatherFrame,style="wo.TLabel")
weatherHighLowLabel=ttk.Label(master=weatherFrame,style="wo.TLabel")
blankLabel=ttk.Label(master=weatherFrame,style="blank.TLabel")
weatherSkyLabel=ttk.Label(master=weatherFrame,style="wo.TLabel")
sunImage=ImageTk.PhotoImage(Image.open("/Users/timothyphoenix/pythoncodes/SlowStart/sun.png"))
rainImage=ImageTk.PhotoImage(Image.open("/Users/timothyphoenix/pythoncodes/SlowStart/rain.png"))
snowImage=ImageTk.PhotoImage(Image.open("/Users/timothyphoenix/pythoncodes/SlowStart/snow.png"))
nightImage=ImageTk.PhotoImage(Image.open("/Users/timothyphoenix/pythoncodes/SlowStart/night.png"))
cloudyImage=ImageTk.PhotoImage(Image.open("/Users/timothyphoenix/pythoncodes/SlowStart/cloud.png"))
windyImage=ImageTk.PhotoImage(Image.open("/Users/timothyphoenix/pythoncodes/SlowStart/wind.png"))

topStoriesLabel=ttk.Label(master=window,text="Today's top stories "+currentSource, style="labels.TLabel")

selectionButtonFrame=ttk.Frame(master=window,style="frame.TFrame")
selectionButtonFrame.rowconfigure(0,weight=1)
selectionButtonFrame.columnconfigure([0,1,2],weight=1)

globeButton=ttk.Button(master=selectionButtonFrame,text='GLOBE',command=selectGlobe,style="button.TButton")
timesButton=ttk.Button(master=selectionButtonFrame,text='NYT',style="button.TButton",command=selectTimes)
plusButton=ttk.Button(master=selectionButtonFrame,text='+',style="button.TButton",command=PlusMinus)

clockLabel.pack(fill='both')

dateLabel.pack(fill='both')

weatherTitleLabel.pack(fill='both')

weatherFrame.pack(anchor='center',fill='both')

weatherTempLabel.grid(row = 0, column = 2 ,sticky='nsew')
#weatherDescLabel.grid(row=1,column=2,sticky='e')
weatherHighLowLabel.grid(row=0,column=4,sticky='nsew')
#blankLabel.grid(row=1,column=3,sticky='nsew')
weatherSkyLabel.grid(row=0,column=3,sticky='nsew')

topStoriesLabel.pack(anchor='center',fill='both')

selectionButtonFrame.pack(anchor=tk.CENTER,fill='both')

globeButton.grid(row=0,column=0,sticky='nsew')
timesButton.grid(row=0,column=1,sticky='nsew')
plusButton.grid(row=0,column=2,sticky='nsew')

newsLabel1=ttk.Label(master=window, text=headlineList[0],style="news.TLabel")
newsLabel1.pack(anchor='center',fill='both')
newsLabel1.bind("<Button-1>", lambda e: callback(newsLabel1))

newsLabel2=ttk.Label(master=window,text=headlineList[1],style="news.TLabel")
newsLabel2.pack(anchor='center',fill='both')
newsLabel2.bind("<Button-1>", lambda e: callback(newsLabel2))

newsLabel3=ttk.Label(master=window,text=headlineList[2],style="news.TLabel")
newsLabel3.pack(anchor='center',fill='both')
newsLabel3.bind("<Button-1>", lambda e: callback(newsLabel3))

newsLabel4=ttk.Label(master=window,text=headlineList[3],style="news.TLabel")
newsLabel4.pack(anchor='center',fill='both')
newsLabel4.bind("<Button-1>", lambda e: callback(newsLabel4))

newsLabel5=ttk.Label(master=window,text=headlineList[4]+'\n',style="news.TLabel")
newsLabel5.pack(anchor='center',fill='both')
newsLabel5.bind("<Button-1>", lambda e: callback(newsLabel5))

newsLabel6=ttk.Label(master=window,style="news.TLabel")
newsLabel7=ttk.Label(master=window,style="news.TLabel")
newsLabel8=ttk.Label(master=window,style="news.TLabel")

weatherFrame.bind("<Button-1>", lambda e: webbrowser.open_new('https://weather.com/weather/today/l/471ac387b9d9b7d5f177db994944383904c34ee39a5c8074e587521005254553'))
dateLabel.bind("<Button-1>", lambda e: openCal())

weatherParser()
clock()
window.mainloop()
