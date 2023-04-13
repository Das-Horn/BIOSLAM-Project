from DB import InfluxDB2
from DataIn import Serial,WFDB, MQTT
from Controller import *
import os
from dotenv import load_dotenv

from serial.serialutil import *

def main():
    load_dotenv()
    
    db = InfluxDB2(
        token=os.getenv("TOKEN"),
        address="192.168.0.150",
        db_name="ProjectData",
        org="Project"
    )
    # data = Serial(DB=db)
    # data = WFDB(DB=db, file_path="Data-testing/sample-data/ECG/16265")
    data = MQTT(db,server_name="192.168.0.150", length=15)
    control = HeartRate(
        data,
        upper_tresh=3,
        lower_tresh=-1.1,
        baseline=1.66
    )
    
    # Event Loop
    try:
        while True:
            os.system('cls')
            print(f'Current Buffer Stats = {control.update() * 4} bpm')
    except KeyboardInterrupt as c :
        print("Stopping Program...")
        sys.exit(1)
        # Enter any cleanup data here
    except SerialException as se:
        print("Error connecting to board please make sure it is connedcted properly.")
        print(f'Port : {data.get_serial_port()}\nBaudrate : {data.get_baudrate()}')
        print(f'\n\nMore Error details below..\n{se}')
    pass

if __name__ == "__main__":
    main()