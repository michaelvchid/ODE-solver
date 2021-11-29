from flask import Flask, render_template, g, request, flash
from py.ODEs import solve_ODE, is_num, Euler, Heun, RungeKutta4th
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
	if (request.method == "POST"):
		order = request.form["order"]
		initials = request.form["initials"]
		ode = request.form["ode"]
		ti = request.form["ti"]
		tf = request.form["tf"]
		error = False

		if(order.isnumeric() == False):
			error = True
			flash("Please enter a positive integer order.")

		if(order.isnumeric() and len(initials.split(",")) != int(order)):
			error = True
			flash(f"Please enter {order} initial conditions.")

		for init in initials.split(","):
			if(is_num(init) == False):
				error = True
				flash(f"Please enter numerical values for initial conditions.")
				break

		if(is_num(ti) == False or is_num(tf) == False):
			error = True
			flash("Please enter numerical start/end times.")

		if(error == False):
			# instead of checking whether or not the inputted function was valid,
			# we use try/except. If the given function was invalid, then
			# solve_ODE() will throw an error
			try:
				_,_, fig = solve_ODE(order, initials, ode, ti,tf)
				# Used to show the plotly graph on the webpage 
				graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
			except:
				error = True
				flash("Please enter a valid equation for your differential equation.")

		# final check to see if we can create a valid plot
		if(error == False):
			return render_template("base.html", page="home", graphJSON=graphJSON)
		else: 
			return render_template("base.html", page="home")
		
	else: # GET method
		flash("Please enter the info for the differential equation you want to solve.")
		return render_template("base.html", page="home")






# Creates page that lets users approximate solutions with methods
@app.route("/methods", methods=["POST", "GET"])
def methods():
	# If the page is loaded after submitting a message:
	if request.method == "POST":
		initial = request.form["initial_euler"]
		f = request.form["f_euler"]
		step = request.form["step_euler"]
		tf = request.form["tf_euler"]

		error = False

		if(is_num(initial) == False):
			error = True
			flash(f"Please enter numerical value for initial condition.")

		if(is_num(tf) == False):
			error = True
			flash("Please enter numerical end time.")

		if(is_num(step) == False):
			error = True
			flash("Please enter numerical step value.")

		fig = 0
		if(error == False):
			# instead of checking whether or not the inputted function was valid,
			# we use try/except. If the given function was invalid, then
			# solve_ODE() will throw an error
			try:

				t1, y1, fig1 = solve_ODE("1", initial, f, "0", tf)
				fig=px.scatter(x=t1, y=y1, title="Approximating the Solution of dy/dt = f(t,y)")
				fig.update_traces(mode="lines", showlegend=True, name="Solution", line={"color":px.colors.qualitative.Plotly[0]})
			except:
				error = True
				flash("Please enter a valid equation for your differential equation.")

		# final check to see if we can create a valid plot and add all num. methods
		if(error == False):
			if(request.form.get("euler")):
				t2 ,y2, fig2 = Euler(f, initial, step, tf)
				fig.add_scatter(x=t2, y=y2,mode='markers+lines', name="Euler's Method", line={"color":px.colors.qualitative.Plotly[1]})
			if(request.form.get("heun")):
				t3 ,y3, fig3 = Heun(f, initial, step, tf)
				fig.add_scatter(x=t3, y=y3,mode='markers+lines', name="Heun's Method", line={"color":px.colors.qualitative.Plotly[2]})
			if(request.form.get("rungekutta")):
				t4 ,y4, fig4 = RungeKutta4th(f, initial, step, tf)
				fig.add_scatter(x=t4, y=y4,mode='markers+lines', name="Runge-Kutta 4th Order Method", line={"color":px.colors.qualitative.Plotly[3]})
			graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
			return render_template("methods.html", page="methods", graphJSON=graphJSON)
		else:
			return render_template("methods.html", page="methods")


	else: #GET method
		flash("Please enter the info for the differential equation you want to approximate.")
		return render_template("methods.html", page="methods")




