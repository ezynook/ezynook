## Step Install PM2

```
#Ubuntu
sudo apt-get install curl 
curl -sL https://deb.nodesource.com/setup_17.x | sudo -E bash - 
sudo apt-get install nodejs 
#CentOS
yum install -y gcc-c++ make 
curl -sL https://rpm.nodesource.com/setup_16.x | sudo -E bash - 
sudo yum install nodejs 
```

# Install PM2

```
npm install -g pm2
env PATH=$PATH:/usr/local/bin pm2 startup -u root
adduser admin
passwd admin
usermod -aG sudo admin
```

# วิธีใช้

```
pm2 list -> แสดงรายการ task ทั้งหมด
pm2 info id -> แสดงรายละเอียดของ task
pm2 start --name "taskname" "/path/filename.sh" -u username / cd /home/user/ -> pm2 start xxx.sh
pm2 save -> สั่งให้ save
pm2 startup -> enable on boot
```
