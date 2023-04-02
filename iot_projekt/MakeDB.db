import time
import schedule
import sqlite3
import sys
import smbus
from sens import read_ph_sensor, set_neopixel_leds
from Tomgps import RunGPSLAT, RunGPSLNG

# Makes a variable out of out DB
dbname='PH_DB.db'
con = sqlite3.connect('PH_DB.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PH_SENSOR (TIMESTAMP DATETIME, ANALOG_VALUE NUMERIC, PH_VALUE NUMERIC, LAT_VALUE  REAL, LNG_VALUE REAL)")
    print("DATABASE CREATED")


#Use read PH sensor function from sens.py
read_ph_sensor()
# Use read PH Value funcction from sens.py
ANALOG_VALUE = read_ph_sensor()
set_neopixel_leds(ANALOG_VALUE)
#Import RunGPSLAT and RunGPSLNG function from TomGPS.py
RunGPSLAT()
RunGPSLNG()


#Get the all the data from PH sensor, Neopixel and GPS
def getAnalogdata():
    ANALOG_VALUE = read_ph_sensor()
    PH_VALUE = set_neopixel_leds(ANALOG_VALUE)
    LAT_VALUE = RunGPSLAT()
    LNG_VALUE = RunGPSLNG()
    if ANALOG_VALUE is not None and PH_VALUE is not None and LAT_VALUE is not None and LNG_VALUE is not None:
        ANALOG_VALUE = round(ANALOG_VALUE)
        PH_VALUE = round(PH_VALUE)
        LAT_VALUE = LAT_VALUE
        LNG_VALUE = LNG_VALUE
    return ANALOG_VALUE, PH_VALUE, LAT_VALUE, LNG_VALUE

#Inserts the data from getAnalogdata() into our DB
def logData(ANALOG_VALUE, PH_VALUE, LAT_VALUE, LNG_VALUE):
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    curs.execute("INSERT INTO PH_SENSOR values(datetime('now'),(?),(?),(?),(?))", (ANALOG_VALUE,PH_VALUE, LAT_VALUE, LNG_VALUE,))
    con.commit()
    con.close()


def main():
    try:
        while True:
            #Run all the functions
            #schdule.run_pending()
            RunGPSLAT()
            RunGPSLNG()
            ANALOG_VALUE,PH_VALUE,LAT_VALUE,LNG_VALUE = getAnalogdata()
            logData(ANALOG_VALUE,PH_VALUE,LAT_VALUE,LNG_VALUE)
    except KeyboardInterrupt:
        print("STOP the program")
        con.commit()
        con.close()
        print("Inserting data into database")
        

#Execute all our functions
#schedule.every(5).seconds.do(main)
main()

