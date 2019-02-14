import pigpio
#Global variables
pi = pigpio.pi()
way_l = 0
way_r = 0
enc_l = 0
enc_r = 0
counts_to_deg = 360/341.2
pwm_frequency = 1000

#GPIO pins BCM layout
IN1_MOTOR_LEFT = 12 
IN2_MOTOR_LEFT = 18

IN1_MOTOR_RIGHT = 13
IN2_MOTOR_RIGHT = 19

MOTOR_DRIVE_CHANNELS = [IN1_MOTOR_LEFT, IN2_MOTOR_LEFT, IN1_MOTOR_RIGHT, IN2_MOTOR_RIGHT]