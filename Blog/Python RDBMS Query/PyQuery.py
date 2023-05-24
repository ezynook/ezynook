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

    def exported(self):
        cursor = self.dbconnect()
        dateSql = self.fnDate()
        cursor.execute(f"""
                    SELECT
                        *
                    FROM
                        SAPPHIRE.V_RPA_CIOE_07_01
                    WHERE
                        TO_CHAR(CREATEDT, 'YYYY') = '2021'
                    ORDER BY CREATEDT
                """)
        # db.commit()
        arr = []
        for row in cursor:
            arr.append(row)

        df = pd.DataFrame(arr)
        if len(df) > 0:
            df['dllntfdate'] = dateSql[0]
            print(df)
            cursor.close()
        else:
            print('no record found')

#Call My Function
if __name__ == "__main__":
    OracleToHdfs()