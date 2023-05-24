#!/root/anaconda3/bin/python
from datetime import datetime, timedelta
import os, time
import sqlite3

class Airflow:

    def __init__(self) -> None:
        self.getData()

    def dbconnect(self):
        try:
            conn = sqlite3.connect('/root/airflow/airflow.db')
            return conn
        except Exception as e:
            print('dbconnection error!', e)

    def getToday(self):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        return today

    def getYesterday(self):
        yest = datetime.now() + timedelta(days = -1)
        day_yest = yest.strftime("%Y-%m-%d")
        return day_yest

    def getData(self):
        today = self.getToday()
        conn = self.dbconnect()
        sql = f"""
                SELECT 
                    dag_id, 
                    STRFTIME('%d-%m-%Y %H:%M:%S', start_date) as start_date, 
                    state 
                FROM 
                    dag_run 
                WHERE
                    STRFTIME('%Y-%m-%d', start_date) = '{today}'
            """
        cursor = conn.execute(sql)
        strData = ""
        for row in cursor:
            strData += "Dagname: " + row[0]+"\n"
            strData += "Date: " + row[1]+"\n"
            strData += "Status: " + row[2]+"\n"

        print(strData)
        #สำรองไว้ส่งตรงหา Zabbix Trapper items
        #os.system(f'zabbix_sender -z 10.30.99.242 -s "mgnt-etl.tat.or.th" -k db.status -o "{str(e)}"')
        conn.close()

if __name__ == '__main__':
    Airflow()
