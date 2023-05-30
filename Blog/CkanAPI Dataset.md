## 📚 Data Explorer in CKAN Open-D

---
### ✅ สร้าง Dataset ใน Web UI แบบ Manual ก่อน โดยเลือก Datatype เป็น CSV, XLSX เท่านั้น เพื่อใช้งาน Data Explorer

__ฐานข้อมูลที่เกี่ยวข้อง (schema.table)__

__ชื่อ Dataset ใน DB__ = ckan.resource.[package_id <span style="color:red">(เชื่อมโยงกับ ckan.package.id)</span>]

__ชื่อ Data Explorer ใน DB__ = datastore.[ชื่อ Table จะเป็น Package_ID]

---

__รูปแบบการตั้งชื่อไฟล์__

__resource.package_id__ = <span style="color:red">(a6b) </span><span style="color:blue">(da3) </span><span style="color:#009900">(34-f78a-42dc-81ab-4e934f98c0ac)</span>
__Directory ที่ใช้ในการวางไฟล์ใน Host ตัวอย่าง__

🔴 Directory

🔵 Sub-Directory

🟢 File (Non Extension)

/var/lib/ckan/resources/<span style="color:red">a6b</span>/<span style="color:blue">da3</span>/<span style="color:#009900">34-f78a-42dc-81ab-4e934f98c0ac</span>

---
__หากมีการเอาไฟล์ไปวางทับใน Path มีความจำเป็นต้อง Overwrite Data Explorer ในส่วน datastore.[ชื่อ Table จะเป็น Package_ID] ด้วย เนื่องจากไฟล์กับ Data Explorer จะไม่เหมือนกัน__

---
__Data Explorer Columes__

| _id | _full_text | Columes อื่นๆตาม Structure ปกติ |
|-----|------------|---------------------------------|
| 1   | NULL       | bla bla                         |

# API


```python
import pandas as pd
import psycopg2 as pg
import numpy as np
import os
from sqlalchemy import create_engine
from urllib.parse import quote
import json
import requests

USERNAME='ckan'
PASSWORD='ckan'
IPADDR='192.168.10.98'
DB='datastore'
#datastore.package_id
TABLE_ID="7654c4b2-5ef7-4e93-affe-09acbb06402a"
#Docker volume
FILE_PATH="/var/lib/ckan/resources/765/4c4/"
#ckan.resource.package_id
FILE_NAME="b2-5ef7-4e93-affe-09acbb06402a"

class SDC_API:
    def __init__(self) -> None:
        self.editDataExplorer()
        
    def Connect(self):
        engine = create_engine(f"postgresql://{USERNAME}:%s@{IPADDR}/{DB}" % quote(f'{PASSWORD}'))
        return engine
        
    def editDataExplorer(self):
        #Call API
        url = "http://demo-cinspire.myddns.me:9400/json/MEA/usage_distict"
        response = requests.get(url, auth=("admin", "Dci@2560"), verify=False)
        data = response.json()
        data1 = data['MEA.usage_distictResponse']['MEA.usage_distictOutput']['MEA.row']
        #Append to DataFrame
        df = pd.DataFrame(data1)
        df.insert(0, '_id', df.index)
        df.insert(1, '_full_text', np.nan)
        df.to_sql(f"{TABLE_ID}", self.Connect(), if_exists='replace', index=False)
        print("Success")
        
if __name__ == '__main__':
    obj = SDC_API()
```

# API and Dataset


```python
import pandas as pd
import psycopg2 as pg
import numpy as np
import os
from sqlalchemy import create_engine
from urllib.parse import quote

USERNAME='ckan'
PASSWORD='ckan'
IPADDR='192.168.10.98'
DB='datastore'
#datastore.package_id
TABLE_ID="7654c4b2-5ef7-4e93-affe-09acbb06402a"
#Docker volume
FILE_PATH="/home/volume/volumes/open-data_ckan_storage/_data/resources/765/4c4/"
#ckan.resource.package_id
FILE_NAME="b2-5ef7-4e93-affe-09acbb06402a"

class SDC:
    def __init__(self) -> None:
        self.getData()
        
    def Connect(self):
        engine = create_engine(f"postgresql://{USERNAME}:%s@{IPADDR}/{DB}" % quote(f'{PASSWORD}'))
        return engine
    
    def getData(self):
        url = "http://demo-cinspire.myddns.me:9400/json/MEA/usage_distict"
        response = requests.get(url, auth=("admin", "Dci@2560"), verify=False)
        data = response.json()
        data1 = data['MEA.usage_distictResponse']['MEA.usage_distictOutput']['MEA.row']
        #Append to DataFrame
        df = pd.DataFrame(data1)
        os.system(f"rm -f {FILE_PATH}*")
        df.to_csv(f"{FILE_PATH}{FILE_NAME}", index=False)
        print(f"Replace {FILE_NAME} Success")
        self.editDataExplorer(df)
        
    def editDataExplorer(self, df):
        df.insert(0, '_id', df.index)
        df.insert(1, '_full_text', np.nan)
        df.to_sql(f"{TABLE_ID}", self.Connect(), if_exists='replace', index=False)
        print("Success Append Data Explorer")
        
if __name__ == '__main__':
    obj = SDC()
```
