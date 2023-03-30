import time
import schedule
import sqlite3
import sys
from ph_read import Values

dbname='PH_DB.db'
con = sqlite3.connect('PH_DB.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PH_SENSOR (TIMESTAMP DATETIME, PH_VALUE NUMERIC)")
    print("DATABASE CREATED")

#Import value function from ph_read.py
Values()
#print(a)


#get data from PH sensor MÅSKE SKAL DETTE SLETTES DA VI ALLEREDE FÅR DATA
#def getPHdata():
	# Inset pin til vores ph sensor Det skulle gerne være "PIN GPIO 2 OG 3, MÅSKE 3 OG 5"
    # Hvis der er flere pin objekter skal de indsættes her
    #print("Test")
    # VALUE,WATERTEMP = VORES PIN SOM ER FORBUNDET TIL SENSOR SOM MÅLER PH VÆRDI
    #if "VALUE" is not None and "WATERTEMP" is not None:
        #PH_VALUE = round(VALUE)
    #return PH_VALUE, 

def getPHdata():
    PH_VALUE = Values()
    if PH_VALUE is not None:
        PH_VALUE = round(PH_VALUE)
        #print(f'{PH_VALUE}',"INDE I getPHdata")
    return PH_VALUE




# Set data into PH sensor db:
#def SetPHdata(VALUE, WATERTEMP):
	#print("Getting PH data:")
	#curs=sqlite3.connect('PH_DB.db')
	#curs.execute("INSERT INTO PH_VALUE values(datetime('now'), (?), (?)", (VALUE, WATERTEMP))
	#curs.commit()
	#curs.close()

def sendPHdata(PH_VALUE):
    print("Inserting PH values into DB")
    conn = sqlite3.connect(dbname)
    curs =con.cursor()
    curs.execute("INSERT INTO PH_SENSOR values(datetime('now'),(?))", (PH_VALUE,))
    conn.commit()
    conn.close()


# main function
#def main():
	#while True:
		#VALUE, WATERTEMP = getPHdata()
		#SetPHdata (VALUE, WATERTEMO)
		#print("test")
def main():
    while True:
        PH_VALUE = getPHdata()
        sendPHdata(PH_VALUE)

# ------------ Execute program 
main()