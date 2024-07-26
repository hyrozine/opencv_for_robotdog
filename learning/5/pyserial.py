import serial 
import threading
import time

class Uart:
    def __init__(self):
        self.port = '/dev/ttyUSB1'
        self.baud = 115200
        self.timeout = 1
        self.port = serial.Serial(self.port, self.baud, timeout = self.timeout)
        self.port.close()
        if not self.port.is_open():
            self.port.open()


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
    