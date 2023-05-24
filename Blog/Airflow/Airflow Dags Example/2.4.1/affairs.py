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
        .appName("affairs") \
        .config(conf=conf) \
        .enableHiveSupport() \
        .getOrCreate()

schema = StructType([
    StructField("affairs", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("age", StringType(), True),
    StructField("yearsmarried", StringType(), True),
    StructField("children", StringType(), True),
    StructField("religiousness", StringType(), True),
    StructField("education", StringType(), True),
    StructField("occupation", StringType(), True),
    StructField("rating", StringType(), True)])

args = {
    'owner': 'affairs',
    'depends_on_past': False,    
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def savetoTable():
    df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/Affairs.csv")
    df2 = df.drop(["Unnamed: 0"], axis=1)
    df2
    myDF = spark.createDataFrame(df2, schema=schema)
    check_tb = os.system("sudo -u hdfs hdfs dfs -ls /user/hive/warehouse/pyspark.db | grep affairs")
    if check_tb == 0:
        myDF.write.mode("append").saveAsTable("pyspark.affairs")
    else:
        os.system("sudo -u hdfs hdfs dfs -rmr /user/hive/warehouse/pyspark.db/affairs")
        myDF.write \
          .mode("overwrite") \
          .saveAsTable("pyspark.affairs")
    
def clearspark():
    spark.stop()
    
dag = DAG(
    dag_id='affairs',
    default_args=args,
    start_date= datetime(2023, 2, 10),
    description='affairs',
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