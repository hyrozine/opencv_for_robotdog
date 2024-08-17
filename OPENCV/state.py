from utils import COLOR, STATE, LEFT, RIGHT, STRAIGHT
from color_detect import detect_blue_upstair, detect_red_divpath, detect_user, detect_orange_end
from ball_detect import detect_ball
from line_detect import line_track
from uart import my_uart


# import sensor
# import pyb
# from pyb import Pin, Timer, LED


 # light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))


class State_Machine():
    def __init__(self):
        self.state = STATE['state_1_out']
        #self.state = STATE['state_3_yellow_climb']
        self.ball_time = 0
        self.now_time = 0
        self.blue_time = 0
        self.ball_user = 0
        self.FLAG_BALL_TYPE = { 'PRUPLE': False, 'BROWN': False}
        self.lane_flag = 0

    def state_machine_exe(self, frame):
        #print("now:",self.state)

        if self.state == STATE['state_1_out']:
            # if self.find_ball(frame) is True:
            #     if self.FLAG_BALL_TYPE['BROWN'] == True:
            #         self.ball_user = 1
            #     elif self.FLAG_BALL_TYPE['PRUPLE'] == True:
            #         self.ball_user = 2  
            #     my_uart.send_data()
            # else:
            line_track(frame)
            my_uart.send_data()
            my_uart.clear_data()
            self.state_trans(STATE['state_2_obstacle'])

        elif self.state == STATE['state_2_obstacle']:
            if self.find_blue_upstair(frame) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_3_upstair'])
            else:
                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()

        elif self.state == STATE['state_3_upstair']:
            self.state_trans(STATE['state_4_downstair'])
            my_uart.clear_data()
        elif self.state == STATE['state_4_downstair']:
            if self.find_red_divpath(frame) is True :
                my_uart.send_data()
                self.state_trans(STATE['state_5_user1'])
                self.state_trans(STATE['state_5_user2'])
            else:
                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()
        elif self.state == STATE['state_5_user1']:
            if self.find_user(frame, self.ball_user):
                #my_uart.set_data(1, 'isOpen')
                my_uart.send_data()
            else:
                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()
        elif self.state == STATE['state_5_user2']:
            if self.find_user(frame, self.ball_user):
                #my_uart.set_data(1, 'isOpen')
                my_uart.send_data()
            else:
                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()
        elif self.state == STATE['state_6_backhome']:
            if self.find_orange_end(frame, 2) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_1_out'])
                #light.pulse_width_percent(10)  # 控制亮度 0~100完成
            else:
                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()
        else:
            pass

    def state_trans(self, st):
        N = 20
        if st == STATE['state_1_out']:
            for i in range(N):
                info = my_uart.receive_data()
                if '1' in info:
                    self.state = st  # 状态转移成功
                    print("out")
                    break
        elif st == STATE['state_2_obstacle']:
            for i in range(N):
                info = my_uart.receive_data()
                if '2' in info:
                    self.state = st  # 状态转移成功
                    print('upstair')
                    # self.blue_time = pyb.millis() # TODO: 
                    break
        elif st == STATE['state_3_upstair']:
            for i in range(N):
                info = my_uart.receive_data()
                if '3' in info:
                    self.state = st  # 状态转移成功
                    print('downstair')
                    break
        elif st == STATE['state_4_downstair']:
            for i in range(N):
                info = my_uart.receive_data()
                if '4' in info:
                    self.state = st  # 状态转移成功
                    print('near user')
                    break
        elif st == STATE['state_5_user1']:
            for i in range(N):
                info = my_uart.receive_data()
                if '5' in info:
                    self.state = st
                    print('user1 has been found!')
                    break
        elif st == STATE['state_5_user2']:
            for i in range(N):
                info = my_uart.receive_data()
                if '5' in info:
                    self.state = st
                    print('user2 has been found!')
                    break
        elif st == STATE['state_6_backhome']:
            for i in range(N):
                info = my_uart.receive_data()
                if '6' in info:
                    self.state = st
                    print('TO THE END!')
                    break
        else:
            pass
        print("now:",self.state)

    

    def find_ball(self, img):
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
