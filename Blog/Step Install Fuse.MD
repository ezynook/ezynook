# Step Install Hadoop-Fuse Using Ambari (CentOS 7)

```bash
#Copy Repo ของ ambari.repo นำไปวางที่
/etc/yum.repos.d/
```
## ติดตั้ง Fuse library
```bash
yum install -y hadoop
yum install -y hive
yum install -y fuse*
yum install -y hadoop-hdfs-fuse
```
## กำหนด JVM Path
```bash
vim /root/.profile
export LD_LIBRARY_PATH=/usr/local/jdk8u222-b10/jre/lib/amd64/:/usr/local/jdk8u222-b10/jre/lib/amd64/server
source /root/.profile

#Copy HDFS Lib
cp /usr/hdp/3.1.0.0-78/usr/lib/libhdfs.so.0.0.0 /usr/local/jdk8u222-b10/jre/lib/amd64/server/
```
## วิธีการ Mount HDFS
```sh
hadoop-fuse-dfs dfs://nn01.bigdata:8020 /hdfs
```
## วิธีการเช็ค HDFS Mount ตอนเปิดเครื่อง
```bash
vim /home/fuse.sh
```
``` bash
#!/bin/bash

MOUNT=`cat /proc/mounts | grep fuse_dfs`

if [ -z "$MOUNT" ]; then
        umount /hdfs
        hadoop-fuse-dfs dfs://nn01.bigdata:8020 /hdfs
        echo "Hadoop Fuse is Umount Will Fixed Successfully" >> /var/log/fuse.log
else
        echo "Hadoop Fuse Already" >> /var/log/fuse.log
fi
```
```bash
chmod +x /home/fuse.sh
```
```bash
vim /root/.bashrc
#เพิ่มคำสั่งนี้บรรทัดสุดท้าย
bash /home/fuse.sh
```
## หรือจะเช็คทุกเวลาที่ต้องการโดยใช้ Crontab ดังนี้
```bash
crontab -e
```
```bash
*/15 * * * * /home/fuse.sh
```