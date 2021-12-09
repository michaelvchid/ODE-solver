# About
This project aims to create a webapp that allows users to find a graphical solution to a wide array of differential equations. The first main functionality of the webapp works with ODEs of the form d^ny/dt^n = f(t,y,y',...,y^{n-1}). The second portion of the webapp provides an interface that allows the user to input an ODE in the form of dy/dt = f(t,y) and lets them select from multiple numerical methods to view how such methods' solutions are different from the true solution, as well as analyze how well each method compares to the others. 

## Setup
The following guide will provide instructions on how to reproduce this webapp on your own machine. The webapp was created with tools that may be Windows-specific. For this reason, there may be slight differences when following these instructions on Linux or Mac. Note that this setup process makes use of the Anaconda Prompt for Python as well as Flask, a tool used to create webapps. Other necessary packages include `plotly`, `express` from Plotly, `sqlite3`, `json`, `scipy`, `numpy`, `pandas`, and `pyplot` from matplotlib.

First, head to the repository on GitHub at https://github.com/michaelvchid/PIC16B-Project (if you're viewing this on GitHub, you're most definitely on the correct page already). Next, look for the green button with the word "Code", and click it to bring a dropdown menu. Then, click download ZIP. 

Once this is downloaded, unzip the folder and send the extracted folder to somewhere memorable or where you would like to store the project. 

Next, open up the Anaconda Prompt and `cd` into the directory of the downloaded folder so that the current directory contains files such as app.py, proposal.md and README.md. Your working directory should appear something like "...\Downloads\PIC16B-Project-main\PIC16B-Project-main". 

Now that you are currently in the proper directory, enter on Anaconda Prompt `set FLASK_ENV=development`. The console shouldn't print anything out. 

Lastly, enter `flask run`. After loading everything, the console will print out `Running on http://127.0.0.1:5000/`, or have a different address. Copy the address and past it into your favorite web browser. Then, you should be able to view the webapp and interact with it!