# วิธีกำหนดสิทธิ HDFS, Hive ใน Ranger

### Login เข้าสู่ระบบ

```bash
Username = admin
Password = P@ssw0rd
```

### เลือกเมนู HDFS

* ใส่ข้อมูลตามช่องที่ระบุ
* หลังจากนั้นกด Test Connection ว่า Successfully หรือไม่

```bash
Service Name: ตั้งชื่อ Service
Username: hdfs
Password: hdfs
Namenode URL: hdfs://masternode.bigdata:8020,http://slavenode.bigdata:8020
Add New Configurations: [tag.download.auth.users = hdfs, policy.download.auth.users = hdfs]
```

### เลือกเมนู Hive

```bash
Service Name: HIVE
Username: hive
Password: hive
jdbc.driverClassName: org.apache.hive.jdbc.HiveDriver
#Pattern masternode,slavenode,datanode1
jdbc.url: jdbc:hive2://masternode.bigdata:2181,slavenode.bigdata:2181,datanode01.bigdata:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2
Add New Configurations: [
    tag.download.auth.users = hive
    policy.download.auth.users = hive
    policy.grantrevoke.auth.users = hive
]
```

### หากต้องการเปิดสิทธิหรือเพิ่ม User

* เข้าไปยัง Service ที่ต้องการเพิ่ม เช่น HDFS, HIVE
  * Add New Policy

```bash
Policy Name: something
database: หากต้องการให้เข้าถึงทั้งหมด *
table: หากต้องการให้เข้าถึงทั้งหมด *
Hive column: หากต้องการให้เข้าถึงทั้งหมด *
Select User: เลือก User ที่ต้องการ
Permissions: เลือกการเข้าถึง
ติ๊กถูกตรง [/] Delegate Admin *
```

