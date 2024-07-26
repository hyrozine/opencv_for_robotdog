import serial 
import threading
import time

import serial.tools
import serial.tools.list_ports

class Uart:
    def __init__(self):
        self.port = '/dev/ttyUSB0'
        self.baud = 115200
        self.timeout = 0.1
        self.port = serial.Serial(self.port, self.baud, timeout = self.timeout)
        if not self.port.is_open:
            self.port.open()

    def scan_all_ports():
        TTY_list = []
        ports_list = serial.tools.list_ports.comports()
        if len(ports_list) <= 0:
            print("no port detected")
        else:
            print("ports available: ")
            for comfort in ports_list:
                TTY_num = list(comfort)[0]
                print(TTY_num, "  /  ", list(comfort)[1])
                TTY_list.append(TTY_num)
        return TTY_list

    def send_data(self):
        while(1):
            self.port.write(str(time.time).encode('utf-8'))

    def recieve_data(self):
       while(1):
           msg = self.port.readline()
           if (len(msg)>0):
               print('timenow:'+str(msg).decode())
    

    

if __name__ == '__main__':
    my_uart = Uart()
    t1 = threading.Thread(target=my_uart.send_data())
    t1.start()
    t2 = threading.Thread(target=my_uart.recieve_data())
    t2.start()
    