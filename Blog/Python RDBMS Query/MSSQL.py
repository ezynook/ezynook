import pyodbc 
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import os as exec

class MSSQLToHdfs:
    def __init__(self):
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
        return now.strftime("%Y-%m-%d %H:%M:%S"),now.strftime("%Y-%m-%d"),now.strftime("%H"),now.strftime("%Y_%m_%d_%H_%M_%S"),now.strftime("%Y")

    def CheckHour():
        check_hour = MSSQLToHdfs.fnDate()
        if (check_hour[2] >= '00' and check_hour[2] <= '01'):
            return '00:00', '01:00'
        elif (check_hour[2] >= '02' and check_hour[2] <= '03'):
            return '02:00', '03:00'
        elif (check_hour[2] >= '04' and check_hour[2] <= '05'):
            return '04:00', '05:00'
        else:
            return '', ''

    def exported(self):
        filter_date = MSSQLToHdfs.CheckHour()
        cursor = MSSQLToHdfs.dbconnect()
        dateSql = MSSQLToHdfs.fnDate()
        cursor.execute(f"""
                    SELECT
                        *
                    FROM
                        dexProjDb.dlpoc.fg_ftockInventory_WMS_daily
                    WHERE 
                        FORMAT(INTF_DATE, 'YYYY-MM-DD') = '{dateSql[1]}'
                    AND
                        convert(varchar, INTF_DATE, 5) BETWEEN '{filter_date[0]}' AND '{filter_date[1]}'
                    ORDER BY
                        INTF_DATE
                """)
        # db.commit()
        arr = []
        for row in cursor:
            arr.append(row)

        df = pd.DataFrame(arr)
        if len(df) > 0:
            df['dllntfdate'] = dateSql[0]
            exec.system(f"mkdir -p /hdfs/user/hive/warehouse/irpc.db/fg_ftockInventory_WMS_daily/{dateSql[4]}")
            df.to_csv(f"/hdfs/user/hive/warehouse/irpc.db/fg_ftockInventory_WMS_daily/{dateSql[4]}/fg_ftockInventory_WMS_daily_{dateSql[3]}.csv", sep='|', header=False, index=False)
            return df
        else:
            print('no record found')

if __name__ == "__main__":
    MSSQLToHdfs.exported()