import pyodbc 
import pandas as pd
from datetime import datetime

class MSSQLToHDfs:

    def __init__(self) -> None:
        self.exported()

    def dbconnect(self):
        try:
            db = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                "Server=INTFPHDDB-DEV;"
                "Database=dexProjDb;"
                "UID=dlpoc;"
                "PWD=pocdlread@2022;")
            return db.cursor()
        except Exception as e:
            print(e)

    def fnDate(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S"),now.strftime("%Y-%m-%d"),now.strftime("%H"),now.strftime("%Y_%m_%d_%H_%M_%S")

    def CheckHour(self):
        check_hour = MSSQLToHDfs.fnDate()
        if (check_hour[2] >= '06' and check_hour[2] <= '08'):
            return '06:00', '08:00'
        elif (check_hour[2] >= '10' and check_hour[2] <= '12'):
            return '10:00', '12:00'
        elif (check_hour[2] >= '14' and check_hour[2] <= '16'):
            return '14:00', '16:00'
        elif (check_hour[2] >= '18' and check_hour[2] <= '20'):
            return '10:00', '12:00'
        else:
            return '', ''

    def exported(self):
        filter_date = MSSQLToHDfs.CheckHour()
        cursor = MSSQLToHDfs.dbconnect()
        dateSql = MSSQLToHDfs.fnDate()
        cursor.execute(f"""
                    SELECT
                        *
                    FROM
                        dexProjDb.dlpoc.tlastfl_journal
                    WHERE 
                        FORMAT(dwhIntfDate, 'YYYY-MM-DD') = '{dateSql[1]}'
                    AND
                        convert(varchar, dwhIntfDate, 5) BETWEEN '{filter_date[0]}' AND '{filter_date[1]}'
                    ORDER BY
                        dwhIntfDate
                """)
        # db.commit()
        arr = []
        for row in cursor:
            arr.append(row)

        if len(df) > 0:
            df = pd.DataFrame(arr)
            df['dllntfdate'] = dateSql[0]
            df.to_csv(f"/hdfs/user/hive/warehouse/irpc.db/tlastfl_journal/2022/tlastfl_journal_{dateSql[3]}.csv", sep='|', header=False, index=False)
            cursor.close()
        else:
            print('No Record found in dataframe')
