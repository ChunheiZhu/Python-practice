from vpython import *
import numpy as np
import time
clockR = 2
clockT = clockR/10
majorTickL = clockR/7
majorTickT = 2*np.pi*clockR/400
majorTickW = clockT*1.2
manorTickL = clockR/12
manorTickT = 2*np.pi*clockR/600
manorTickW = clockT*1.2
minuteHandL = clockR-majorTickL
minuteHandT = minuteHandL/25
mniuteHandOffset = clockT/2 + minuteHandT
hubRadius = clockT/2
hourHandL = .75*minuteHandL
hourHandT = minuteHandT*1.25
hourHandOffset = clockT/2 + hourHandT
hourRadius = clockT/2
hourAngle = np.pi/2
minuteAngle = np.pi/2
minInc = .0001
hourInc = minInc/12
secondHandL = clockR - majorTickL/2
secondHandT = minuteHandL/50
secondHandOffset = clockT*1.5 + minuteHandT
secondAngle = np.pi/2
secondInc = minInc*60

cityt = {
    'UTC': 0,
    'New York': -4,
    'London': 0,
    'Berlin': 1,
    'Beijing': 8,
    'Tokyo': 9,
    'Sydney': 10
}
bcolor = {
    'white':color.white,
    'black':color.black,
    'blue':color.blue,
    'cyan':color.cyan,
    'green':color.green
}

currentcity = 'UTC'
currentoffset = cityt[currentcity]
for theta in np.linspace(0,2*np.pi,13):
    majorTick = box(axis = vector(clockR*np.cos(theta),clockR*np.sin(theta),0),
                    color = color.black,length = majorTickL,width = majorTickW,
                    height = majorTickT,pos = vector((clockR-majorTickL/2)*np.cos(theta),(clockR-majorTickL/2)*np.sin(theta),0))
for theta in np.linspace(0,2*np.pi,61):
    manorTick = box(axis = vector(clockR*np.cos(theta),clockR*np.sin(theta),0),
                    color = color.black,length = manorTickL,width = manorTickW,height = manorTickT,
                    pos = vector((clockR-manorTickL/2)*np.cos(theta),(clockR-manorTickL/2)*np.sin(theta),0))
clockFace = cylinder(axis = vector(0,0,1),color = vector(0,1,.8),length = clockT,radius = clockR,pos = vector(0,0,-clockT/2))
minuteHand = arrow(axis = vector(0,1,0),color = color.red,shaftwidth = minuteHandT,
                   length = minuteHandL,pos = vector(0,0,mniuteHandOffset))
hourHand = arrow(axis = vector(0,1,0),color = color.red,shaftwidth = hourHandT,
                 length = hourHandL,pos = vector(0,0,hourHandOffset))
hub = cylinder(axis = vector(0,0,1),color = color.red,radius = hubRadius,length = 2*clockT)
secondHand = arrow(axis = vector(0,1,0),color = color.red,shaftwidth = secondHandT,
                   length = secondHandL,pos = vector(0,0,secondHandOffset))
myLabel = label(text=f'{currentcity} Time', pos=vector(0,1.3*clockR,0), height=16, box=False, color=color.orange)
Angle = np.pi/2
AngleInc = -2*np.pi/12
Angle = Angle + AngleInc
numH = clockR/6

def pickcity(x):
    global currentcity, currentoffset
    currentcity = x.selected
    currentoffset = cityt[currentcity]
    myLabel.text = f'{currentcity} Time'
def backcolor(x):
    clockFace.color = bcolor[x.selected]
scene.append_to_caption('\n\n')
wtext(text = 'Choose Font size')
scene.append_to_caption('\n\n')
def setFontSize(x):
    global numH
    if x.selected == 'small':
        numH = clockR/9
    elif x.selected == 'medium':
        numH = clockR/6
    elif x.selected == 'large':
        numH = clockR/3
    for i, t in enumerate(clockNums):
        theta = np.pi/2 - i*(2*np.pi/12)
        t.height = numH
        t.pos = vector(clockR*.75*np.cos(theta),
                       clockR*.75*np.sin(theta) - numH/2, 0)
clockNums = []
menu(bind = setFontSize,choices = ['small','medium','large'])
scene.append_to_caption('\n\n')
wtext(text = "Select City Timezone")
scene.append_to_caption('\n\n')
menu(bind = pickcity, choices = list(cityt.keys()))
scene.append_to_caption('\n\n')
wtext(text = "Select Clock Face Color")
scene.append_to_caption('\n\n')
menu(bind = backcolor, choices = list(bcolor.keys()))
myLabel.text = f'{currentcity} Time'
for i in range(1,13,1):
    clockNum = text(align='center', text=str(i),pos=vector(clockR*.75*np.cos(Angle), clockR*.75*np.sin(Angle) - numH/2, 0),height=numH, depth=clockT, color=color.orange)
    clockNums.append(clockNum)
    Angle = Angle + AngleInc
while True:
    rate(50)
    utc_ts = time.time()           
    citytm = time.gmtime(utc_ts + currentoffset*3600)
    hour   = citytm.tm_hour % 12  
    minute = citytm.tm_min
    second = citytm.tm_sec
    hourAngle = -((hour+minute/60)/12)*2*np.pi + np.pi/2
    minuteAngle = -((minute+second/60)/60)*2*np.pi + np.pi/2
    secondAngle = -(second/60)*2*np.pi + np.pi/2
    print(second)
    hourHand.axis = vector(hourHandL*np.cos(hourAngle),hourHandL*np.sin(hourAngle),0)
    minuteHand.axis = vector(minuteHandL*np.cos(minuteAngle),minuteHandL*np.sin(minuteAngle),0)
    secondHand.axis = vector(secondHandL*np.cos(secondAngle),secondHandL*np.sin(secondAngle),0)