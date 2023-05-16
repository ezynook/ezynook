## 🛠 วิธี Build Docker Pasit style 😄
---
เลือก Base Image ที่ต้องการเช่น Alpine, Debian, Ubuntu
โดยใช้วิธีการ Run แบบ Interactive ในตัวอย่างนี้จะเลือกใช้เป็น ```debian:11```
```bash
docker run -itd --name service_name -d debian:11 
```
หลังจากนั้นให้เข้าไปยัง Docker โดยวิธีการ exec 
เข้าไปแล้วทำการ Install Package ที่ต้องการให้เรียบร้อย:
```bash
docker exec -it service_name /bin/bash
```
หลังจากที่ได้ทำการติดตั้งและลง Package ที่ต้องการเสร็จให้ทำการสร้าง ```docker-entrypoint.sh```
เพื่อให้เป็น ```Command``` หลังจากที่ได้ทำการ Running Container ซึ่ง container มีความจำเป็นต้อง
ใช้ realtime logs เพื่อให้ Docker ทำงานต่อได้โดยใช้คำสั่ง Shell Script
> สร้าง ```docker-entrypoint.sh``` ให้นำไปไว้ที่ /usr/local/bin
```bash
cd /usr/local/bin
vim docker-entrypoint
```

> รูปแบบที่ 1 ให้ Infinity Loop เพื่อตรวจสอบให้ตรง Interval ตาม Sleep ที่ได้ตั้งค่าไว้
```bash
#!/bin/bash

_init(){
	if [ -z "$(netstat -lnpt | grep 3306)" ]; then
		service mariadb start > dev/null
		echo "Mariadb is Starting...."
	else
		echo "MariaDB is Started"
	fi
}
#keep docker running with Loop
while true; do
	_init
	sleep 3
done
```
> รูปแบบที่ 2 ใช้วิธีการ Start Service ที่ต้องการให้ครบถ้วนตามลำดับแล้วใช้ tail -f ในการคงสภาพการทำงาน
```bash
#!/bin/bash

_INIT=$(netstat -lnpt | grep 3306)

if [ -z "$_INIT" ]; then
	service mariadb start > /dev/null
	echo "Mariadb is Starting..."
else
	echo "Mariadb is Started"
fi
sleep 5
#keep docker is running
tail -f /dev/null
```
เปิดสิทธิ execution file
```bash
chmod +x /usr/local/bin/docker-entrypoint
```
ออกจาก container โดยใช้คำสั่ง ```exit``` หลังจากนั้นทำการพิมพ์คำสั่ง ```docker ps``` เพื่อตรวจสอบ ```container id``` จากนั้น copy ไว้ หลังจากนั้น ```Run``` คำสั่ง ```commit``` เพื่อบันทึก ```container``` ไปเป็น ```images``` ชุดใหม่ โดยใช้คำสั่ง:
```bash
docker commit <container_id> rawimage:latest
```
สร้าง ```Dockerfile``` เพื่อนำ ```images``` ก่อนหน้าที่ได้ทำการ ```commit``` มาจัดการสั่ง ```command``` ให้ ```start docker entrypoint``` อัตโนมัติหลังจากทำการ ```run container``` โดยใช้คำสั่ง:
```bash
vim Dockerfile
```
```dockerfile
FROM rawimage:latest
MAINTAINER pasit.dev

#คำสั่งในการเช็ค Container หลังจากรันแล้วว่าการทำงานถูกต้องหรือไม่โดย 
#State จะมีดังนี้ ['healthy', 'unhealthy', 'exited']
HEALTHCHECK --interval=5s --timeout=3s --retries=1 CMD <Any linux command to check > || exit 1

#หากนำ shellscript ที่เขียนไว้ไปวางใน /usr/local/bin ไม่จำเป็นต้องเรียก path
#หากไปวางไว้ที่ path อื่นๆ มีความจำเป็นต้องระบุเช่น /root/docker-entrypoint
ENTRYPOINT [ "docker-entrypoint" ]
```
บันทึก Dockerfile แล้วทำการ Build เป็น Image ชุดใหม่ โดยใช้คำสั่ง:
```bash
docker build -t new_image_name:tag_name .
```
หลังจากนั้นก็ทำการ Run คำสั่งตามปกติโดยวิธีมี 2 วิธี
> วิธีที่ 1 Docker run syntax
```bash
docker run --name service_name \
-p 80:80 -p 3306:3306 \
--restart=always \
-d new_image_name:tag_name
```
> วิธีที่ 2 docker-compose.yml
```yaml
version: '3'
services:
  service_name:
    image: new_image_name:tag_name
    container_name: service_name
    ports:
      - 80:80
      - 3306:3306
    volumes:
      - volume_data:/var/lib/mysql
    restart: always

    #หากทำ Healthy Check ใน Dockerfile แล้วไม่จำเป็นต้องใช้คำสั่งนี้
    healthcheck:
      test: <Any linux command to Check> || exit 1
      interval: 15s
      retries: 3
      start_period: 10s
      timeout: 10s

volumes:
  volume_data:
```
สั่ง run ```docker-compose.yml```
```bash
docker-compose up -d
```
---
## 🛳 วิธีการ Push ขึ้น Public Registry
> ### Docker Hub
ใช้คำสั่งเพื่อดูรายการ Images:
```bash
docker images
```
จากนั้นทำการเปลี่ยนชื่อ image ที่ต้องการ push ขึ้นไปตาม pattern ของ ```Docker Hub```
```bash
docker tag <image id> docker_hub_username/imagename:tagname
#ตัวอย่าง
#docker tag 7ca7a3e1fa9d ezynook/mysql:5.7
```
ทำการ Login ไปยัง docker.com
```bash
docker login
#Username: Your Username
#Password: Your Password
```
ขึ้นตอนสุดท้ายทำการ Push
```bash
docker push docker_hub_username/imagename:tagname
```
> ### Github Registry
ใช้คำสั่งเพื่อดูรายการ Images:
```bash
docker images
```
จากนั้นทำการเปลี่ยนชื่อ image ที่ต้องการ push ขึ้นไปตาม pattern ของ ```GitHub```
```bash
docker tag <image id> ghcr.io/username/repository/imagename:tagname
#ตัวอย่าง
#docker tag 7ca7a3e1fa9d ezynook/mysql:5.7
```
ทำการ Login ไปยัง github.com
* Personal token key Generate [Link to Token](https://github.com/settings/tokens)
```bash
docker login
#Username: Your Username
#Password: Personal token key
```
ขึ้นตอนสุดท้ายทำการ Push
```bash
docker push ghcr.io/username/repository/imagename:tagname
```
> ### Gitlab Registry
```bash
docker push docker_hub_username/imagename:tagname
```
> ### Github Registry
ใช้คำสั่งเพื่อดูรายการ Images:
```bash
docker images
```
จากนั้นทำการเปลี่ยนชื่อ image ที่ต้องการ push ขึ้นไปตาม pattern ของ ```Gitlab```
```bash
docker tag <image id> registry.gitlab.com/username/imagename:tagname
#ตัวอย่าง
#docker tag 7ca7a3e1fa9d ezynook/mysql:5.7
```
ทำการ Login ไปยัง gitlab.com
* Personal token key Generate [Link to Token](https://gitlab.com/-/profile/personal_access_tokens)
```bash
docker login
#Username: Your Username
#Password: Personal token key
```
ขึ้นตอนสุดท้ายทำการ Push
```bash
docker push registry.gitlab.com/username/imagename:tagname
```
---
Develope by | ```Pasit Yodsoi (pasit.dev)``` ©
