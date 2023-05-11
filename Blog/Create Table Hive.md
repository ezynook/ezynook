# Create Database

```
CREATE DATABASE dbname LOCATION '/user/hive/warehouse/mnre/rain';
```

# Create Table CSV Type

```
CREATE TABLE Schema.`TableName`(  
	`col` string
	)   
ROW FORMAT SERDE   
   'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'  
WITH SERDEPROPERTIES (   
   'field.delim'='|',  
   'serialization.format'='|')   
STORED AS INPUTFORMAT  
   'org.apache.hadoop.mapred.TextInputFormat'   
OUTPUTFORMAT   
   'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' 
LOCATION   
   '/user/hive/warehouse/schema/TableName' 
TBLPROPERTIES ("skip.header.line.count"="1");
```

# Create Table Parquet Type

```
CREATE TABLE `schema.tablename`(
  `col` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  '/spark/iceberg/schema/table'
TBLPROPERTIES (
  'spark.sql.create.version'='3.3.1', 
  'spark.sql.sources.provider'='parquet');
```
