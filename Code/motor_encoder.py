import smbus


class MotorEncoder:
    
    def __init__(self):
            self.bus = smbus.SMBus(3)
            self.address_l = 0x40
            self.address_r = 0x48
            self.value0_r = (self.bus.read_byte(self.address_r) << 24) + (self.bus.read_byte(self.address_r) << 16) +(self.bus.read_byte(self.address_r) << 8) + self.bus.read_byte(self.address_r)
            if self.value0_r > 2147483647:
                self.value0_r = -(self.value0_r & 0x7FFFFFFF)
            self.value0_l = (self.bus.read_byte(self.address_l) << 24) + (self.bus.read_byte(self.address_l) << 16) +(self.bus.read_byte(self.address_l) << 8) + self.bus.read_byte(self.address_l)
            if self.value0_l > 2147483647:
                self.value0_l = -(self.value0_l & 0x7FFFFFFF)
            
    def get_motor_angles(self):
            value_l = (self.bus.read_byte(self.address_l) << 24) + (self.bus.read_byte(self.address_l) << 16) +(self.bus.read_byte(self.address_l) << 8) + self.bus.read_byte(self.address_l)
            if (value_l >> 31):
                value_l = -(value_l & 0x7FFFFFFF)
            angle_l= (value_l-self.value0_l)*0.4825
            value_r = (self.bus.read_byte(self.address_r) << 24) + (self.bus.read_byte(self.address_r) << 16) +(self.bus.read_byte(self.address_r) << 8) + self.bus.read_byte(self.address_r)
            if (value_r >> 31):
                value_r = -(value_r & 0x7FFFFFFF)
            angle_r= (value_r-self.value0_r)*0.4825
            return angle_l, angle_r