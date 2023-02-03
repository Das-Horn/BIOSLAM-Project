from DB import InfluxDB2
from DataIn import Serial
from Controller import PCInputs

def main():
    db = InfluxDB2()
    data = Serial(DB=db)
    control = PCInputs(data)
    pass

if __name__ == "__main__":
    main()