from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import numpy as np
import utm
import os

from trino.dbapi import connect

now = datetime.now().strftime("%Y-%m-%d")
nowtext = datetime.now().strftime("%Y_%m_%d_%H%M%S")

def get_data(**context):
    conn = connect(
            host="172.16.23.200",
            port=8443,
            user="hive",
            catalog="hive",
            schema="default",
        )
    df = pd.read_sql("SELECT DISTINCT * FROM hive.default.artesian_well_getdata",conn)
    df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['new_long'],df['new_lat']))

    thailand  = gpd.read_file("https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json")
    for i,r in df.iterrows():
        if r['geometry'].is_empty != True:
            for idx,rt in thailand.iterrows():
                if r['geometry'].within(rt['geometry']) == True:
                    df.loc[i,'check_area'] = 2
                    break
                else:
                    df.loc[i,'check_area'] = 1
        else:
            df.loc[i,'check_area'] = np.nan

    df.loc[(df['geometry'].is_empty == True) & (pd.isnull(df['utmeasting'])) & (pd.isnull(df['utmnorthing'])) ,'check_area'] = 0
    df.loc[np.isnan(df['check_area']) & pd.notnull(df['utmeasting']) & pd.notnull(df['utmnorthing']) ,'check_area'] = 3

    data_utmez_null = df.loc[df['check_area'] == 3]
    data_utmez_null['latitude_47'] = utm.to_latlon(data_utmez_null['utmeasting'],data_utmez_null['utmnorthing'], 47, 'N',strict=False)[0]
    data_utmez_null['longitude_47'] = utm.to_latlon(data_utmez_null['utmeasting'],data_utmez_null['utmnorthing'], 47, 'N',strict=False)[1]

    data_utmez_null['latitude_48'] = utm.to_latlon(data_utmez_null['utmeasting'],data_utmez_null['utmnorthing'], 48, 'N',strict=False)[0]
    data_utmez_null['longitude_48'] = utm.to_latlon(data_utmez_null['utmeasting'],data_utmez_null['utmnorthing'], 48, 'N',strict=False)[1]


    for i,r in data_utmez_null.iterrows():
        for idx,rt in thailand.iterrows():
            if Point(r['longitude_47'],r['latitude_47']).within(rt['geometry']) == True:
                df.loc[i,'new_lat'] = r['latitude_47']
                df.loc[i,'new_long'] = r['longitude_47']
                    
                df.loc[i,'check_area'] = 2
                break
                
            elif Point(r['longitude_48'],r['latitude_48']).within(rt['geometry']) == True:
                df.loc[i,'new_lat'] = r['latitude_48']
                df.loc[i,'new_long'] = r['longitude_48']
                    
                df.loc[i,'check_area'] = 2
                break
            else:
                df.loc[i,'check_area'] = 0

    del data_utmez_null


    one_to_two = pd.read_csv('/home/admin/airflow/script/artesian_well/one_to_two.csv')
    one_to_two = one_to_two['no'].values.tolist()
    df.loc[df['no'].isin(one_to_two),'check_area'] = 2

    two_to_one = pd.read_csv('/home/admin/airflow/script/artesian_well/two_to_one.csv')
    two_to_one = two_to_one['no'].values.tolist()
    df.loc[df['no'].isin(two_to_one),'check_area'] = 1


    file_name1='/tmp/view_artesian_well_'+nowtext+'.csv'
    df.to_csv(file_name1,sep="|",index=False,encoding='utf-8-sig')

    try:
        os.system("sudo -u hdfs hdfs dfs -rm /user/hive/warehouse/default/view_artesian_well_group2/*")
    except:
        pass

    df['locat'] = np.nan
    df['yiel_in_8_hour'] = np.nan

    df2 = df[['no', 'locat', 'mubanno', 'mubanname', 'tumbolname', 'ampurname',
        'provincenam', 'wtid', 'welltypename', 'bwdname', 'deeptdrill',
        'deepdev', 'yiel', 'static', 'wdd', 'utmez', 'utmmz', 'utmeasting',
        'utmnorthing', 'lat', 'long', 'yiel_in_8_hour', 'new_lat', 'new_long',
        'geometry', 'date_of', 'check_area']]

    file_name2='/tmp/artesian_well_'+nowtext+'.csv'
    df2.to_csv(file_name2,sep="|",index=False,encoding='utf-8-sig')

    context["ti"].xcom_push(key='file_name1', value=file_name1)
    context["ti"].xcom_push(key='file_name2', value=file_name2)


default_args = {
    'owner': 'mnre',
    'depends_on_past': False,    
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2022, 11, 10)
}
with DAG(
    dag_id='artesian_well',
    default_args=default_args,
    description='artesian_well',
#     schedule_interval='40 6 * * 1',
    schedule_interval='40 00 * * 1',
    catchup=False,
    tags=['ทรัพยากรน้ำ','บ่อน้ำบาดาล']
) as dag:

    t1 = PythonOperator(
        task_id='get_data',
        python_callable=get_data,
        provide_context=True
    )

    t2 = BashOperator(
        task_id="put_data_to_view",
        bash_command=f'sudo -u hdfs hdfs dfs -put {t1.output["file_name1"]} ' 
        '/user/hive/warehouse/default/view_artesian_well_group2/',
    )

    t3 = BashOperator(
        task_id="RemoveTmp_view",
        bash_command=f'cd /tmp;rm -fv {t1.output["file_name1"]} ',
    )

    t4 = BashOperator(
        task_id="put_data_to_well",
        bash_command=f'sudo -u hdfs hdfs dfs -put {t1.output["file_name2"]} ' 
        '/user/hive/warehouse/default/artesian_well/',
    )

    t5 = BashOperator(
        task_id="RemoveTmp_well",
        bash_command=f'cd /tmp;rm -fv {t1.output["file_name2"]} ',
    )

    t1 >> t2 >> t3 >> t4 >> t5