from DB import InfluxDB2
from DataIn import Serial
from Controller import PCInputs
import os

def main():
    db = InfluxDB2()
    data = Serial(DB=db)
    control = PCInputs(data)
    
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