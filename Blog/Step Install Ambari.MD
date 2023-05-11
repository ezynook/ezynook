# ขั้นตอนก่อนติดตั้ง Ambari

```sh
- vi /etc/selinux/config 	>> SELINUX=disabled
- systemctl stop firewalld & systemctl disable firewalld    >> ปิด Firewall
- yum -y install chrony or ntpd    >>sync time turn ntpd on check เรื่องเวลาทุกเครื่องให้ ตรงกัน
```

# ทำทุกเครื่อง Ambari server ถ้าไม่ทำจะติดปัญหา install package smartsense-hst ไม่ผ่าน

สร้างไฟล์ /etc/yum.repo.d/ambari.repo ข้างในใส่ดังนี้

```
[ambari]
name=ambari repo
baseurl=http://ro-bucharest-repo.bigstepcloud.com/hortonworks-repos/ambari/centos7/2.7.3.0/  
or 
baseurl=https://makeopensourcegreatagain.com/rpms/
enabled=1
gpgcheck=0
```

# ตั้งชื่อ hostname

`vi /etc/hosts`

```
192.168.10.226  nn01.softnix
192.168.10.227  nn02.softnix
192.168.10.228  dn01.softnix
192.168.10.229  dn02.softnix
```

*Make sure ว่า run hostname -f  แล้วจะ return server2.softnix.co.th ไม่เช่นนั้นจะ deploy ไม่ผ่าน*

# ติดตั้ง ambari server

```
- wget http://ro-bucharest-repo.bigstepcloud.com/hortonworks-repos/ambari/centos7/2.7.3.0/ambari/ambari-server-2.7.3.0-139.x86_64.rpm
or
- wget http://172.17.45.16/repos/hortonworks-repos/ambari/centos7/2.7.3.0/ambari/ambari-server-2.7.3.0-139.x86_64.rpm
- yum install ambari-server-2.7.3.0-139.x86_64.rpm -y		>> จะติดตั้ง dependency มาให้ด้วย
```

# ติดตั้ง Database and config

```

- yum install mariadb mariadb-server mysql-connector-java.noarch -y
- wget http://172.17.45.16/repos/centos/7/os/x86_64/Packages/mysql-connector-java-5.1.49.jar
- #wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.49/mysql-connector-java-5.1.49.jar
- cp mysql-connector-java-5.1.49.jar /usr/share/java/mysql-connector-java.jar
- systemctl start mariadb & systemctl enable mariadb
- mysql -uroot -p
> set password = password('password');
> flush privileges;
> create database ambari;
> use ambari;
> CREATE USER 'ambari'@'%' IDENTIFIED BY 'admin';
> GRANT ALL PRIVILEGES on *.* To 'ambari'@'%' IDENTIFIED BY 'admin';
> CREATE USER 'ambari'@'nn01.irpc' IDENTIFIED BY 'admin';
> GRANT ALL PRIVILEGES on *.* To 'ambari'@'nn01.irpc' IDENTIFIED BY 'admin';
> CREATE USER 'ambari'@'localhost' IDENTIFIED BY 'admin';
> GRANT ALL PRIVILEGES on *.* To 'ambari'@'localhost' IDENTIFIED BY 'admin';
> flush privileges;

```

# ถ้าต้องการติดตั้ง hive สร้าง db hive และ user hive บน mysql ไว้

```
> MariaDB [(none)]> create database hive;
> MariaDB [(none)]> CREATE USER 'hive'@'nn01.irpc' IDENTIFIED BY 'hive';
> MariaDB [(none)]> CREATE USER 'hive'@'localhost' IDENTIFIED BY 'hive';
> MariaDB [(none)]> CREATE USER 'hive'@'%' IDENTIFIED BY 'hive';
> MariaDB [(none)]> GRANT ALL PRIVILEGES on *.* To 'hive'@'nn01.irpc' IDENTIFIED BY 'hive';
> MariaDB [(none)]> GRANT ALL PRIVILEGES on *.* To 'hive'@'localhost' IDENTIFIED BY 'hive';
> MariaDB [(none)]> GRANT ALL PRIVILEGES on *.* To 'hive'@'%' IDENTIFIED BY 'hive';
```

# ถ้าต้องการติดตั้ง Ranger สร้าง db hive และ user ranger บน mysql ไว้

```
> MariaDB [(none)]> CREATE DATABASE ranger;
> MariaDB [(none)]> CREATE USER 'ranger'@'nn01.irpc' IDENTIFIED BY 'ranger';
> MariaDB [(none)]> CREATE USER 'ranger'@'localhost' IDENTIFIED BY 'ranger';
> MariaDB [(none)]> CREATE USER 'ranger'@'%' IDENTIFIED BY 'ranger';
> MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'ranger'@'nn01.irpc' WITH GRANT OPTION;
> MariaDB [(none)]> GRANT ALL PRIVILEGES on *.* To 'ranger'@'localhost' IDENTIFIED BY 'ranger';
> MariaDB [(none)]> GRANT ALL PRIVILEGES on *.* To 'ranger'@'%' IDENTIFIED BY 'ranger';
> MariaDB [(none)]> FLUSH PRIVILEGES;
```

`- vim /etc/profile`

```
#แทรกบรรทัดนี้ท้ายสุด
export buildNumber=2.7.3.0.0
- source  /etc/profile
- ambari-server setup --jdbc-db=mysql --jdbc-driver=/usr/share/java/mysql-connector-java.jar  #make sure ว่ามี file นี้ถ้าไม่มีสามารถ downlaod จากเว็บทั่วไปได้
```

# Deploy Java ทำทุกเครื่อง

```
wget https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u222-b10/OpenJDK8U-jdk_x64_linux_hotspot_8u222b10.tar.gz
tar -zxvf OpenJDK8U-jdk_x64_linux_hotspot_8u222b10.tar.gz
chown -R root:root jdk8u222-b10/
chmod -R 755 jdk8u222-b10/
mv jdk8u222-b10/ /usr/local/
vim /etc/profile
export JAVA_HOME=/usr/local/jdk8u222-b10
export PATH=$JAVA_HOME/bin:$PATH
source  /etc/profile
```

# Ambari-server setup

```
[root@server2 ~]# ambari-server setup
Using python  /usr/bin/python
Setup ambari-server
Checking SELinux...
SELinux status is 'disabled'
Customize user account for ambari-server daemon [y/n] (n)? n
Adjusting ambari-server permissions and ownership...
Checking firewall status...
Checking JDK...
Do you want to change Oracle JDK [y/n] (n)? y
[1] Oracle JDK 1.8 + Java Cryptography Extension (JCE) Policy Files 8
[2] Custom JDK
==============================================================================
Enter choice (1): 2
WARNING: JDK must be installed on all hosts and JAVA_HOME must be valid on all hosts.
WARNING: JCE Policy files are required for configuring Kerberos security. If you plan to use Kerberos,please make sure JCE Unlimited Strength Jurisdiction Policy Files are valid on all hosts.
Path to JAVA_HOME: /usr/local/jdk8u222-b10/
Validating JDK on Ambari Server...done.
Check JDK version for Ambari Server...
JDK version found: 8
Minimum JDK version is 8 for Ambari. Skipping to setup different JDK for Ambari Server.
Checking GPL software agreement...
GPL License for LZO: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
Enable Ambari Server to download and install GPL Licensed LZO packages [y/n] (n)? y
Completing setup...
Configuring database...
Enter advanced database configuration [y/n] (n)? y
Configuring database...
==============================================================================
Choose one of the following options:
[1] - PostgreSQL (Embedded)	>> Default user/pass (ambari/bigdata)
[2] - Oracle
[3] - MySQL / MariaDB
[4] - PostgreSQL
[5] - Microsoft SQL Server (Tech Preview)
[6] - SQL Anywhere
[7] - BDB
==============================================================================
Enter choice (1): 3
Hostname (localhost): hostname or localhost
Port (3306):
Database name (ambari):
Username (ambari):
Enter Database Password (bigdata):
Re-enter password:
Configuring ambari database...
Should ambari use existing default jdbc /usr/share/java/mysql-connector-java.jar [y/n] (y)?
Configuring remote database connection properties...
WARNING: Before starting Ambari Server, you must run the following DDL directly from the database shell to create the schema: /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
Proceed with configuring remote database connection properties [y/n] (y)?
Extracting system views...
ambari-admin-2.7.3.0.139.jar
Enter choice (1): 3
Hostname (localhost): server2.softnix.co.th
Port (3306):
Database name (ambari):
Username (ambari):
Enter Database Password (bigdata):
Re-enter password:
Configuring ambari database...
Should ambari use existing default jdbc /usr/share/java/mysql-connector-java.jar [y/n] (y)?
Configuring remote database connection properties...
WARNING: Before starting Ambari Server, you must run the following DDL directly from the database shell to create the schema: /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
Proceed with configuring remote database connection properties [y/n] (y)?
Extracting system views...
ambari-admin-2.7.3.0.139.jar
....
Ambari repo file doesn't contain latest json url, skipping repoinfos modification
Adjusting ambari-server permissions and ownership...
Ambari Server 'setup' completed successfully.
==============================================================================
```

# ขั้นตอน import schema db ของ ambari

```
- mysql  -uroot -p
>use ambari
>source /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql;
```

# ส่ง start service ambari

`- ambari-server start`

# ขั้นตอนนี้จะทำหรือไม่ทำก็ได้  เพราะตอน Deploy ผ่าน ambari จะทำการติดตั้งให้

## ถ้ายังไม่ได้ลง ambari-agent

```
- wget  http://ro-bucharest-repo.bigstepcloud.com/hortonworks-repos/ambari/centos7/2.7.3.0/ambari/ambari-agent-2.7.3.0-139.x86_64.rpm
- yum install ambari-agent-2.7.3.0-139.x86_64.rpm
```

# แก้ปัญหาเรื่อง public_hostname

```
- vi /var/lib/ambari-agent/public_hostname.sh
#!/bin/sh
echo `hostname -f`

หลังจากนั้น chmod 755
- chmod 755  /var/lib/ambari-agent/public_hostname.sh

แก้ไข ไฟล์ /etc/ambari-agent/conf/ambari-agent.ini
ใน section ของ
[agent]
#เพิ่มบรรทัดนี้ลงไป
public_hostname_script=/var/lib/ambari-agent/public_hostname.sh
ใน section ของ
[server]
ระบุชื่อ hostname ให้ตรงกับ hostname -f
เช่น  hostname -f แล้วเอา output มาใส่ตรง hostname
hostname=server2.localhost

- ambari-agent restart
```


# ขั้นตอนการ run

```
http://192.168.1.81:8080/#/login
user:admin
pass:admin
เลือก launch install wizard
ตั้งชื่อ clustername
ลบ repo ออกให้หมดเหลือไว้เฉพาะ redhat7
เลือกเป็น Public Repo ที่ช่อง Base URL ระบุดังนี้
HDP-3.1 = http://172.17.45.16/repos/hortonworks-repos/HDP/centos7/3.1.0.0/
HDP-3.1-GPL  = http://172.17.45.16/repos/hortonworks-repos/HDP-GPL/centos7/3.1.0.0/
HDP-UTILS-1.1.0.22  = http://172.17.45.16/repos/hortonworks-repos/HDP-UTILS/centos7/1.1.0.22/
หลังจากนั้นกด Next


ที่หน้า Install options ระบุดังนี้
Target Hosts = server2.softnix.co.th
เลือก Provide your SSH Private Key to automatically register hosts
สร้าง ssh-keygen ที่ command แล้ว copy id_rsa ที่เป็น private key มาวางไว้ที่ช่อง ssh private key


# วิธีสร้าง authorized key ----------------------------#
เครื่องที่ 1 IP 192.168.10.93
- ssh-keygen -t rsa 
- ssh-copy-id -i ~/.ssh/id_rsa 192.168.10.94
- ssh root@192.168.10.94

เครื่องที่ 2 IP 192.168.10.94
- ssh-keygen -t rsa 
- ssh-copy-id -i ~/.ssh/id_rsa 192.168.10.93
- ssh root@192.168.10.93 
#-------------------------------------------------#


สร้าง authorized_keys แล้วเอา public key มาวางไว้ให้เรียบร้อย
- cd /root/.ssh/
- cat id_rsa  	>>> #แล้ว copy ไปวางไว้ที่หน้า ssh private key
#หลังจากนั้นกด Next
#หมายเหตุ ถ้าไม่สามารถติดตั้ง agent ได้ขึ้น error ไม่เจอ folder ambari_server ให้ทำการสร้างขึ้นมาด้วยคำสั่ง 
- mkdir -p /usr/lib/ambari-server/lib/ambari_server/
```

# แก้ปัญหาตอน deploy package แล้วไม่สามารถ yum install ได้ ให้ลองตรวจสอบ file ambari-hdp-1.repo ถ้าไม่มี URL or URL ผิด  ให้ทำตาม Step นี้  (ทำที่เครื่อง ambari server เครื่องเดียว)

```
- ambari-server stop
- mysql -uroot -p ambari
- select * from repo_definition;      >> เช็ค URL ว่าถูกหรือไม่ ถ้าไม่ถูกให้แก้ไข
ทำการ update URL ตามนี้
> update repo_definition set base_url="http://172.17.45.16/repos/hortonworks-repos/HDP/centos7/3.1.0.0/" where repo_name="HDP";
> update repo_definition set base_url="http://172.17.45.16/repos/hortonworks-repos/HDP-UTILS/centos7/1.1.0.22/" where repo_name="HDP-UTILS";
> update repo_definition set base_url="http://172.17.45.16/repos/hortonworks-repos/HDP-GPL/centos7/3.1.0.0/" where repo_name="HDP-GPL";
# Or insert new
> insert into repo_definition (id, repo_os_id, repo_name, repo_id, base_url, unique_repo)
values ('27', '9', 'HDP-GPL', 'HDP-GPL-3.1.0.0', 'http://172.17.45.16/repos/hortonworks-repos/HDP-GPL/centos7/3.1.0.0/', 0);

> 17:27 11/19/2021
- rm -rf /etc/yum.repos.d/ambari-hdp-1.repo   	>> ทำการลบ file ambari-hdp-1.repo ทุกเครื่อง
- yum clean all && yum makecache		>> ทุกเครื่อง
- ambari-server start 
-  ทำการ Run ติดตั้งใหม่ 
วิธีแก้ปัญหาจาก web https://www.jianshu.com/p/8e4ca48c156a
#-------------------------------------------------#
mkdir -p /usr/lib/ambari-server/lib/ambari_server/
mkdir -p /var/lib/ambari-agent/data
mkdir -p /usr/lib/ambari-server/lib/
mkdir -p /var/lib/ambari-agent/cache/stacks/HDP/3.0/services/SMARTSENSE/package/files/rpm
```


# Step Deploy hive

```
# add user hive on postgres
- CREATE DATABASE hive;
- CREATE USER hive WITH PASSWORD 'hive';
- GRANT ALL PRIVILEGES ON DATABASE hive TO hive;
# Change password user 
- ALTER USER user_name WITH PASSWORD 'new_password';
```


# แก้ปัญหา Ranger Start ไม่ขึ้น

```
cp mysql-connector-java-5.1.49.jar /var/lib/ambari-agent/tmp/mysql-connector-java.jar
chmod 775 /usr/hdp/current/ranger-admin/ews/ranger-admin-services.sh

Path schema mysql 
/var/lib/ambari-server/resources/stacks/HDP/2.1/services/HIVE/etc/
```


# แก้ปัญหา hive ไม่สามารถ create database

`sudo -u hdfs hdfs dfs -chmod 777 /warehouse/tablespace/external/hive`
