# Basic Config
```bash
- Disable Selinux
- Disable Firewall
- Add Repo /etc/yum.d.repo
- ./cloudera-manager-installer.bin --skip_repo_package=1 #ข้าม Online Repos
```
# การติดตั้ง Cloudera

```
- Copy repos ไปวางไว้ที่ /etc/yum.repos/d (ที่เหลือลบหมดให้เลือกแค่ CentOS-Base.repo)
- ตั้ง /etc/hosts ให้เป็น IPAddress	hostname
- แลก SSH-Key ให้ครบทุกเคื่อง
- Copy File Setup cloudera-manager-installer-6.3.1.bin ไปไว้ที่ /root
- chmod +x cloudera-manager-installer-6.3.1.bin
- cloudera-manager-installer-6.3.1.bin --skip_repo_package=1
- หลังจากติดตั้งเสร็จ รอให้ Port Up สักครู่จากนั้นเข้า http://ipaddress:7180
- เลือกเป็น Free Version
- Setting Repo
	- ตัวแรก -> http://192.168.10.14/repos/cdh6/cdh6/6.3.2/ (ใน repos ต้องมี allket.asc)
	- ตัวที่ 2 -> http://192.168.10.14/repos/cloudera-cdh6-parcels/
```
