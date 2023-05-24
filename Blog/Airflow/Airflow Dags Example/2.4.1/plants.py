from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import pyspark
import pandas as pd
import requests
import json
import os

now = datetime.now()
update_dt = now.strftime("%Y-%m-%d %H:%M:%S")
today = now.strftime("%Y-%m-%d")

os.environ['HADOOP_CONF_DIR'] = '/etc/hadoop/conf'
os.environ['JAVA_HOME'] = '/usr/local/jdk8u222-b10'
os.environ['HADOOP_USER_NAME']='hive'
os.environ['PYSPARK_PYTHON'] ='/HDFS01/anaconda3/envs/main/bin/python'
conf = pyspark.SparkConf().setAll([
     ('spark.driver.maxResultSize', '0'),
     ('spark.driver.memory', '2g'),
     ('spark.sql.repl.eagerEval.enabled','true'),
     ('hive.strict.managed.tables','false'),
     ('hive.metastore.uris', 'thrift://nn01.bigdata:9083'),
     ('metastore.client.capability.check','false')
    ])
spark = SparkSession.builder \
        .master("local[*]") \
        .appName("plants") \
        .config(conf=conf) \
        .enableHiveSupport() \
        .getOrCreate()

schema = StructType([
    StructField("province_id", StringType(), True),
    StructField("des_id", StringType(), True),
    StructField("route_name", StringType(), True),
    StructField("how_long", StringType(), True),
    StructField("staff", StringType(), True),
    StructField("width", StringType(), True),
    StructField("len", StringType(), True),
    StructField("update_date", StringType(), True),
])

args = {
    'owner': 'plants',
    'depends_on_past': False,    
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def savetoTable():
    df = spark.createDataFrame(pd.read_excel('https://data.go.th/dataset/723f4c28-79de-4a29-bea9-efacbaec236d/resource/db646c54-2780-4b06-bc27-d4455ad1a6f4/download/untitled.xlsx'), schema=schema)
    df = df.withColumn("update_dt", lit(update_dt))
    check_tb = os.system("sudo -u hdfs hdfs dfs -ls /user/hive/warehouse/pyspark.db | grep plants")
    if check_tb == 0:
        df.write.mode("append").saveAsTable("pyspark.plants")
    else:
        os.system("sudo -u hdfs hdfs dfs -rmr /user/hive/warehouse/pyspark.db/plants/")
        df.write.mode("overwrite").saveAsTable("pyspark.plants")
        
def clearspark():
    spark.stop()
    
dag = DAG(
    dag_id='plants',
    default_args=args,
    start_date= datetime(2023, 2, 10),
    description='plants',
    catchup=False,
    schedule_interval='15 15 * * *',
)

t1 = PythonOperator(
    task_id='Save_to_Hive',
    python_callable=savetoTable,
    dag=dag
)

t2 = PythonOperator(
    task_id="Clear_Session_Pyspark",
    python_callable=clearspark,
    dag=dag
)

t1 >> t2