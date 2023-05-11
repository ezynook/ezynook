# Step Install Ubuntu

## Install Java

```
#Ubuntu
sudo apt-get update
sudo apt-get install openjdk-11-jdk-headless \
	             openjdk-11-jre-headless \
	             openjdk-11-jre
#CentOS
sudo yum install java-11-openjdk-devel \
		 java-11-openjdk \
		 java-1.8.0-openjdk-devel \
		 java-1.8.0-openjdk
```

## Download And Config Path

```
wget "https://repo1.maven.org/maven2/io/trino/trino-server/352/trino-server-352.tar.gz"
tar -xzvf trino-server-352.tar.gz
sudo mv trino-server-352 /home/trino
sudo chown $$USER:$$USER /home/trino
export TRINO_HOME=/home/trino
export PATH=$$PATH:$$TRINO_HOME/bin
mkdir -p /home/trino/etc/catalog
touch etc/node.properties
touch etc/jvm.config
touch etc/config.properties
touch etc/log.properties
touch etc/catalog/hive.properties
```

> `vim etc/node.properties`

```
node.environment=production
node.id=ffffffff-ffff-ffff-ffff-ffffffffffff #uuidgen
node.data-dir=/home/trino/data
```

> `vim etc/jvm.config`

```
-server
-Xmx16G #Available host
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+UseGCOverheadLimit
-XX:+ExplicitGCInvokesConcurrent
-XX:+HeapDumpOnOutOfMemoryError
-XX:+ExitOnOutOfMemoryError
-Djdk.attach.allowAttachSelf=true
```

> `vim etc/config.properties`

```
#Stand-Alone Config
coordinator=true
node-scheduler.include-coordinator=true
http-server.http.port=8080
query.max-memory=5GB
query.max-memory-per-node=1GB
discovery-server.enabled=true
discovery.uri=http://192.168.10.40:8080
#Worker
coordinator=true
node-scheduler.include-coordinator=false
http-server.http.port=8080
discovery.uri=http://192.168.10.40:8080
```

> `vim etc/log.properties`

`io.trino=DEBUG (DEBUG, INFO, WARN and ERROR)`

> `vim etc/jmx.properties`

`connector.name=jmx`

## Set Default Java Home

```
sudo update-java-alternatives --list
sudo update-alternatives --config java (Choose 11)
sudo  update-alternatives --config javac (Choose 11)
```

## Command to Use

`./bin/launcher run, start, status, stop`

## How to Set Path Custom Java Home

```
PATH=/home/presto/jdk17/bin:$PATH /home/presto/bin/launcher start
PATH=/home/presto/jdk17/bin:$PATH /home/presto/bin/launcher restart
PATH=/home/presto/jdk17/bin:$PATH /home/presto/bin/launcher run
```

---

## How to Setup Keystore (SSL) For Trino

```
keytool -genkeypair -alias trino_keystore -validity 3650 -keyalg RSA -dname "CN=192.168.10.226,OU=Unknown,O=Unknown,L=Unknown,S=Unknown,C=Unknown" -ext SAN=IP:192.168.10.226 -keypass admin123 -keystore /home/trino-server-364/etc/trino_keystore.jks -storepass admin123 -storetype JKS
```

> OR

```
keytool -genkeypair -alias trino_keystore -validity 3650 -keyalg RSA -dname "CN=masternode.bigdata,OU=Unknown,O=Unknown,L=Unknown,S=Unknown,C=Unknown" -ext SAN="DNS:masternode.bigdata,IP:127.0.0.1,IP:172.16.23.200,IP:47.254.255.244" -keypass admin123 -keystore /home/trino-server-364/etc/trino_keystore.jks -storepass admin123 -storetype JKS
```

## Import to JDK

```
keytool -importkeystore -srckeystore /home/trino/etc/trino_keystore.jks -destkeystore /home/trino/etc/trino_keystore.jks -deststoretype pkcs12
```

```
keytool -exportcert -keystore /home/trino/etc/trino_keystore.jks  -alias trino_keystore  -file /home/trino/etc/trino_certificate.cer
```

```
keytool -import -alias trino_trust -keystore /home/trino/jdk-11.0.12/lib/security/cacerts -file /home/trino/etc/trino_certificate.cer -trustcacerts
```

## หากเกิด Error ในขั้นตอนนี้ให้ใส่รหัสผ่านดังนี้

`password = changeit`

## ตรวจสอบดูว่ามีรายการที่ได้ Add ไปหรือไม่ด้วยคำสั่งนี้

`keytool -list -v -keystore /home/trino/etc/trino_keystore.jks`

---

## หากต้องการ Authentication ด้วย Dbeaver

#### สร้าง htpasswd

```
htpasswd -B -C 10 htaccess username
create role user_group
grant user_group to user username
```

## Dbeaver ให้ใส่ Parameter ดังนี้

* [X] SSH = True
`SSLKeyStorePassword = admin123`
`SSLKeyStorePath = C:\Data\trino_Keystore.jks #ไฟล์ Trino Key Store`