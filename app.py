from flask import Flask, render_template, g, request
from ODEs import solve_ODE2
import json
import plotly
import sqlite3

# Creates app with file name
app = Flask(__name__)

# Creates a home page
@app.route("/", methods=["POST","GET"])
def main():
	if (request.method == "POST"):
		order = request.form["order"]
		initials = request.form["initials"]
		ode = request.form["ode"]
		ti = request.form["ti"]
		tf = request.form["tf"]

		_,_, fig = solve_ODE2(order, initials, ode, ti,tf)
		graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
		return render_template("base.html", page="home", graphJSON=graphJSON)
		
	else:
		return render_template("base.html", page="home")






# Creates page that lets users submit messages
@app.route("/submit", methods=["POST", "GET"])
def submit():
	# If the page is loaded after submitting a message:
	if request.method == "POST":
		msg = insert_message(request)
		return render_template("submit.html",
			message = msg[0],
			handle = msg[1])

	# If we're just viewing the page and didn't submit a form
	else: # request.method == "GET"
		return render_template("submit.html")

