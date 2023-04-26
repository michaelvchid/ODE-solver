# Project Proposal
In this (solo) group, Michael Chidbachian will create a web app that helps visualize solutions to differential equations. 

## Abstract
Solving and visualizing differential equations (DEs) and their solutions can be a difficult task. Changing different parameters of the equation(s) can have changes that may be hard to visualize. With an interactive web app, anyone will be able to easily give a DE and have it solved both quantitatively and graphically, with the capability of altering variables to see how the solution changes. Visualizing different numerical methods to solve DEs and manipulating different factors will enable the user to understand how each paramater changes the system and solution. 


## Planned Deliverables
The main goal of this project is to create a webapp that can solve DEs and graph their solutions, with a main part being that it is interactive. This would mean that the user would be able to change coefficients and initial conditions and, in real time, see how they change the solution graphically. The second part would be to approximate solutions using different numerical methods (for example, Euler's method or Huen's method) with the ability to change initial conditions and step sizes and graphically see how it changes the solution.

If everything works out perfectly, then all of the above would work flawlessly on a beautifully-designed and organized webapp. Ideally, it would be able to take in a wide variety of DEs, such as ordinary and partial differential equations, linear ODEs, and more. Changing parameters, especially for the numerical methods, should have fast response times and not take a long time to produce a visually appealing graph. 

Now, if things don't go as planned, then a few things can happen. If the webapp portion of the project isn't coming together, then worst comes to worst and the project would have to work on a Jupyter notebook. If the math part of the project is where trouble arises, then certain features would have to be cut. This may mean the solver can only handle a strict class of DEs or can only do approximations. 

## Resources Required
One thing this project will NOT need is data. Due to the nature of what is being accomplished, no data will be needed from the internet. However, what will be needed is mathematical knowledge on solving/approximating solutions to DEs; knowing different techniques and tricks can greatly improve both the accuracy as well as the speed of the program. 

Though the internet is a great source for math guidance, "Differential Equations with Applications and Historical Notes" by George F. Simmons is one of many resources on differential equations. This project may also need lots of computing power; getting a higher degree of accuracy means more power must be used, and the two must be balanced out. 

## Tools and Skills Required
One of the neccessary skills needed for this project is to create a webapp. This will be accomplished using the same tools that will be taught during week 4 of the PIC 16B course. With three lectures and two web development labs, there will be plenty of information to get this webapp up and running. 

Another tool will be needed to solve differential equations as well as make graphs with interactive sliders. Some of the packages that can and will be used are `matplotlib.pyplot` as well as `odeint` from `scipy.integrate` and other packages from `scipy`. Though this should be able to get quite a bit done, more resources may be needed to accomplish what is desired. 


## What You Will Learn
By the end of this project, I'll have learned quite a bit on webapps and making them interactive. I feel as though this would be a great resource to have under one's belt as it makes it extremely easy for others to view a project: all they have to do is go to the link and that's it! No downloading files or seeing code as one would see in a Jupyter notebook. 

I would also learn a lot more features from `pyplot` and how to make visually appealing graphs. This will be quite handy as data analysis and visualization is by far one of the most important skills to have in STEM-related fields. Lastly, I will get used to `scipy` and understanding what the package can offer.

## Risks
One major risk that I can encounter is that this project won't solve a large enough variety of differential equations. Some classes of DEs may be too difficult to implement and take far too much computing power than what is available, or it may take too much time and take away from the user's experience on the webapp. Another possible risk is that I won't be able to get everything to run properly on a webapp. This portion of the project must be done as soon as possible to avoid having a poor user interface. 

## Ethics
One amazing aspect of this project is that, if it is correctly implemented and all the math is accurate, then there really aren't any harmful impacts it can have on people. This project focuses on a very specific topic and will mainly help people studying mathematics or are doing work that relates to differential equations. Since this is designed for people learning the subject rather than experts who are using this for their job, there can be very little impact provided by this project. 

Of course, this all relies on the assumption that the math is accurate and that the webapp works really well; if the first doesn't happen, then this could sabotage people and hurt their knowledge in the subject. If the second doesn't happen, then it won't be used and won't have any impact on people. 

## Tentative Timeline
By the two-week checkpoint, I aim to have the webapp up and running. By the fourth week, I should have the math portion completed; this will most likely be in a Jupyter notebook as it is the math/visualizations that are very important to get down first. By the sixth week, I hope to have a large portion of the math on the webapp. Depending on how difficult it is to implement everything, the sliders for interactivity may or may not be included in this check up. By the end of the quarter, everything will be ready. 
