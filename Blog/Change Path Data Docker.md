## Stop Docker Service

`systemctl stop docker`

`vim /etc/docker/daemon.json`

## Add This Code

```
{
  "data-root": "/path/to/your/docker"
}
```

## Move and Remove Old Data

```
- rsync -aP /var/lib/docker/ /new/path
- rm -rf /var/lib/docker
```

## Start Service Docker

`systemctl start docker`
