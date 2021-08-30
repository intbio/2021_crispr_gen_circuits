import bokeh
from bokeh import events
from bokeh.plotting import Figure, output_file, show
import math
#import scipy as sp
#import numpy as np
from bokeh.layouts import row, column
from bokeh.models import CustomJS, ColumnDataSource, Button, PreText, TextInput


#Variables
n = 2 #Hill coefficient
Km = 40 #monomeres per cell
beta = 0.2
alphaO = 0
alpha = 216.4
#Initial concentrations of proteins/mRNAs
CmtetRO = 0
CmlambdaO = 0
CmlacIO = 0.1
CptetRO = 0
CplambdaO = 0
CplacIO = 0
CmtetR = 0
Cmlambda = 0
CmlacI = 0
CptetR = 0
Cplambda = 0
CplacI = 0



#Plot building
Span = 10000
ylacI = [0]*Span
ytetR = [0]*Span
ylambda = [0]*Span
mlacI = [0]*Span
mtetR = [0]*Span
mlambda = [0]*Span
mlacI = [0]*Span
mtetR = [0]*Span
mlambda = [0]*Span
x = [dt*0.1 for dt in range(0, Span)]
dt = 0.1
fig = Figure(plot_width=700, plot_height=500, title="Repressilator model",x_axis_label='Time/mRNA half-life time', y_axis_label='Protein concentration, in units of Km')



"""def protConc(CO, CpO, RP, y):
    for i in range(0,1000):
        if (i == 0):
            Cm = CO
            Cp = CpO
        else:
            Cm = Cm + alphaO*dt - Cm*dt + alpha*dt/(1+math.pow(RP,n))
            Cp = Cp - Cp*dt*beta + beta*Cm*dt
        y[i] = Cp"""
    




for i in range(0,Span):
    if (i == 0):
            CmlacI = CmlacIO
            CmtetR = CmtetRO
            Cmlambda = CmlambdaO
            CplacI = CplacIO
            CptetR = CptetRO
            Cplambda = CplambdaO
    else:  
        CmlacI = mlacI[i-1] + alphaO*dt - mlacI[i-1]*dt + alpha*dt/(1+math.pow(ylambda[i-1],n))
        CplacI = ylacI[i-1] - ylacI[i-1]*dt*beta + beta*mlacI[i-1]*dt
        CmtetR = mtetR[i-1] + alphaO*dt - mtetR[i-1]*dt + alpha*dt/(1+math.pow(ylacI[i-1],n))
        CptetR = ytetR[i-1] - ytetR[i-1]*dt*beta + beta*mtetR[i-1]*dt
        Cmlambda = mlambda[i-1] + alphaO*dt - mlambda[i-1]*dt + alpha*dt/(1+math.pow(ytetR[i-1],n))
        Cplambda = ylambda[i-1] - ylambda[i-1]*dt*beta + beta*mlambda[i-1]*dt
    mlacI[i] = CmlacI
    mtetR[i] = CmtetR
    mlambda[i] = Cmlambda
    ylacI[i] = CplacI
    ytetR[i] = CptetR
    ylambda[i] = Cplambda


source = ColumnDataSource(data=dict(x=x, ylacI=ylacI, ytetR=ytetR, ylambda=ylambda))

callback = CustomJS(args=dict(source=source), code="""
    var n = 2 
    var Km = 40 
    var beta = parseFloat(beta.value)
    var alphaO = parseFloat(alphaO.value)
    var alpha = parseFloat(alpha.value)
    var CmtetRO = parseFloat(CmtetRO.value)
    var CmlambdaO = parseFloat(CmlambdaO.value)
    var CmlacIO = parseFloat(CmlacIO.value)
    var CptetRO = parseFloat(CptetRO.value)
    var CplambdaO = parseFloat(CplambdaO.value)
    var CplacIO = parseFloat(CplacIO.value)
    var CmtetR = 0
    var Cmlambda = 0
    var CmlacI = 0
    var CptetR = 0
    var Cplambda = 0
    var CplacI = 0
    var Span = 10000
    var data = source.data
    var dt = 0.1
    var ylacI = data['ylacI']
    var ytetR = data['ytetR']
    var ylambda = data['ylambda']
    var mlacI = Array(Span).fill(0)
    var mtetR = Array(Span).fill(0)
    var mlambda = Array(Span).fill(0)
    

    for (var i = 0; i < 10000; i++)
    {
        if (i == 0)
        {
            CmlacI = CmlacIO
            CmtetR = CmtetRO
            Cmlambda = CmlambdaO
            CplacI = CplacIO
            CptetR = CptetRO
            Cplambda = CplambdaO
        }
        else
        {
            CmlacI = mlacI[i-1] + alphaO*dt - mlacI[i-1]*dt + alpha*dt/(1+Math.pow(ylambda[i-1],n))
            CplacI = ylacI[i-1] - ylacI[i-1]*dt*beta + beta*mlacI[i-1]*dt
            CmtetR = mtetR[i-1] + alphaO*dt - mtetR[i-1]*dt + alpha*dt/(1+Math.pow(ylacI[i-1],n))
            CptetR = ytetR[i-1] - ytetR[i-1]*dt*beta + beta*mtetR[i-1]*dt
            Cmlambda = mlambda[i-1] + alphaO*dt - mlambda[i-1]*dt + alpha*dt/(1+Math.pow(ytetR[i-1],n))
            Cplambda = ylambda[i-1] - ylambda[i-1]*dt*beta + beta*mlambda[i-1]*dt
        }
        mlacI[i] = CmlacI
        mtetR[i] = CmtetR
        mlambda[i] = Cmlambda
        ylacI[i] = CplacI
        ytetR[i] = CptetR
        ylambda[i] = Cplambda
    }
    source.change.emit();
""")

#Textboxes
Ibeta = TextInput(value=str(beta))
callback.args["beta"] = Ibeta
Tbeta = PreText(text = "beta - default value is " + str(beta))
IalphaO = TextInput(value=str(alphaO))
callback.args["alphaO"] = IalphaO
TalphaO = PreText(text = "alphaO - default value is " + str(alphaO))
Ialpha = TextInput(value=str(alpha))
callback.args["alpha"] = Ialpha
Talpha = PreText(text = "alpha - default value is " + str(alpha))
ICmlacIO = TextInput(value=str(CmlacIO))
callback.args["CmlacIO"] = ICmlacIO
TCmlacIO = PreText(text = "CmlacIO - default value is " + str(CmlacIO))
ICmtetRO = TextInput(value=str(CmtetRO))
callback.args["CmtetRO"] = ICmtetRO
TCmtetRO = PreText(text = "CmtetRO - default value is " + str(CmtetRO))
ICmlambdaO = TextInput(value=str(CmlambdaO))
callback.args["CmlambdaO"] = ICmlambdaO
TCmlambdaO = PreText(text = "CmlambdaO - default value is " + str(CmlambdaO))
ICplacIO = TextInput(value=str(CplacIO))
callback.args["CplacIO"] = ICplacIO
TCplacIO = PreText(text = "CplacIO - default value is " + str(CplacIO))
ICptetRO = TextInput(value=str(CptetRO))
callback.args["CptetRO"] = ICptetRO
TCptetRO = PreText(text = "CptetRO - default value is " + str(CptetRO))
ICplambdaO = TextInput(value=str(CplambdaO))
callback.args["CplambdaO"] = ICplambdaO
TCplambdaO = PreText(text = "CplambdaO - default value is " + str(CplambdaO))


#Callback triggers
Ibeta.js_on_change('value', callback)
IalphaO.js_on_change('value', callback)
Ialpha.js_on_change('value', callback)
ICmlacIO.js_on_change('value', callback)
ICmtetRO.js_on_change('value', callback)
ICmlambdaO.js_on_change('value', callback)
ICplacIO.js_on_change('value', callback)
ICptetRO.js_on_change('value', callback)
ICplambdaO.js_on_change('value', callback)


#Plots
fig.circle('x','ylacI', source=source, size = 1, color = 'blue', legend_label="lacI")
fig.circle('x','ytetR', source=source, size = 1, color = 'green', legend_label="tetR")
fig.circle('x','ylambda', source=source, size = 1, color = 'red', legend_label="lambda")

#Legend settings
fig.legend.location = "top_left"

show(row(fig,column(Ibeta,Tbeta,IalphaO,TalphaO,Ialpha,Talpha,ICmlacIO,TCmlacIO,ICmtetRO,TCmtetRO,ICmlambdaO,TCmlambdaO,ICplacIO,TCplacIO,ICptetRO,TCptetRO,ICplambdaO,TCplambdaO)))
