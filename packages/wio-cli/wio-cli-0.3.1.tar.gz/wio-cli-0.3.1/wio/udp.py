# Send UDP broadcast packets
import socket
import re

PORT = 1025
IP = "192.168.4.1"
cmd = "SCAN"
addr = (IP, PORT)

def udp_list():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(1)
    ssid_list = []
    flag = False
    for i in range(3):
        s.sendto('SCAN', addr)
        try:
            while 1:
                data, a = s.recvfrom(1024)
                ssid = data
                if ssid in '\r\n':
                    flag = True
                    break
                ssid = ssid.strip('\r\n')
                ssid_list.append(ssid)
        except socket.timeout:
            continue
        except:
            break
            
        if flag:
            break
    s.close()

    if flag:
        return ssid_list
    else:
        return None

def udp_version():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(1)
    version = 1.1
    flag = False
    for i in range(3):
        s.sendto('VERSION', addr)
        try:
            while 1:
                data, a = s.recvfrom(1024)
                flag = True
                break
        except socket.timeout:
            continue
        except:
            break

        if flag:
            break
    s.close()

    if flag:
        try:
            version = float(re.match(r"([0-9]+.[0-9]+)", data).group(0))
        except Exception as e:
            version = 1.1
        return version
    else:
        return version
    
def udp_debug():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(1)
    flag = False
    for i in range(3):
        s.sendto('DEBUG', addr)
        try:
            while 1:
                data, a = s.recvfrom(1024)
                flag = True
                break
        except socket.timeout:
            continue
        except:
            break

        if flag:
            break
    s.close()

    if flag:
        try:
            debug = re.match(r"([0-9])", data).group(0)
            return debug
        except Exception as e:
            raise e
    
    return flag
    
def send(cmd):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(1)
    flag = False
    for i in range(3):
        try:
            s.sendto(cmd, addr)
            while 1:
                data, a = s.recvfrom(1024)
                if 'ok' in data:
                    flag = True
                    break
        except socket.timeout:
            continue
        except:
            break

        if flag:
            break
    s.close()

    return flag

# print udp_list()
