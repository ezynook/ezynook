import cx_Oracle as oc
import pandas as pd
from datetime import datetime
import os

class OracleToHdfs:
    def __init__(self) -> None:
        self.exported()
        
    def dbconnect(self):
        try:
            db = oc.connect('rpalims/adminrpa@10.31.1.69:1521/lims')
            return db.cursor()
        except Exception as e:
            print(e)

    def fnDate(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S"),now.strftime("%Y-%m-%d"),now.strftime("%H"),now.strftime("%Y_%m_%d_%H_%M_%S")

    def CheckHour(self):
        check_hour = OracleToHdfs.fnDate()
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
        filter_date = OracleToHdfs.CheckHour()
        cursor = OracleToHdfs.dbconnect()
        dateSql = OracleToHdfs.fnDate()
        cursor.execute(f"""
                    SELECT
                        *
                    FROM
                        SAPPHIRE.V_RPA_CIOE_07_01
                    WHERE
                        ROWNUM <= 50
                    AND
                        TO_CHAR(CREATEDT, 'YYYY-MM-DD') = '{dateSql[1]}'
                    AND
                        TO_CHAR(CREATEDT,'HH24:MI') >= '{filter_date[0]}'
                    AND 
                        TO_CHAR(CREATEDT,'HH24:MI') <= '{filter_date[1]}'
                    ORDER BY
                        CREATEDT
                """)
        # db.commit()
        arr = []
        for row in cursor:
            arr.append(row)

        if len(df) > 0:
            df = pd.DataFrame(arr)
            df['dllntfdate'] = dateSql[0]
            df.to_csv('/path/to/hdfs/.filename.csv', sep='|', header=False, index=False)
        else:
            print('Record not found in dataframe')

if __name__ == "__main__":
    OracleToHdfs()
