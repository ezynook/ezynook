# Install Ansible And Used
<hr>

```
yum install epel-release -y
yum install ansible -y
cd /etc/ansible
```
## ตั้งค่า Hosts ทั้งหมดในการจัดการ
> `vim /etc/ansible/hosts`
```bash
#ชื่อฟาล์ม (สามารถมีได้หลายตัวใน Ansible เดียว)
[bigdata]
192.168.10.10
192.168.10.11
192.168.10.12
192.168.10.13

#กำหนด Username, Password ในการ Login (ควรจะใช้เหมือนกันในฟาล์ม)
[bigdata:vars]
ansible_user=root
ansible_password=admin
```
## แก้ไขไฟล์ ansible.cfg
> `vim ansible.cfg`
```bash
เอา # ด้านหน้าออก
[default]
#host_key_checking = False
```
## หลังจากนั้นทำการทดสอบว่าสามารถติดตั้ง Host ทั้งหมดได้หรือไม่โดยใช้คำสั่ง
> `ansible bigdata -m ping`
* ถ้าใช้งานได้จะขึ้นมาประมาณนี้
```py
192.168.10.43 | SUCCESS => {
"ansible_facts": {
"discovered_interpreter_python": "/usr/bin/python"
},
"changed": false,
"ping": "pong"
}
192.168.10.42 | SUCCESS => {
"ansible_facts": {
"discovered_interpreter_python": "/usr/bin/python"
},
"changed": false,
"ping": "pong"
}
```
## ทำการสร้าง YMAL เพื่อกำหนดค่าการ Deploy
[Ansible Syntax And Tutorial](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html)
> `vim /etc/ansible/bigdata.yml`

* กำหนดชื่อดังนี้
	- name: ชื่อ service
	- hosts: ชื่อฟาร์มที่ได้ตั้งไว้ตอน /etc/ansible/hosts
```bash
- name: service_name
  hosts: host_farm
  tasks:
```
* ตัวอย่างการติดตั้ง Package Yum install
```bash
  - name: install_httpd
    ansible.builtin.yum:
      name: httpd
      state: latest
```
* ตัวอย่างการ Copy File ไปยังเครื่องต่างๆ
```bash
  - name: copy_file
    ansible.builtin.copy:
      src: /etc/yum.repos.d/cloudera.repo
      dest: /etc/yum.repos.d/cloudera.repo
      mode: '0644'
```
* ตัวอย่างการใช้กับ pip install
```bash
  - name: pip_install
    ansible.builtin.pip:
      name:
        - pandas
        - sqlalchemy
```
* ตัวอย่างการโหลดไฟล์จาก URL
```bash
  - name: download_miniconda
    ansible.builtin.get_url:
      url: https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
      dest: /root/Miniconda3-latest-Linux-x86_64.sh
      mode: '0777'
```
* วิธีการ Run คำสั่ง
```sh
ansible-playbook bigdata.yml
```
## ตรวจสอบการทำงาน
* หากใช้งานได้ปกติจะแสดงหน้าจอนี้
	> ok=2 (ใช้งานได้ปกติ) <br>
	> changed=1 (ทำการเปลี่ยนค่าหรือติดตั้งตามคำสั่ง YAML เป็นครั้งแรก)<br>
	> changed=0 (ใช้งานได้แต่ไม่มีการเปลี่ยนค่า หากมีการรันเป็นครั้งที่ 2 หาก Package นั้นๆ มีอยู่แล้ว)<br>
```sh
PLAY [CopyFile] **********************************************************************

TASK [Gathering Facts] ***************************************************************
ok: [192.168.10.43]
ok: [192.168.10.42]

TASK [cp_to_tmp] *********************************************************************
changed: [192.168.10.43]
changed: [192.168.10.42]

PLAY RECAP ***************************************************************************
192.168.10.42              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.10.43              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
> Author: `Pasit Y. Data Engineer @Softnix.Co.Ltd`