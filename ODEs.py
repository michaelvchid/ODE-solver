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
    string = replace_y(string)

    return string


def solve_ODE():
    # ask for inputs
    n = int(input("What is the order of your differential equation?"))
    y0_raw = input("What are your initial conditions y(0), y'(0),... separated by commas")
    
    # split up initial conditions into an array
    y0 = y0_raw.split(",")
    # make y0 elements into numbers
    for num in range(len(y0)):
        y0[num] = eval(manip_expression(y0[num]))
    
    # ask for the ODE
    dydtn = input(f"What is d^{n}y/dt^{n} = ")
    # get time interval and turn into floats
    t_raw = input("What time interval do you want to view? Format as t1:t2")
    t0 = float(t_raw.split(":")[0])
    t1 = float(t_raw.split(":")[1])
    
    # defines our model
    def model(y,t):
        dydt = []
        for i in range(n-1):
            dydt.append(y[i+1])
        dydt.append(eval(manip_expression(dydtn)))
        return dydt          
    
    # create solution
    t = np.linspace(t0,t1,1000)
    sol = odeint(model, y0, t)[:,0]
    
    # plot the solution
    fig = plt.plot(t, sol)
    plt.xlabel("t", fontsize=12)
    plt.ylabel("y(t)", fontsize=12)
    plt.title("Solution y(t) of the ODE")
    plt.grid()
    return sol, t, fig


def solve_ODE2(order, initials, ode, ti, tf):
    """
    Same as solve_ODE(), but has function inputs
    instead of run-time user inputs
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
        dydt.append(eval(manip_expression(dydtn)))
        return dydt          
    
    # create solution
    t = np.linspace(t0,t1,2000)
    sol = odeint(model, y0, t)[:,0]
    
    # # plot the solution
    # fig = plt.plot(t, sol)
    # plt.xlabel("t", fontsize=12)
    # plt.ylabel("y(t)", fontsize=12)
    # plt.title("Solution y(t) of the ODE")
    # plt.grid()
    
    df = pd.DataFrame({"t":t, "y(t)":sol})
    fig = px.line(df, x="t", y="y(t)",title="Solution y(t) of the ODE", width=800, height=500)
    fig.update_layout({
    "plot_bgcolor":"rgba(85,100,125,0.4)",
    "paper_bgcolor":"rgba(255,255,255,1)"
})
    return sol, t, fig


# _,_, fig2 = solve_ODE2("2", "1,1", "-y-y'", "0","10")



# fig2.show()


# ## Testing

# sol, t = solve_ODE()




# df = pd.DataFrame({"t":t, "y(t)":sol})
# fig = px.line(df, x="t", y="y(t)",title="Solution y(t) of the ODE", width=800, height=500)
# fig


# fig.show()



