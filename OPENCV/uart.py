import serial 

class Uart:
    def __init__(self):
        self.port = '/dev/ttyUSB1'
        self.baud = 115200
        self.timeout = 1
        self.port = serial.Serial(self.port, self.baud, timeout = self.timeout)
        self.port.close()
        if not self.port.is_open():
            self.port.open()
        self.datasets = {'header1': 100, 'header2': 8, 'color': 0, 'direction': 0, 'angle': 0, 'isOpen': 0, 'ball': 0, 'end': 101}

    def port_close(self):
        self.port.close()

    def set_data(self, data_value, data_position):
        self.datasets[data_position] = data_value

    def send_data(self):
        allData = []
        # for 遍历字典 append 顺序会乱
        allData.append(self.datasets['header1'])
        allData.append(self.datasets['header2'])
        allData.append(self.datasets['color'])
        allData.append(self.datasets['direction'])
        allData.append(self.datasets['angle'])
        allData.append(self.datasets['isOpen'])
        allData.append(self.datasets['ball'])
        allData.append(self.datasets['end'])
        datas = bytearray(allData)
        self.port.write(datas)

    def recieve_data(self):
        info = '0'
        info = self.port.readline()
        print(info)
        return info
    
    def clear_data(self):
        self.datasets['color'] = 0
        self.datasets['direction'] = 0
        self.datasets['angle'] = 0
        self.datasets['isOpen'] = 0
        self.datasets['ball'] = 0
    
my_uart = Uart()