import time
import schedule
import sqlite3
import sys



dbname='PH_DB.db'
con = sqlite3.connect('PH_DB.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PH_SENSOR (TIMESTAMP DATETIME, VALUE NUMERIC, WATERTEMP NUMERIC)")
    print("DATABASE CREATED")



#get data from PH sensor
#def getPHdata():
	# Inset pin til vores ph sensor
    # Hvis der er flere pin objekter skal de indsættes her
    #print("")
    # VALUE,WATERTEMP = VORES PIN SOM ER FORBUNDET TIL SENSOR SOM MÅLER PH VÆRDI
    #if "VALUE" is not None and "WATERTEMP" is not None:
        #VALUE = round(VALUE)
        #WATERTEMP = round(WATERTEMP,1)
    #return VALUE, WATERTEMP
	

# Set data into PH sensor db:
#def SetPHdata(VALUE, WATERTEMP):
	#print("Getting PH data:")
	#curs=sqlite3.connect('PH_DB.db')
	#curs.execute("INSERT INTO PH_VALUE values(datetime('now'), (?), (?)", (VALUE, WATERTEMP))
	#curs.commit()
	#curs.close()

# main function
#def main():
	#while True:
		#VALUE, WATERTEMP = getPHdata()
		#SetPHdata (VALUE, WATERTEMO)
		#print("test")

# ------------ Execute program 
#main()