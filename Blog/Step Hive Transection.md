## Step Hive Enable ACID Transactions
#### Hive-site.xml Setting (Ambari or Cloudera)
* Create Tables as ACID Insert Only = False (On Ambari)
* hive.support.concurrency = true
* hive.enforce.bucketing = true
* hive.create.as.external.legacy = true
* hive.exec.dynamic.partition.mode = nonstrict
* hive.txn.manager = org.apache.hadoop.hive.ql.lockmgr.DbTxnManager
* Trino Catalog > /home/trino/etc/catalog/hive/properties <br>
Add Above Line `hive.storage-format=ORC`

#### สร้าง Table โดยใช้ Hive (สามารถใช้งานได้เฉพาะ Hive เท่านั้น)
```bash
CREATE TABLE default.test (
  id int,
  name string
)
CLUSTERED BY (id) INTO 2 BUCKETS STORED AS ORC
TBLPROPERTIES (
  "transactional"="true",
  "compactor.mapreduce.map.memory.mb"="2048",
  "compactorthreshold.hive.compactor.delta.num.threshold"="4",
  "compactorthreshold.hive.compactor.delta.pct.threshold"="0.5"
);
```
`OR`

```bash
CREATE TABLE default.acis_test (
    id int,
    name string
    )
STORED AS ORC
TBLPROPERTIES (
  'transactional'='true'
);
```
#### **แนะนำ** ให้สร้างผ่าน Trino เพราะทำงานแบบ On-Mem จะมีการทำงานที่เร็วกว่า
```bash
CREATE TABLE hive.default.acid_trino2 (
  id int,
  name varchar
)
WITH (
  format = 'ORC',
  transactional=true,
  #partitioned_by = ARRAY['ds', 'country'], #ถ้าต้องการทำ Partition
  #bucketed_by = ARRAY['user_id'], #ถ้าต้องการทำ Bucket
  #bucket_count = 50
);
```
---
# คำสั่งทั้งหมดสำเร็จรูปดังนี้
> ### Create Trino Schema.Table
```bash
CREATE TABLE hive.transaction.covid (
	year int,
	weeknum int,
	province varchar,
	new_case int,
	total_case int,
	new_case_excludeabroad int,
	total_case_excludeabroad int,
	new_death int,
	total_death int,
	update_date string
)
WITH (
  format = 'ORC',
  transactional=true,
);
```
---
```py
import pandas as pd
from trino.dbapi import connect
import os
```
> ## Trino Connection
```py
conn = connect(
    host="192.168.10.210",
    port=8090,
    user="hive",
    catalog="hive",
    schema="transaction",
)
cur = conn.cursor()
```
```py
df = pd.read_json("https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces")

for row in df.itertuples():
    sql = f"""
	    INSERT INTO
		hive.transaction.covid
	    VALUES (
		'{row.year}',
		'{row.weeknum}',
		'{row.province}',
		{row.new_case},
		{row.total_case},
		{row.new_case_excludeabroad},
		{row.total_case_excludeabroad},
		{row.new_death},
		{row.total_death},
		'{row.update_date}'
        )
    """
    cur.execute(sql)
    print('Insert Rows : ', row.province)
```
> ## Update
```py
cur.execute("UPDATE default.covid SET province = 'Bangkok City' WHERE province = 'กรุงเทพมหานคร'")
```
> ## Delete
```py
cur.execute("DELETE FROM transaction.covid WHERE province = 'Bangkok City'")
```
