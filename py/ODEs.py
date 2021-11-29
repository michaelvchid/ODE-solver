#!/usr/bin/env python
# coding: utf-8

from scipy.integrate import odeint
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from plotly import express as px


def replace_y(string):
    """
    Input : string
    Output: string
    
    Transforms all "y''''" in a string to "y[4]",
    where the number of apostraphe's after "y" 
    is the number in brackets. If none exists, ie
    the "y" has no apostraphe, it is "y[0]".
    Needed for handling user input and converting
    it to a scipy.odeint-friendly format.
    """
    if(len(string)==0):
        return ""
    
    index = string.find('y')
    count = 0
    
    # will end once we finish the string since find returns -1 if not found
    if(index>=0):
        new_string = string[0:index]
        # count ' directly after a "y"
        for char in string[index+1:]:
            if(char=="'"):
                count += 1
            else:
                break
        
        concat = f"y[{count}]"
        new_string = new_string + concat + replace_y(string[index+count+1:])
    
    # no "y" left in string
    else:
        new_string = string
    return new_string


def manip_expression(string):
    """
    Input : string (mathematical expression)
    Output: string (mathematical expression)
    
    Takes in a math expression and returns it, with 
    all math words (like sin, cos, pi) turned into
    their useful numpy function/constant.
    """
    
    string = string.replace("^","**")
    string = string.replace("sin","np.sin")
    string = string.replace("cos", "np.cos")
    string = string.replace("tan", "np.tan")
    string = string.replace("arcsin","np.arcsin")
    string = string.replace("arccos", "np.arccos")
    string = string.replace("arctan", "np.arctan")
    string = string.replace("e", "np.e")
    string = string.replace("pi", "np.pi")
    string = string.replace("exp", "np.exp")
    string = string.replace("log", "np.log")
    string = string.replace("ln", "np.log")
    string = string.replace("sqrt", "np.sqrt")

    return string

def is_num(string):
    """
    Input: string (mathematical expression)
    Output: bool
    
    Takes in an expression and determines if it is a number.
    """
    # must use try/except. If string isn't valid, eval throws and EOF parsing error.
    try:
        if(type(eval(manip_expression(string))) == int or
          type(eval(manip_expression(string))) == float):
            return True
        else:
            return False
    except:
        return False



def solve_ODE(order, initials, ode, ti, tf):
    """
    Inputs: string
    Outputs: np array, np array, px figure
    Uses scipy.odeint to solve the differential equation ode
    of order 'order', initial conditions 'initials', and
    starting and end times ti, tf
    """
    # ask for inputs
    n = int(order)
    y0_raw = initials
    
    # split up initial conditions into an array
    y0 = y0_raw.split(",")
    # make y0 elements into numbers
    for num in range(len(y0)):
        y0[num] = eval(manip_expression(y0[num]))
    
    # ask for the ODE
    dydtn = ode

    t0 = float(ti)
    t1 = float(tf)
    
    # defines our model
    def model(y,t):
        dydt = []
        for i in range(n-1):
            dydt.append(y[i+1])
        dydt.append(eval(replace_y(manip_expression(dydtn))))
        #dydt.append(eval(manip_expression(dydtn, True)))
        return dydt          
    
    # create solution
    t = np.linspace(t0,t1,2000)
    sol = odeint(model, y0, t)[:,0]
    
    fig = px.line(x=t, y=sol ,title="Solution y(t) of the ODE", width=800, height=500)
    #fig.update_layout({
    #"plot_bgcolor":"rgba(85,100,125,0.4)",
    #"paper_bgcolor":"rgba(255,255,255,1)"
    #})
    return t, sol, fig


def Euler(f, y0, step, t1):
    """
    Input: f   : string (dy/dt = f)
    Input: y0  : string initial value
    Input: step: string step size
    Input: t1  : string final view time
    Output: t,y array of time and solution
    """
    f_new = lambda y,t : eval(manip_expression(f))
    y0_new = eval(manip_expression(y0))
    step_new = eval(manip_expression(step))
    t1_new = eval(manip_expression(t1))
    t = np.linspace(0, t1_new, int((t1_new)/step_new+1), endpoint=True)
    y = np.zeros(len(t))
    y[0] = y0_new
    for n in range(0, len(t)-1):
        y[n+1] = y[n]+f_new(y[n],step_new * n) * step_new
    
    fig = px.line(x=t, y=y,title="Approximation With Euler's Method", width=800, height=500)
    #fig.update_layout({
    #"plot_bgcolor":"rgba(85,100,125,0.4)",
    #"paper_bgcolor":"rgba(255,255,255,1)"
    #})
    return t, y, fig


def Heun(f, y0, step, t1):
    """
    Input: f   : string (dy/dt = f)
    Input: y0  : string initial value
    Input: step: string step size
    Input: t1  : string final view time
    Output: t,y array of time and solution
    """
    f_new = lambda y,t : eval(manip_expression(f))
    y0_new = eval(manip_expression(y0))
    step_new = eval(manip_expression(step))
    t1_new = eval(manip_expression(t1))
    t = np.linspace(0, t1_new, int((t1_new)/step_new+1), endpoint=True)
    y = np.zeros(len(t))
    y_est = np.zeros(len(t))
    
    y[0] = y0_new
    #y_est[0]=y0_new
    for n in range(0, len(t)-1):
        y_est[n+1] = y[n]+f_new(y[n],step_new * n) * step_new
        y[n+1]     = y[n]+1/2*(f_new(y[n],step_new * n)+f_new(y_est[n+1],step_new * (n+1))) * step_new
                               
    fig = px.line(x=t, y=y,title="Approximation With Euler's Method", width=800, height=500)
    #fig.update_layout({
    #"plot_bgcolor":"rgba(85,100,125,0.4)",
    #"paper_bgcolor":"rgba(255,255,255,1)"
    #})
    return t, y, fig


def RungeKutta4th(f, y0, step, t1):
    """
    Input: f   : string (dy/dt = f)
    Input: y0  : string initial value
    Input: step: string step size
    Input: t1  : string final view time
    Output: t,y array of time and solution
    """
    f_new = lambda y,t : eval(manip_expression(f))
    y0_new = eval(manip_expression(y0))
    step_new = eval(manip_expression(step))
    t1_new = eval(manip_expression(t1))
    t = np.linspace(0, t1_new, int((t1_new)/step_new+1), endpoint=True)
    y = np.zeros(len(t))
    
    k1 = np.zeros(len(t))
    k2 = np.zeros(len(t))
    k3 = np.zeros(len(t))
    k4 = np.zeros(len(t))
    
    y[0] = y0_new
    for n in range(0, len(t)-1):
        k1[n] = f_new(y[n],              step_new * n        ) * step_new
        k2[n] = f_new(y[n] + 1/2 * k1[n],step_new * (n + 1/2)) * step_new
        k3[n] = f_new(y[n] + 1/2 * k2[n],step_new * (n + 1/2)) * step_new
        k4[n] = f_new(y[n] +   1 * k3[n],step_new * (n + 1  )) * step_new
        
        y[n+1] = y[n] + 1/6 *(k1[n]+2*k2[n]+2*k3[n]+k4[n])
                               
    fig = px.line(x=t, y=y,title="Approximation With Euler's Method", width=800, height=500)
    #fig.update_layout({
    #"plot_bgcolor":"rgba(85,100,125,0.4)",
    #"paper_bgcolor":"rgba(255,255,255,1)"
    #})
    return t, y, fig


