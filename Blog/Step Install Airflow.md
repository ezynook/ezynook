# Install Airflow

> `ต้องติดตั้ง Ananconda ก่อนติดจั้ง Airflow`

### Create Conda ENV

```
conda create --name airflow_env python=3.9 -y
conda activate airflow_env
```

### Install Airflow

```
pip install "apache-airflow==2.4.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.4.1/constraints-no-providers-3.9.txt"
```

### Airflow Database Init

`airflow db init`

### Airflow Create User

`airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@localhost`

### Upgrade pip

`python -m pip install  --upgrade pip`

### Script to Running (Using PM2)

```
/root/anaconda3/envs/airflow_env/bin/airflow scheduler
/root/anaconda3/envs/airflow_env/bin/airflow webserver --port 8080 --hostname 0.0.0.0 
```

### Install Jupyter

`conda install notebook`

* Jupyter Create Configuration

  `jupyter notebook --generate-config`
* Change Path Default

  `Uncomment #c.NotebookApp.notebook_dir = 'path/notebook'`

### Create Script to Run (On PM2)
`/home/anaconda3/envs/main/bin/jupyter notebook --allow-root --ip=0.0.0.0`
