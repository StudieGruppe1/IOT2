import sqlite3 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)


conn = sqlite3.connect('PH_DB.db',check_same_thread=False) 
curs = conn.cursor() 
curs.execute("SELECT TIMESTAMP, PHVALUE from PH_SENSOR") 
#data = curs.fetchall() 
#TIMESTAMP = [] 
#PHVALUE = [] 
#for i in data: 
    #TIMESTAMP.append(i[0])	#x column contain data(1,2,3,4,5) 
    #PHVALUE.append(i[1])	#y column contain data(1,2,3,4,5) 
#plt.plot(TIMESTAMP,PHVALUE) 
#plt.show()

def Data(PHVALUES):
	n = len(PHVALUES)
	for i in range(0, n-1):
		if (PHVALUES[i] < -10 or PHVALUES[i] >50):
			PHVALUES[i] = PHVALUES[i-2]
	return PHVALUES

def maxRowsTable():
	for row in curs.execute("SELECT COUNT(PHVALUE) from  PH_SENSOR"):  #COUNT = COLUMN NAME
		maxNumberRows=row[0]
	return maxNumberRows

global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
        numSamples = 100

@app.route('/plot/PHVALUE')
def plot_PHVALUE():
	PH_VALUES = Data
	ys = PH_VALUES
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

	
if __name__ == "__main__":
   app.run(host='127.0.0.1', port=80, debug=False)