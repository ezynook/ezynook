# Apache Iceberg Table

```
CREATE EXTERNAL TABLE `iceberg_pyspark.tbl_engineer`(
  `id` int, 
  `workby` string, 
  `customer` string, 
  `site` string, 
  `malltype` string, 
  `worktype` string, 
  `details` string, 
  `onsite` string, 
  `time` string, 
  `travel` string, 
  `engineer` string, 
  `status` string, 
  `day` string, 
  `date_end` string, 
  `status_work` string, 
  `end_job_detail` string, 
  `file_location` string, 
  `update_by` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  '/user/hive/warehouse/iceberg_pyspark/tbl_engineer/data'
TBLPROPERTIES (
  'spark.sql.create.version'='3.3.1', 
  'spark.sql.sources.provider'='parquet'
  );
```
