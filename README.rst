====
MSDP
====

MSDP team ID: 15
MSDP team members: Emmanouil Chondrakis, Shane Bird, Dan Zhu, Peng Ye

Description
===========

This project is to provide a friendly Web Application UI for end-user to estimate Dublin Bus Dynamic Travel
Time in convenience. The candidate solution for the term project of COMP47360.

The major trained model in this web application is Artificial Neural Network based Linear Regression (ANN-MLP),
which can predict a bus travel time from Station A to Station B, considerring about Weather condition and Time
intervale in a working day as well.
The secondary algorithm implemented in this Web Application is Double-Lines Algorithm, which is calculating and
providing an alternative solution of multiple lines linking A and B if they are not in the same bus line.

Prerequisites
----------------------

1. Python 3.6
This project was created in a Python 3.6 environment. It will be easier to set up the project if
you install [Anaconda](https://conda.io/docs/user-guide/install/download.html) or [Miniconda]
(https://conda.io/miniconda.html). Other options, such as [PyEnv](https://github.com/pyenv/pyenv)
and classic virtual environment (i.e. `venv`), will also work.

2. Mysql 5.7.23 and MySQL Library
Both Server and Clinet need to be installed in advance before deploying other components
MySQLdb Library also needs to be installed before opening Data Analytics Page

3. Data Science Libraries
panda, numpy in necessary to be installed before running web appliction

4. Django 2.0.6
Install Django 2.0.6 or later version

NOTE: The current live System is Ubuntu (4.4.0-130-generic), which is the only version of Linux that has been tested.
      The Web Appliction does not guarantee to be run successfully in any other Linux/Unix System.

Installation and Setup and Running the Program
----------------------
1. Boot up Mysql Server
# sudo service mysql start

2. Boot up Django Server
# python3 src/msdp/run.py start

3. Stop Django Server
# python3 src/msdp/run.py stop

Access the web application and general instructions for query a bus travel time 
----------------------
1. Access the first page
http://137.43.49.51:8000/dublinbus/

2. Access the second page (Data Analytics)
http://137.43.49.51:8000/accounts/login/

or

Click "Data Analytics" on the top right of first page

3. How to query a bus travel time
  1) Open the first page
  2) Input the values on input boxes of 'Start','Destination','Date' and 'Time' and click Submit
  3) If the IDs of Start and Destination are in the same bus line, there will be one or more than one candidate bus
     lines displayed on the right of the page. Click 'Show' buttom on the displayed bus line, the route will be showed
     on the left google map
  4) If the IDs of Start and Destination are NOT in the same bus line, "No direct bus route" will be displayed on the
     right of page. Click "Try Transfer" will be able to get the replace Double-Line route as the alternative solution.
     This could take a little long time if it calculate with such IDs for the first time.

4. How to use Data Analytics Page
  1) Click "Data Analytics" on the top-rightof the first page to open login page
  2) Input username: MSDP
     Input password: MSDPUCD123
     Click 'Login' to enter the secured page
  3) After entered data analytics page, select Bus Line, Months and Time interval to get a list of related TripIDs
  4) Click one TripID Icon will display a group of charts of data related to this TripID. This will take 2~5 mins
     for loading the data from MySQL Server


Note
====

This project has been set up using PyScaffold 3.0.1. For details and usage
information on PyScaffold see http://pyscaffold.org/.
