from DB import InfluxDB2
from DataIn import Serial
from Controller import PCInputs
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    db = InfluxDB2(
        token=os.getenv("TOKEN"),
        address="192.168.0.150",
        db_name="ProjectData",
        org="Project"
    )
    data = Serial(DB=db)
    control = PCInputs(
        data,
        upper_tresh=3,
        lower_tresh=1,
        baseline=1.66
    )
    
    # Event Loop
    try:
        while True:
            os.system('cls')
            print(f'Current Buffer Stats = {control.update()}')
    except KeyboardInterrupt as c :
        print("Stopping Program...")
        # Enter any cleanup data here
    pass

if __name__ == "__main__":
    main()