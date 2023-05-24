import cx_Oracle
import pandas as pd
from datetime import date, datetime
import os as exe

class OracleToHdfs:

    def __init__(self) -> None:
        self.exported()

    def dbconnect(self):
        try:
            db = cx_Oracle.connect('rpalims/adminrpa@10.31.1.69:1521/lims')
            return db.cursor()
        except:
            print("An exception occurred")

    def fnDate(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S"),now.strftime("%Y-%m-%d"),now.strftime("%H"),now.strftime("%Y_%m_%d_%H_%M_%S"), now.strftime("%Y")

    def valdate(self):
        valdate1 = '2010-08'
        valdate2 = '2010-08'
        valdate3 = '2010'
        return valdate1,valdate2,valdate3

    def CheckHour(self):
        check_hour = OracleToHdfs.fnDate()
        if (check_hour[2] >= '06' and check_hour[2] <= '08'):
            return '06:00', '08:00'
        elif (check_hour[2] >= '10' and check_hour[2] <= '12'):
            return '10:00', '12:00'
        elif (check_hour[2] >= '14' and check_hour[2] <= '16'):
            return '14:00', '16:00'
        elif (check_hour[2] >= '10' and check_hour[2] <= '12'):
            return '10:00', '12:00'
        elif (check_hour[2] >= '12' and check_hour[2] <= '14'):
            return '12:00', '14:00'
        elif (check_hour[2] >= '14' and check_hour[2] <= '16'):
            return '14:00', '16:00'
        elif (check_hour[2] >= '16' and check_hour[2] <= '18'):
            return '16:00', '18:00'
        elif (check_hour[2] >= '18' and check_hour[2] <= '20'):
            return '18:00', '20:00'
        else:
            return '', ''

    def exported(self):
        filter_date = OracleToHdfs.CheckHour()
        cursor = OracleToHdfs.dbconnect()
        dateSql = OracleToHdfs.fnDate()
        valdatefn = OracleToHdfs.valdate()
        cursor.execute(f"""
                    SELECT
                        *
                    FROM
                        SAPPHIRE.V_RPA_CIOE_07_01
                    WHERE
                        TO_CHAR(CREATEDT, 'YYYY-MM-DD') = '2021'
                    ORDER BY CREATEDT
                """)
        # db.commit()
        arr = []
        for row in cursor:
            arr.append(row)

        df = pd.DataFrame(arr)
        if len(df) > 0:
            df['dllntfdate'] = dateSql[0]
            exe.system(f"mkdir -p /hdfs/user/hive/warehouse/irpc.db/V_RPA_CIOE_07_01/{dateSql[4]}")
            df.to_csv(f'/hdfs/user/hive/warehouse/irpc.db/V_RPA_CIOE_07_01/{dateSql[4]}/V_RPA_CIOE_07_01_{dateSql[3]}.csv', sep='|', index=False, header=False)
            # return df
            cursor.close()
        else:
            print('no record found')

#Call My Function
if __name__ == "__main__":
    OracleToHdfs()