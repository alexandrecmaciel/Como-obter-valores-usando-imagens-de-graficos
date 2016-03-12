# ROTINA PARA OBTER DADOS EXPERIMENTAIS DE GRAFICOS NO FORMATO PNG
# ALEXANDRE DE CASTRO MACIEL, DEP. DE FISICA DA UFPI
# MARCO DE 2016
# EXPLICACAO EM https://goo.gl/3rDLZ8

import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook
import os
import os.path

filename = 'TestGraph004.PNG'
Xa        = 0.5
Xb        = 1.5
log10X    = False
lognX     = False
Ya        = 1e-6
Yb        = 1e-4
log10Y    = True
lognY     = False
drawXhead = True

if log10X :
    Xa = np.log10(Xa)
    Xb = np.log10(Xb)
if log10Y :
    Ya = np.log10(Ya)
    Yb = np.log10(Yb)
if lognX :
    Xa = np.log(Xa)
    Xb = np.log(Xb)
if lognY :
    Ya = np.log(Ya)
    Yb = np.log(Yb)

url = os.path.dirname(os.path.abspath(__file__))
datafile = cbook.get_sample_data(url+'/'+filename)
img = imread(datafile)

fig = plt.figure()

fig.clear()
plot = fig.add_subplot(111)
plot.imshow(img, zorder=0, extent=[0.0, 1.0, 0.0, 1.0])

XaxisX = []
XaxisY = []
YaxisX = []
YaxisY = []
dataX  = []
dataY  = []
getX   = []
getY   = []

def onclick(event):
    x, y = event.xdata, event.ydata
    if x != None and y != None :
        plot(x, y)
    else :
        outputData()
    return

def plot(x, y) :
    global XaxisX, XaxisY, YaxisX, YaxisY, dataX, dataY, Xa, Xb, Ya, Yb
    global XzeroX, XzeroY, YzeroX, YzeroY, drawXhead

    if   len(XaxisX) < 2 :
        XaxisX.append(x)
        XaxisY.append(y)
    elif len(YaxisX) < 2 :
        YaxisX.append(x)
        YaxisY.append(y)
    else :
        dataX.append(x)
        dataY.append(y)

    fig.clear()
    plot = fig.add_subplot(111)
    if len(XaxisX) :

        plot.scatter(XaxisX, XaxisY, s=40, c='red', marker='x', zorder=1)

    if len(XaxisX) == 2 :

        XzeroX = XaxisX[0]-(XaxisX[1]-XaxisX[0])/(Xb-Xa)*Xa
        XzeroY = XaxisY[0]-(XaxisY[1]-XaxisY[0])/(Xb-Xa)*Xa

        if XaxisX[1] != XaxisX[0] :
            a = XaxisY[0]-(XaxisY[1]-XaxisY[0])/(XaxisX[1]-XaxisX[0])*XaxisX[0]
            b = (XaxisY[1]-XaxisY[0])/(XaxisX[1]-XaxisX[0])

            newX = [0.0, 1.0]
            newY = [a, a+b]

            plot.plot(newX, newY, 'red', zorder=2)
        else :
            plot.axvline(x=XaxisX[0], color='red')

        plot.scatter([XzeroX], [XzeroY], c='red', zorder=3)

    if len(YaxisX) :

        plot.scatter(YaxisX, YaxisY, s=40, c='green', marker='x', zorder=1)

    if len(YaxisX) == 2 :

        YzeroX = YaxisX[0]-(YaxisX[1]-YaxisX[0])/(Yb-Ya)*Ya
        YzeroY = YaxisY[0]-(YaxisY[1]-YaxisY[0])/(Yb-Ya)*Ya

        if YaxisX[1] != YaxisX[0] :
            a = YaxisY[0]-(YaxisY[1]-YaxisY[0])/(YaxisX[1]-YaxisX[0])*YaxisX[0]
            b = (YaxisY[1]-YaxisY[0])/(YaxisX[1]-YaxisX[0])

            newX = [0.0, 1.0]
            newY = [a, a+b]

            plot.plot(newX, newY, 'green', zorder=2)
        else :
            plot.axvline(x=YaxisX[0], color='green')

        plot.scatter([YzeroX], [YzeroY], c='green', zorder=3)

    if len(dataX) :
        plot.scatter(dataX, dataY, s=50, c='cyan', edgecolors='black', zorder=3)
        if drawXhead :
            for i, j in zip(dataX, dataY) :
                plot.axvline(x=i, color='cyan')
                plot.axhline(y=j, color='cyan')

    plot.imshow(img, zorder=0, extent=[0.0, 1.0, 0.0, 1.0])
    fig.canvas.draw()

    return

def outputData() :
    global XaxisX, XaxisY, YaxisX, YaxisY, dataX, dataY, Xa, Xb, Ya, Yb
    global XzeroX, XzeroY, YzeroX, YzeroY, log10X, log10Y
    global getX, getY

    for i, j in zip(dataX, dataY) :

        Pline = [i-XzeroX, j-XzeroY]
        modPline = np.sqrt(Pline[0]**2+Pline[1]**2)
        deltaX = modPline * (i-XzeroX) / modPline
        getX.append(deltaX * (Xb-Xa) / (XaxisX[1]-XaxisX[0]))

        Pline = [i-YzeroX, j-YzeroY]
        modPline = np.sqrt(Pline[0]**2+Pline[1]**2)
        deltaY = modPline * (j-YzeroY) / modPline
        getY.append(deltaY * (Yb-Ya) / (YaxisY[1]-YaxisY[0]))

    for ii, jj in zip (getX, getY) :
        if log10X :
            ii = 10**ii
        if log10Y :
            jj = 10**jj

        if lognX :
            ii = np.exp(ii)
        if lognY :
            jj = np.exp(jj)

        print ii, jj

    fig.canvas.mpl_disconnect(cid)

    return

cid = fig.canvas.mpl_connect('button_press_event', onclick)