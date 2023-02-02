import wfdb
from influxdb_client import InfluxDBClient
import time
from datetime import datetime


def main():
    #Getting Waveform data from record
    record = wfdb.rdrecord('sample-data/16265') # p_signal to get data, 
    
    # Uploading Data to Database
    client = InfluxDBClient(url="http://192.168.0.150:8086", token="BhrNgTdlkn6ycGDsm_vx9GjEFs2xJYpyYbj7U-WXIxzbBlSuapJTbNdIaCBR5tO69_WPJTRwaGLqKva14PUQdw==", org="Y4 Project")
    wirte_api = client.write_api()
    for vals in record.p_signal:
        points = [
            {
                "measurement": "Waveform",
                "tags": {
                    "Record":record.record_name,
                    "Unit": record.units[0],
                    "Measurement":record.sig_name[0]
                },
                "fields": {
                    "value":vals[0]
                },
                "time": int(round(time.time() * 1000000000))
            },
            {
                "measurement": "Waveform",
                "tags": {
                    "Record":record.record_name,
                    "Unit": record.units[1],
                    "Measurement":record.sig_name[1]
                },
                "fields": {
                    "value":vals[1]
                },
                "time": int(round(time.time() * 1000000000))
            }
        ]
        print(f'Writing point to DB : {points}')
        wirte_api.write("Waveforms","Y4 Project", points)
        time.sleep(0.00001)

    
    
if __name__ == "__main__":
    main()