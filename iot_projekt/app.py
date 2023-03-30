from datetime import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('PH_DB.db', check_same_thread=False)
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM PH_SENSOR ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		PHVALUE = row[1]
		GRADER = row[2]
	#conn.close()
	return time, PHVALUE, GRADER

# Get 'x' samples of historical data
def getHistData (numSamples):
	curs.execute("SELECT * FROM PH_SENSOR ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	PHVALUES = []
	GRADERS = []
	for row in reversed(data):
		dates.append(row[0])
		PHVALUES.append(row[1])
		GRADERS.append(row[2])
		PHVALUES, GRADERS = Data(PHVALUES, GRADERS)
	return dates, PHVALUES, GRADERS

# Test data for cleanning possible "out of range" values
def Data(PHVALUES, GRADERS):
	n = len(PHVALUES)
	for i in range(0, n-1):
		if (PHVALUES[i] < -10 or PHVALUES[i] >50):
			PHVALUES[i] = PHVALUES[i-2]
		if (GRADERS[i] < 0 or GRADERS[i] >100):
			GRADERS[i] = PHVALUES[i-2]
	return PHVALUES, GRADERS


# Get Max number of rows (table size)
def maxRowsTable():
	for row in curs.execute("SELECT COUNT(PHVALUE) from  PH_SENSOR"):  #COUNT = COLUMN NAME
		maxNumberRows=row[0]
	return maxNumberRows

# Get sample frequency in minutes
def freqSample():
	times, PHVALUES, GRADERS = getHistData (2)
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp0 = datetime.strptime(times[0], fmt)
	tstamp1 = datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
        numSamples = 100

global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 100
				
		
# main route 
@app.route("/")
def index():
	time, PHVALUE, GRADER = getLastData()
	templateData = {
	  'time'		: time,
      'PHVALUE'		: PHVALUE,
      'GRADER'		: GRADER,
      'freq'		: freqSamples,
      'rangeTime'		: rangeTime
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples 
    global freqSamples
    global rangeTime
    rangeTime = int (request.form['rangeTime'])
    if (rangeTime < freqSamples):
        rangeTime = freqSamples + 1
    numSamples = rangeTime//freqSamples
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    time, PHVALUE, GRADER = getLastData()
    
    templateData = {
	  'time'		: time,
      'PHVALUE'		: PHVALUE,
      'GRADER'		: GRADER,
      'freq'		: freqSamples,
      'rangeTime'	: rangeTime
	}
    return render_template('index.html', **templateData)
	
	
@app.route('/plot/PHVALUE')
def plot_PHVALUE():
	times, PHVALUES, GRADERS = getHistData(numSamples)
	ys = PHVALUES
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("PHVALUES")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#@app.route('/plot/GRADER')
#def plot_hum():
#	times, PHVALUES, GRADERS = getHistData(numSamples)
#	ys = GRADERS
#	fig = Figure()
#	axis = fig.add_subplot(1, 1, 1)
#	axis.set_title("GRADERS [0C]")
#	axis.set_xlabel("Samples")
#	axis.grid(True)
#	xs = range(numSamples)
#	axis.plot(xs, ys)
#	canvas = FigureCanvas(fig)
#	output = io.BytesIO()
#	canvas.print_png(output)
#	response = make_response(output.getvalue())
#	response.mimetype = 'image/png'
#	return response
	
if __name__ == "__main__":
   app.run(host='127.0.0.1', port=80, debug=False)