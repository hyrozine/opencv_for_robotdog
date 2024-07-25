import cv2
from utils import COLOR, STATE

"""
    状态机
"""
from color_detect import detect_blue_upstair, detect_red_divpath, detect_user, detect_orange_end
from ball_detect import detect_ball
from line_detect import line_track
from uart import my_uart
from utils import COLOR, STATE, LEFT, RIGHT, STRAIGHT

import pyserial

# import sensor
# import pyb
# from pyb import Pin, Timer, LED

yellow_time = 0

FLAG_BALL_TYPE = { 'PRUPLE': False, 'BROWN': False}

light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))


class State_Machine():
    def __init__(self):
        self.state = STATE['state_1_recognize_ball']
        #self.state = STATE['state_3_yellow_climb']
        self.ball_time = 0
        self.now_time = 0
        self.blue_time = 0

    def state_machine_exe(self, frame):
        #print("now:",self.state)

        
        if self.state == STATE['state_1_recognize_ball']:
            if self.find_ball(frame) is True:  
                my_uart.send_data()
                self.state_trans(STATE['state_2_blue_climb'])
            else:
                my_uart.set_data(RIGHT, 'direction')
                my_uart.set_data(45, 'angle')
                my_uart.send_data()
            my_uart.clear_data()

        elif self.state == STATE['state_2_blue_climb']:
            if self.find_blue_upstair(frame) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_3_red_turn'])
            else:
                line_track(frame.copy(), err=1, type='grass', angle_limit=30)

                light.pulse_width_percent(18)

                my_uart.send_data()
            my_uart.clear_data()

        elif self.state == STATE['state_3_red_turn']:
            if self.find_red_divpath(frame) is True :
                my_uart.send_data()
                self.state_trans(STATE['state_4_user'])
            else:
                light.pulse_width_percent(18)

                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()
        elif self.state == STATE['state_4_user']:
            if self.find_user(frame, )
            self.state_trans(STATE['state_6_grass'])
        elif self.state == STATE['state_5_user2']:
            if self.find_user(img, 2) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_7_user3'])
                #light.pulse_width_percent(10)  # 控制亮度 0~100完成
            else:
                self.now_time = pyb.millis()
                if self.now_time - self.yellow_time < 81000:
                    my_line.line_track(img.copy())
                    my_line.line_track(img.copy(), err=1, type='grass', angle_limit=30)
                elif self.now_time - self.yellow_time < 105000:
                    print("过环岛")
                    #light.pulse_width_percent(0)
                    #light.pulse_width_percent(3)
                    #my_uart.set_data(1, 'isOpen')
                    my_line.line_track(img.copy(), err=1, angle_limit=30)
                else:
                    #my_uart.set_data(2, 'isOpen')
                    #my_line.line_track(img.copy(), err=1, type='grass')
                    my_line.line_track(img.copy(), err=1, type='grass', angle_limit=30)
                my_uart.send_data()
            my_uart.clear_data()
            """ 到达草地 """
        elif self.state == STATE['state_6_grass']:
            if self.find_grass(img) is True:
                my_uart.send_data()
                light.pulse_width_percent(18)
                self.state_trans(STATE['state_2_user1'])
            else:
                my_line.line_track(img.copy(), err=1, type='grass', angle_limit=30)
                my_uart.send_data()
            my_uart.clear_data()
            """ 到达用户3区域 """
        elif self.state == STATE['state_7_user3']:
            if self.find_user(img, 3) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_1_begin'])
                #light.pulse_width_percent(10)  # 控制亮度 0~100
            else:
                #if detect_grass(img) is True:
                    #my_line.line_track_grass(img.copy())
                #else:
                    #my_line.line_track(img.copy(), type='grass', err=1)
                my_line.line_track(img.copy(), err=1, type='grass', angle_limit=30)
                my_uart.send_data()
            my_uart.clear_data()
        else:
            pass

    def state_trans(self, st):
        N = 20
        if st == STATE['state_1_recognize_ball']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '1' in info:
                    self.state = st  # 状态转移成功
                    print("recieved ball")
                    break
        elif st == STATE['state_2_turn_out']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '2' in info:
                    self.state = st  # 状态转移成功
                    print('turning out success')
                    # self.blue_time = pyb.millis() # TODO: 
                    break
        elif st == STATE['state_3_blue_climb']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '3' in info:
                    self.state = st  # 状态转移成功
                    print('upstairs!!!')
                    break
        elif st == STATE['state_4_red_turn']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '4' in info:
                    self.state = st  # 状态转移成功
                    print('near roundabout')
                    break
        elif st == STATE['state_5_orage_end']:
            for i in range(N):
                info = my_uart.reveive_data()
                if '5' in info:
                    self.state = st
                    print('turn in!')
                    break
        else:
            pass
        print("now:",self.state)

    

    def find_ball(self, img):
        self.FLAG_BALL_TYPE = { 'PRUPLE': False, 'BROWN': False}
        self.FLAG_BALL_TYPE['PRUPLE'] = detect_ball(img, 'PRUPLE')
        self.FLAG_BALL_TYPE['BROWN'] = detect_ball(img, 'BROWN')
        
        if  self.FLAG_BALL_TYPE['PRUPLE'] is True or self.FLAG_BALL_TYPE['BROWN'] is True:
            my_uart.set_data(1, 'ball')  # 检测到球
            if self.FLAG_BALL_TYPE['PRUPLE'] is True:
                my_uart.set_data(COLOR['PRUPLE'], 'color')
                print("找到紫球")
            elif self.FLAG_BALL_TYPE['BROWN'] is True:
                my_uart.set_data(COLOR['BROWN'], 'color')
                print("找到棕球")
            return True
        else:
            my_uart.set_data(0, 'ball')
            # my_uart.set_data(COLOR['BLACK'], 'color')
            return False

    def find_user(self, img, id: int):
     
        id_list = { '1': 'BROWN', '2': 'PRUPLE'}
        FLAG_USER = detect_user(img, id)
        if FLAG_USER is not True:
            return False
        my_uart.set_data(COLOR[id_list[str(id)]], 'color')  
        print('到达用户' + str(id) + '区域')
        return True

    def find_blue_upstair(self, img):
        
        FLAG_BLUE = detect_blue_upstair(img)
        if FLAG_BLUE is not True:
            return False
        
        print("到达台阶")
        my_uart.set_data(COLOR['BLUE'], 'color')
        return True
    
    def find_red_divpath(self, img):
        
        FLAG_RED = detect_red_divpath(img)
        if FLAG_RED is not True:
            return False
        
        print("to the roundabout")
        my_uart.set_data(COLOR['RED'], 'color')
        return True

    def find_orange_end(self, img):
        
        FLAG_ORANGE = detect_orange_end(img)
        if FLAG_ORANGE is not True:
            return False
        
        print("TO THE END")
        my_uart.set_data(COLOR['ORANGE'], 'color')
        return True

state_machine = State_Machine()
