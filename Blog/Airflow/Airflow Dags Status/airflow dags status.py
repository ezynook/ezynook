import psycopg2
from datetime import datetime
import os, time

os.environ['TZ'] = 'Asia/Bangkok'
time.tzset()

class AirflowTAT:
    def __init__(self) -> None:
        self.getData()

    def connect(self):
        conn = psycopg2.connect(
            database = "airflow",
            user = "airflow",
            password = "airflow",
            host = "10.41.1.25",
            port = "5432"
        )
        return conn

    def getToday(self):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        return dt_string
    
    def getData(self):
        today = self.getToday()
        conn = self.connect()
        sql = (f"""
                SELECT
                    dag_id,
                    execution_date at time zone 'Asia/Bangkok' as dt,
                    "state"
                FROM
                    dag_run
                WHERE
                    (
                        CAST((execution_date AT TIME ZONE 'Asia/Bangkok') AS date) = DATE '{today}'
                        AND
                        dag_id = 'social_lets_travel'
                    )
                ORDER BY
                    execution_date DESC
        """)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print('DagID = ', row[0])
            print('StartDate = ', row[1])
            print('State = ', row[2], "\n")

        conn.close()

if __name__ == '__main__':
    AirflowTAT()