from vpython import *
import numpy as np
import time

# --- 参数 ---
clockR = 2
clockT = clockR/10
minuteHandL = clockR - clockT*0.7
minuteHandT = minuteHandL/25
minuteHandOffset = clockT/2 + minuteHandT
hourHandL = 0.75*minuteHandL
hourHandT = minuteHandT*1.25
hourHandOffset = clockT/2 + hourHandT
secondHandL = minuteHandL
secondHandT = minuteHandL/50
secondHandOffset = clockT*1.5 + minuteHandT

# --- 城市与颜色（固定偏移；未处理DST） ---
cityt = {'UTC':0,'New York':-4,'London':0,'Berlin':1,'Beijing':8,'Tokyo':9,'Sydney':10}
bcolor = {'white':color.white,'black':color.black,'blue':color.blue,'cyan':color.cyan,'green':color.green}
currentcity = 'UTC'
currentoffset = cityt[currentcity]

# --- 场景+表盘（尽量轻量） ---
scene.caption = ''  # 初始化 caption，避免历史 caption 干扰
clockFace = cylinder(axis=vector(0,0,1), color=vector(0,1,.8), length=clockT, radius=clockR, pos=vector(0,0,-clockT/2))
minuteHand = arrow(axis=vector(0,1,0), color=color.red, shaftwidth=minuteHandT, length=minuteHandL, pos=vector(0,0,minuteHandOffset))
hourHand   = arrow(axis=vector(0,1,0), color=color.red, shaftwidth=hourHandT,   length=hourHandL,   pos=vector(0,0,hourHandOffset))
secondHand = arrow(axis=vector(0,1,0), color=color.red, shaftwidth=secondHandT, length=secondHandL, pos=vector(0,0,secondHandOffset))

# 用 label（2D 文本）替代 3D text，轻很多
title_lbl = label(text=f'{currentcity} Time', pos=vector(0,1.3*clockR,0), height=16, box=False, color=color.orange)

# --- 菜单回调 ---
def pickcity(x):
    global currentcity, currentoffset
    sel = x.selected
    if sel in cityt:
        currentcity = sel
        currentoffset = cityt[sel]
        title_lbl.text = f'{currentcity} Time'

def backcolor(x):
    sel = x.selected
    if sel in bcolor:
        clockFace.color = bcolor[sel]

# --- 菜单（只画一次） ---
menu(bind=pickcity, choices=list(cityt.keys()))
scene.append_to_caption('   ')
menu(bind=backcolor, choices=list(bcolor.keys()))
scene.append_to_caption('\n')

# --- 主循环 ---
while True:
    rate(20)  # 10~30 都可以
    utc_ts = time.time()
    citytm = time.gmtime(utc_ts + currentoffset*3600)
    h = citytm.tm_hour % 12
    m = citytm.tm_min
    s = citytm.tm_sec

    hourAngle   = -((h + m/60)/12)*2*np.pi + np.pi/2
    minuteAngle = -((m + s/60)/60)*2*np.pi + np.pi/2
    secondAngle = -(s/60)*2*np.pi + np.pi/2

    hourHand.axis   = vector(hourHandL*np.cos(hourAngle),     hourHandL*np.sin(hourAngle),     0)
    minuteHand.axis = vector(minuteHandL*np.cos(minuteAngle), minuteHandL*np.sin(minuteAngle), 0)
    secondHand.axis = vector(secondHandL*np.cos(secondAngle), secondHandL*np.sin(secondAngle), 0)
