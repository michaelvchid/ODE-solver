from flask import Flask, render_template, g, request, flash
from py.ODEs import solve_ODE, is_num, is_positive, Euler, Heun, RungeKutta4th
import json
import plotly
from plotly import express as px
import sqlite3

# Creates app with file name
app = Flask(__name__)
app.secret_key = "thisIsSomeRandomStringForTheSession"

# Creates a home page
@app.route("/", methods=["POST","GET"])
def main():
	#get all the inputted info from form if they submitted form:
	if (request.method == "POST"):
		order = request.form["order"] #order of ODE
		initials = request.form["initials"] # initial conditions
		ode = request.form["ode"] # the differential equation that was inputted by the user
		tf = request.form["tf"] # final view time 

		# perform error check to make sure inputs are clean and won't raise errors in python
		error = error_check_main(order, initials, ode, tf)

		if(error == False):
			# instead of checking whether or not the inputted function was valid,
			# we use try/except. If the given function was invalid, then
			# solve_ODE() will throw an error
			try:
				# get figure from solution
				_,_, fig = solve_ODE(order, initials, ode, "0",tf)
				# Change size of graph and use JSON to prepare the graph to be displayed on webapp
				fig.update_layout(width=900, height=500)
				graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
			except:
				# if solve_ODE threw an error, then the equation was invalid
				error = True
				flash("Please enter a valid equation for your differential equation.")

		# checks to see if we created a valid plot, and if so, send it with render_template
		if(error == False):
			return render_template("base.html", page="home", graphJSON=graphJSON)
		else: 
			return render_template("base.html", page="home")
		
	else: # GET method
		return render_template("base.html", page="home")





# Creates page that lets users approximate solutions with methods
@app.route("/methods", methods=["POST", "GET"])
def methods():
	# If the page is loaded after submitting a message:
	if (request.method == "POST"):
		initial = request.form["initial_euler"] # initial conditions
		f = request.form["f_euler"] # inputted function
		step = request.form["step_euler"] # inputted step size
		tf = request.form["tf_euler"] # inputted final view time

		error = error_check_methods(initial, step, tf)

		if(error == False):
			# instead of checking whether or not the inputted function was valid,
			# we use try/except. If the given function was invalid, then
			# solve_ODE() will throw an error
			try:
				# create figure of actual solution that will always be shown
				t1, y1, fig1 = solve_ODE("1", initial, f, "0", tf)
				fig=px.scatter(x=t1, y=y1, title="Approximating the Solution of dy/dt = f(t,y)")

				# change layout so only lines show, with the name "solution", and the color of the line
				# is the default first color Plotly always assigns. Doing this will ensure the color
				# of each line is the same, whether or not the following methods are chosen.
				fig.update_traces(mode="lines", showlegend=True, name="Solution", line={"color":px.colors.qualitative.Plotly[0]})
			
			except:
				# bad ODE inputted
				error = True
				flash("Please enter a valid equation for your differential equation.")

		# if we created a valid solution, then create the selected numerical method graphs too
		if(error == False):

			# create a plot for each of the selected numerical methods:
			if(request.form.get("euler")): # if the "euler" box was selected:
				t2 ,y2, fig2 = Euler(f, initial, step, tf)
				fig.add_scatter(x=t2, y=y2,mode='markers+lines', name="Euler's Method", line={"color":px.colors.qualitative.Plotly[1]})

			if(request.form.get("heun")): # if "heun" box was selected:
				t3 ,y3, fig3 = Heun(f, initial, step, tf)
				fig.add_scatter(x=t3, y=y3,mode='markers+lines', name="Heun's Method", line={"color":px.colors.qualitative.Plotly[2]})

			if(request.form.get("rungekutta")): # if the "rungekutta" box was selected:
				t4 ,y4, fig4 = RungeKutta4th(f, initial, step, tf)
				fig.add_scatter(x=t4, y=y4,mode='markers+lines', name="Runge-Kutta 4th Order Method", line={"color":px.colors.qualitative.Plotly[3]})

			# update graph size and use JSON to prepare it for the website
			fig.update_layout(width=900, height=500)
			graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
			# render the methods page
			return render_template("methods.html", page="methods", graphJSON=graphJSON)
		else:
			return render_template("methods.html", page="methods")


	else: #GET method
		return render_template("methods.html", page="methods")




@app.route("/about", methods=["GET"])
def about():

	return render_template("about.html")



def error_check_main(order, initials, ode, tf):
	"""
	Inputs: strings from submitted form on main page
	Output: returns whether an error occurred in analyzing the inputs
	"""
	# perform error check to make sure inputs are clean and won't raise errors in python
	error = False

	#if inputted order is not a valid number 
	if(order.isnumeric() == False):
		error = True
		flash("Please enter a positive integer order.")

	# checks if the order matches the number of initial conditions given
	if(order.isnumeric() and len(initials.split(",")) != int(order)):
		error = True
		flash(f"Please enter {order} initial conditions.")

	# makes sure all initial conditions are valid numbers
	for init in initials.split(","):
		if(is_num(init) == False):
			error = True
			flash(f"Please enter numerical values for initial conditions.")
			break

	# makes sure final view time is a valid number
	if(is_num(tf) == False):
		error = True
		flash("Please enter numerical start/end times.")

	return error


def error_check_methods(initial, step, tf):

	error = False

	if(is_num(initial) == False):
		error = True
		flash(f"Please enter numerical value for initial condition.")

	if(is_num(step) == False):
		error = True
		flash("Please enter numerical step size.")
	elif (is_positive(step) == False):
		error = True
		flash("Please enter a positive step size.")

	if(is_num(tf) == False):
		error = True
		flash("Please enter numerical end time.")
	elif (is_positive(tf) == False):
		error = True
		flash("Please enter a positive end time.")

	return error