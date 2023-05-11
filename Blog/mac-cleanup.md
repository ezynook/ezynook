# Mac-Cleanup (Using Bash)
## How to Install
```sh
curl -o cleanup https://raw.githubusercontent.com/mac-cleanup/mac-cleanup-sh/main/mac-cleanup
chmod +x cleanup
sudo mv cleanup /usr/local/bin/cleanup
```
## How to Running Script Cleanup
```cleanup``` OR ```mac-cleanup```

---
# Mac-Cleanup (Using Python)
## How to Install
### Using Home Brew
```bash
brew tap mac-cleanup/mac-cleanup-py
brew install mac-cleanup-py 
```
### Using PIP
```py
pip3 install mac-cleanup
```
### Usage Options
```bash
$ mac-cleanup -h

usage: mac-cleanup [-h] [-d] [-u] [-c] [-m]

    A Mac Cleanup Utility in Python
    v2.2.5
    https://github.com/mac-cleanup/mac-cleanup-py

optional arguments:
  -h, --help       show this help message and exit
  -d, --dry-run    Shows approx space to be cleaned
  -u, --update     Script will update brew while cleaning
  -c, --configure  Launch modules configuration
  -m, --modules    Specify custom modules' path
```