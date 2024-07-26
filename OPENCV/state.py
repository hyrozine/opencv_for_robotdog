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
        self.state = STATE['state_1_recognize_ball']
        #self.state = STATE['state_3_yellow_climb']
        self.ball_time = 0
        self.now_time = 0
        self.blue_time = 0
        self.ball_user = 0
        self.FLAG_BALL_TYPE

    def state_machine_exe(self, frame):
        #print("now:",self.state)

        if self.state == STATE['state_1_recognize_ball']:
            if self.find_ball(frame) is True:
                if self.FLAG_BALL_TYPE['BROWN'] == True:
                    self.ball_user = 1
                elif self.FLAG_BALL_TYPE['PRUPLE'] == True:
                    self.ball_user = 2  
                my_uart.send_data()
                self.state_trans(STATE['state_2_blue_climb'])
            else:
                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()

        elif self.state == STATE['state_2_blue_climb']:
            if self.find_blue_upstair(frame) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_3_red_turn'])
            else:
                line_track(frame.copy(), err=1, type='grass', angle_limit=30)

                # light.pulse_width_percent(18)

                my_uart.send_data()
            my_uart.clear_data()

        elif self.state == STATE['state_3_red_turn']:
            if self.find_red_divpath(frame) is True :
                my_uart.send_data()
                self.state_trans(STATE['state_4_user'])
            else:
                # light.pulse_width_percent(18)

                line_track(frame.copy())
                my_uart.send_data()
            my_uart.clear_data()
        elif self.state == STATE['state_4_user']:
            if self.find_user(frame, self.ball_user):
                my_uart.set_data(1, 'isOpen')
                my_uart.send_data()
                self.state_trans(STATE['state_5_orange_end'])
            else:
                line_track(frame.copy(), err=1, type = 'grass', angle_limit=30)
            my_uart.clear_data()
        elif self.state == STATE['state_5_orange_end']:
            if self.find_orange_end(frame, 2) is True:
                my_uart.send_data()
                self.state_trans(STATE['state_6_turn_in'])
                #light.pulse_width_percent(10)  # 控制亮度 0~100完成
            else:
                line_track(frame.copy(), err=1, type='grass', angle_limit=30)
                my_uart.send_data()
            my_uart.clear_data()
        elif self.state == STATE['state_6_turn_in']:
            if line_track(frame.copy(), err = 10, type = 'turn', angle_limit=50):
                my_uart.send_data()
            else:
                my_uart.set_data(STRAIGHT, 'direction')
                my_uart.set_data(90, 'angle')
                self.state_trans(STATE['state_1_recognize_ball'])
                my_uart.send_data()
            my_uart.clear_data()
        else:
            pass

    def state_trans(self, st):
        N = 20
        if st == STATE['state_1_recognize_ball']:
            for i in range(N):
                info = my_uart.receive_data()
                if '1' in info:
                    self.state = st  # 状态转移成功
                    print("finished")
                    break
        elif st == STATE['state_2_blue_climb']:
            for i in range(N):
                info = my_uart.receive_data()
                if '2' in info:
                    self.state = st  # 状态转移成功
                    print('recieved ball')
                    # self.blue_time = pyb.millis() # TODO: 
                    break
        elif st == STATE['state_3_red_turn']:
            for i in range(N):
                info = my_uart.receive_data()
                if '3' in info:
                    self.state = st  # 状态转移成功
                    print('upstairs!!!')
                    break
        elif st == STATE['state_4_user']:
            for i in range(N):
                info = my_uart.receive_data()
                if '4' in info:
                    self.state = st  # 状态转移成功
                    print('near user')
                    break
        elif st == STATE['state_5_orange_end']:
            for i in range(N):
                info = my_uart.receive_data()
                if '5' in info:
                    self.state = st
                    print('user has been found!')
                    break
        elif st == STATE['state_6_turn_in']:
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
