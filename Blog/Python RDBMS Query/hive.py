from multiprocessing import connection
from pyhive import hive
import pandas as pd

class readHive:

    def __init__(self) -> None:
        self.getData()

    def getData(self):
        conn = hive.Connection(host="bigdata.softnix.co.th", port=10000, username="hive")
        df = pd.read_sql("SELECT * FROM default.weatherquality limit 10", conn)
        # df.to_csv(r'./dwr_flood_drought.csv', index=None, sep='|')
        if len(df):
            print(df)
        else:
            print('error no record found !')

if __name__ == "__main__":
    readHive()