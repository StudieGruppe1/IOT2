from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('PH_DB1.db', check_same_thread=False)
curs=conn.cursor()

def getLastData():
	for row in curs.execute("SELECT * FROM PH_SENSOR ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		ANALOG_VALUE = row[1]
		PH_VALUE = row[2]
	#conn.close()
	return time, ANALOG_VALUE, PH_VALUE

# Get 'x' samples of historical data
def getHistData (numSamples):
	curs.execute("SELECT * FROM PH_SENSOR ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	ANALOG_VALUES = []
	PH_VALUES = []
	for row in reversed(data):
		dates.append(row[0])
		ANALOG_VALUES.append(row[1])
		PH_VALUES.append(row[2])
	return dates, ANALOG_VALUES, PH_VALUES

# Get Max number of rows (table size)
def maxRowsTable():
	for row in curs.execute("SELECT COUNT(ANALOG_VALUE) from  PH_SENSOR"):  #COUNT = COLUMN NAME
		maxNumberRows=row[0]
	return maxNumberRows

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
        numSamples = 100


# Test data for cleanning possible "out of range" values
def Data(ANALOG_VALUES, PH_VALUES):
	n = len(ANALOG_VALUES)
	for i in range(0, n-1):
		if (ANALOG_VALUES[i] < -10 or ANALOG_VALUES[i] >50):
			ANALOG_VALUES[i] = ANALOG_VALUES[i-2]
		if (PH_VALUES[i] < 0 or PH_VALUES[i] >100):
			PH_VALUES[i] = ANALOG_VALUES[i-2]
	return ANALOG_VALUES, PH_VALUES


# Get sample frequency in minutes
def freqSample():
	times, ANALOG_VALUES, PH_VALUES = getHistData (2)
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp0 = datetime.strptime(times[0], fmt)
	tstamp1 = datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)


global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 100
				
		
# main route 
@app.route("/")
def index():
	time, ANALOG_VALUE, PH_VALUE = getLastData()
	templateData = {
	  'time'		: time,
      'ANALOG_VALUE'		: ANALOG_VALUE,
      'PH_VALUE'		:PH_VALUE,
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
    
    time, ANALOG_VALUE, PH_VALUE = getLastData()
    
    templateData = {
	  'time'		: time,
      'ANALOG_VALUE'		: ANALOG_VALUE,
      'PH_VALUE'		: PH_VALUE,
      'freq'		: freqSamples,
      'rangeTime'	: rangeTime
	}
    return render_template('index.html', **templateData)
	
	
def plot_ANALOG_VALUES():
	times, ANALOG_VALUES, PH_VALUES  = getHistData(numSamples)
	ys = ANALOG_VALUES
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("ANALOG_VALUES")
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

def plot_PH_VALUES():
	times, ANALOG_VALUES, PH_VALUES  = getHistData(numSamples)
	ys =  PH_VALUES
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("PH_VALUES")
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

@app.route('/plot/ANALOG_VALUES')
def plot_ANALOG_VALUES():
	times, ANALOG_VALUES, PH_VALUES  = getHistData(numSamples)
	ys = ANALOG_VALUES
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("ANALOG_VALUES")
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

@app.route('/plot/PH_VALUES')
def plot_PH_VALUES():
	times, ANALOG_VALUES, PH_VALUES  = getHistData(numSamples)
	ys = PH_VALUES
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("PH_VALUES")
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

	
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)