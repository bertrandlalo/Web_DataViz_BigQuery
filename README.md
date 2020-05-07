#  Web Data Visualization with Flask, Chart.JS, Vue.JS, Ajax and Big Query

This is a toy/POC project, to take some framework in hands.
The goal is to draw some custom graphs from big database.

The specifications are the following :
- Data should come from a BigQuery dataset</li>
- For security purpose, the query job should belong to server
    (use AJAX to make client and server communicate)
- Client should be able to apply selection filters (ie. WHERE)
    to the data from a control pane
- Client should be able to choose which variable to plot on the chart</li>
- Client should be able to custom the properties of the chart (title, label ...)</li>
- Client should be able to save the chart parameters and re-load it later on</li>
 

## Get started
### Preparation

#### Gcloud
Create account ... 

This is meant to work on Python , but I need to check for Python 2 (@Pap)

#### Virtual env
In a terminal : 
```console
python3 -m venv flask-charts-venv
source flask-charts-venv/bin/activate
pip install -r requirements 
```

### Usage 
#### 1. GCloud authentification
```console
gcloud auth login your@email.com
gcloud auth application-default login
```
#### 2. Activate venv and launch app 
```console
source xq-bi-venv/bin/activate
python app.py
```
Then visit http://127.0.0.1:5000/

## Demo 

### Hello Chart.JS
This app aims at exploring Chart.JS functionalities on generated random data. 
The user can choose the kind of graph (bar, pie, doughnuts, polar)
 and the number of dataset to draw (he can choose to add, remove and randomize the data).  

![](static/gif/hello_chartJS.gif)

### Hello Big Query 
This app uses Vue.JS to handle the client selections, sends a request to python 
flask server (through Ajax), that calls Big Query to gather data, and sends them 
back to the client where Chart.JS draws a bar chart with the chosen datasets filters
 (which data to select ? ) and aggregators (which variable for X, Y axis ? ).  
![](static/gif/hello_BigQuery1.gif)

## Libraries 
### Flask 
[Flask](https://flask.palletsprojects.com/en/1.1.x)
is a minimalistic python framework for building web apps. It provides one
with tools, libraries and technologies that allow to build a web application.
**I chose to use Flask framework for simplicity purpose**. 

### Chart.JS
[Chart.JS](https://chartjs.org) is a popular open source library to
plot data in web applications.
It is highly customizable, but configuring all of its options remains
a challenge ! Hence, I started to explore it from a simple
example where I ploted random data and then built upon it to real data.
**I chose to use Chart.JS framework for
its clean design and versatility.**

### Vue.JS
[Vue.JS](https://vuejs.org) is a recent javascript framework claiming to be approchable,
versatile and performant.
It is basically a way of hacking HTML DOM, by watching variables, updating states
accordingly without big effort.
**I wanted to try it here to handle client selection from control panel
(see page on BigQuery**

### Big Query
    
[Big Query](https://cloud.google.com/bigquery?hl=en))
is a fully-managed, serverless data warehouse that enables scalable,
cost-effective and fast analysis over petabytes of data.
It is a serverless Software as a Service (SaaS) that supports
querying using ANSI SQL.
**I wanted to try it here to use available public datasets
-for now, it's one of my own dataset (see page on BigQuery) -**.




