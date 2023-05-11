# วิธีการทำ PasswordLess SSHKey
## SSH Ket Generate
```sh
ssh-keygen -t rsa -b 4096 -C "nook@email.com"
```
## Copy SSH ID to Another Host on Cluster
> `ssh-copy-id root@ip_address` <br>
## OR
> `cat ~/.ssh/id_rsa.pub | ssh root@ip_address "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"`

<br>

>Author: `Pasit Y. Data Engineer @Softnix.Co.Ltd`
