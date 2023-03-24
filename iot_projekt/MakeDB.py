import time
#import schedule
import sqlite3
import sys
#import Adafruit_DHT


dbname='PH_DB.db'
con = sqlite3.connect('PH_DB.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF NOT EXSITS PH_VALUE")
    cur.execute("CREATE TABLE PH_SENSOR (TIMESTAMP DATETIME, VALUE NUMERIC, WATERTEMP NUMERIC)")
    print("DATABASE CREATED")


# get data from DHT sensor
#def getDHTdata():	
#	DHT22Sensor = Adafruit_DHT.DHT22
#	DHTpin = 16
#	hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
#	if hum is not None and temp is not None:
#		hum = round(hum)
#		temp = round(temp, 1)
#	return temp, hum

#get data from PH sensor
def getPHdata():
	# Inset pin til vores ph sensor
    # Hvis der er flere pin objekter skal de indsættes her
    print("")
    # VALUE,WATERTEMP = VORES PIN SOM ER FORBUNDET TIL SENSOR SOM MÅLER PH VÆRDI
    # if "VALUE" is not None and "WATERTEMP" is not None:
        #VALUE = round(VALUE)
        #WATERTEMP = round(WATERTEMP,1)
    #return VALUE, WATERTEMP
	

# log sensor data on database
#def logData (temp, hum):
#	conn=sqlite3.connect(dbname)
#	curs=conn.cursor()
#	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
#	conn.commit()
#	conn.close()

# Set data into PH sensor db:
def SetPHdata():
	print("Getting PH data:")
	curs=sqlite3.connect('PH_DB.db')
	#curs.execute("INSERT INTO PH_VALUE values(datetime('now'), (?), (?)", (VALUE, WATERTEMP))
	curs.commit()
	curs.close()

# main function
def main():
	while True:
		#temp, hum = getDHTdata()
		#logData (temp, hum)
		#time.sleep(sampleFreq)
		print("test")

# ------------ Execute program 
main()