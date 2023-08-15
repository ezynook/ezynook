data = {
    'admin':'admin',
    'nook':'nook'
}

username = "admin"
password = "nook"
if username in data and password in data[username]:
    print('yes')
else:
    print('no')