import cfg
import pigpio


class MotorDrive:
    def __init__(self):
        cfg.pi.set_mode(cfg.IN1_MOTOR_LEFT, pigpio.OUTPUT)
        cfg.pi.set_mode(cfg.IN2_MOTOR_LEFT, pigpio.OUTPUT)
        cfg.pi.set_mode(cfg.IN1_MOTOR_RIGHT, pigpio.OUTPUT)
        cfg.pi.set_mode(cfg.IN2_MOTOR_RIGHT, pigpio.OUTPUT)
        cfg.pi.write(cfg.IN1_MOTOR_LEFT,0)
        cfg.pi.write(cfg.IN2_MOTOR_LEFT,0)
        cfg.pi.write(cfg.IN1_MOTOR_RIGHT,0)
        cfg.pi.write(cfg.IN2_MOTOR_RIGHT,0)
        self.dutyLeft = 0
        self.dutyRight = 0
    
    def get_duty(self):
        return self.dutyLeft, self.dutyRight

    def stop_motors(self):
        cfg.pi.hardware_PWM(cfg.IN1_MOTOR_LEFT,0,0)
        cfg.pi.hardware_PWM(cfg.IN2_MOTOR_LEFT,0,0)
        cfg.pi.hardware_PWM(cfg.IN1_MOTOR_RIGHT,0,0)
        cfg.pi.hardware_PWM(cfg.IN2_MOTOR_RIGHT,0,0)
        cfg.pi.write(cfg.IN1_MOTOR_LEFT,0)
        cfg.pi.write(cfg.IN2_MOTOR_LEFT,0)
        cfg.pi.write(cfg.IN1_MOTOR_RIGHT,0)
        cfg.pi.write(cfg.IN2_MOTOR_RIGHT,0)
        
    def brake_motors(self):
        cfg.pi.hardware_PWM(cfg.IN1_MOTOR_LEFT,0,0)
        cfg.pi.hardware_PWM(cfg.IN2_MOTOR_LEFT,0,0)
        cfg.pi.hardware_PWM(cfg.IN1_MOTOR_RIGHT,0,0)
        cfg.pi.hardware_PWM(cfg.IN2_MOTOR_RIGHT,0,0)
        cfg.pi.write(cfg.IN1_MOTOR_LEFT,1)
        cfg.pi.write(cfg.IN2_MOTOR_LEFT,1)
        cfg.pi.write(cfg.IN1_MOTOR_RIGHT,1)
        cfg.pi.write(cfg.IN2_MOTOR_RIGHT,1)
        
    def set_duty(self, duty_L, duty_R):
        self.dutyLeft = duty_L
        self.dutyRight = duty_R
        duty_L = int(duty_L*10000)
        duty_R = int(duty_R*10000)
        if (abs(duty_L) > 1000000) or (abs(duty_R) > 1000000):
            return
        if (duty_L/(abs(duty_L+1))>0):  #Forward
            cfg.pi.hardware_PWM(cfg.IN2_MOTOR_LEFT,0,0)
            cfg.pi.write(cfg.IN1_MOTOR_LEFT,0)
            cfg.pi.write(cfg.IN2_MOTOR_LEFT,0)
            cfg.pi.write(cfg.IN2_MOTOR_LEFT,1)
            cfg.pi.hardware_PWM(cfg.IN1_MOTOR_LEFT,50000,1000000-abs(duty_L))
            cfg.way_l = 1
        else:
            cfg.pi.hardware_PWM(cfg.IN1_MOTOR_LEFT,0,0)
            cfg.pi.write(cfg.IN1_MOTOR_LEFT,0)
            cfg.pi.write(cfg.IN2_MOTOR_LEFT,0)
            cfg.pi.write(cfg.IN1_MOTOR_LEFT,1)
            cfg.pi.hardware_PWM(cfg.IN2_MOTOR_LEFT,50000,1000000-abs(duty_L))
            cfg.way_l = -1
        if (duty_R/(abs(duty_R+1))>0):  #Forward
            cfg.pi.hardware_PWM(cfg.IN2_MOTOR_RIGHT,0,0)
            cfg.pi.write(cfg.IN1_MOTOR_RIGHT,0)
            cfg.pi.write(cfg.IN2_MOTOR_RIGHT,0)
            cfg.pi.write(cfg.IN2_MOTOR_RIGHT,1)
            cfg.pi.hardware_PWM(cfg.IN1_MOTOR_RIGHT,50000,1000000-abs(duty_R))
            cfg.way_r = 1
        else:
            cfg.pi.hardware_PWM(cfg.IN1_MOTOR_RIGHT,0,0)
            cfg.pi.write(cfg.IN1_MOTOR_RIGHT,0)
            cfg.pi.write(cfg.IN2_MOTOR_RIGHT,0)
            cfg.pi.write(cfg.IN1_MOTOR_RIGHT,1)
            cfg.pi.hardware_PWM(cfg.IN2_MOTOR_RIGHT,50000,1000000-abs(duty_R))
            cfg.way_r = -1

     