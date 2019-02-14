import smbus
import math
import time 

class IMU:

    # Pre-defined ranges
    ACC_RANGE_2G = 0x00
    ACC_RANGE_4G = 0x08
    ACC_RANGE_8G = 0x10
    ACC_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    POWER_MGMT_1 = 0x6B
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACC_CONFIG = 0x1C

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x68 
        self.gyro_scale_factor = 131
        self.acc_scale_factor = 16384
        self.gyro_pitch_angle = 0
        self.gyro_bias = 0
        self.accPitchAngle_bias = 0
        self.x_pitch = 0
    

    def set_gyro_range(self,range):
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, range)
        if (range == self.GYRO_RANGE_250DEG):
            self.gyro_scale_factor = 131
        if (range == self.GYRO_RANGE_500DEG):
            self.gyro_scale_factor = 65.5
        if (range == self.GYRO_RANGE_1000DEG):
            self.gyro_scale_factor = 32.8
        if (range == self.GYRO_RANGE_2000DEG):
            self.gyro_scale_factor = 16.4
        else:
            self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)
            self.bus.write_byte_data(self.address, self.GYRO_CONFIG, self.GYRO_RANGE_250DEG)
            self.gyro_scale_factor = 131
        return 

    def set_acc_range(self,range): 
        self.bus.write_byte_data(self.address, self.ACC_CONFIG, 0x00)
        self.bus.write_byte_data(self.address, self.ACC_CONFIG, range)
        if (range == self.ACC_RANGE_2G):
            self.acc_scale_factor = 16384
        if (range == self.ACC_RANGE_4G):
            self.acc_scale_factor = 8192
        if (range == self.ACC_RANGE_8G):
            self.acc_scale_factor = 4096
        if (range == self.ACC_RANGE_16G):
            self.acc_scale_factor = 2048
        else:
            self.bus.write_byte_data(self.address, self.ACC_CONFIG, 0x00)
            self.bus.write_byte_data(self.address, self.ACC_CONFIG, self.ACC_RANGE_2G)
            self.acc_scale_factor = 16384
        return 

    def read_word(self,reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        value = (h << 8) + l
        return value
     
    def read_word_2c(self,reg):
        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
     
      
    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, math.sqrt((x*x)+(z*z)))
        return math.degrees(radians)
     
    def init_imu(self):     
            self.bus.write_byte_data(self.address, self.POWER_MGMT_1, 0x00)
            time.sleep(1)
            self.set_gyro_range(self.GYRO_RANGE_250DEG)
            self.set_acc_range(self.ACC_RANGE_2G)
            gyroOffset = 0
            accPitchAngle_init = 0
            print("Lay down device, calibration pending!\n")
            input("Press Enter to start calibration!\n")
            print("Calibration started...\n")
            k = 0
            while k < 100:
                    k+=1
                    gyroOffset = gyroOffset + self.read_word_2c(0x43)/self.gyro_scale_factor
                    xout = self.read_word_2c(0x3b) / self.acc_scale_factor
                    yout = self.read_word_2c(0x3d)/ self.acc_scale_factor
                    zout = self.read_word_2c(0x3f) / self.acc_scale_factor
                    accPitchAngle_init = accPitchAngle_init + self.get_x_rotation(xout,yout,zout)
                    time.sleep(0.020)
            self.gyro_bias = gyroOffset/100
            self.accPitchAngle_bias = accPitchAngle_init/100
            print("Calibration finished!\n")
            return

    def get_IMU_values(self,ts):
            
            gyro_x = self.read_word_2c(0x43)/self.gyro_scale_factor
            self.gyro_pitch_angle = self.x_pitch + ts*(gyro_x-self.gyro_bias)  
          
            acc_x = self.read_word_2c(0x3b) / self.acc_scale_factor
            acc_y = self.read_word_2c(0x3d) / self.acc_scale_factor
            acc_z = self.read_word_2c(0x3f) / self.acc_scale_factor
            accPitchAngle = self.get_x_rotation(acc_x,acc_y,acc_z)-self.accPitchAngle_bias
            self.x_pitch = 0.93*self.gyro_pitch_angle + 0.07*accPitchAngle    
            return (gyro_x-self.gyro_bias), self.x_pitch
