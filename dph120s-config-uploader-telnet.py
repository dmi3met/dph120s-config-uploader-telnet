import telnetlib
import datetime
import time
import re

ip_address = '172.16.0.100'
port = 6000
server_ip = '172.16.0.160'
username = 'admin'
password = 'admin'

tn = telnetlib.Telnet()


def t_read(value):
    return tn.read_until(value.encode('ascii'))


def cmd(value):
    return tn.write(value.encode('ascii') + b'\r\n')

tn.open(ip_address, port, timeout=5)

r = t_read('Login:')
cmd(username)
r = t_read('Password:')
cmd(password)
t_read('# ')  # successful login

cmd('show basic')
read = t_read('==\r\n# ')
r = read.decode('ascii')

mac_address = re.findall(r'..:..:..:..:..:..', r)[0]
mac_with_minus = re.sub(':', '-', mac_address)
print(mac_address)


cmd('download tftp -ip '+server_ip+' -file '+mac_with_minus+'.txt')
today = datetime.datetime.today()
with open('config-uploader-log.txt', 'a') as file:
    now = today.strftime("%d.%m.%Y %H:%M:%S")
    file.write(now+' >> '+mac_address.upper()+'\n')

cmd('exit')

time.sleep(1)
tn.close()
