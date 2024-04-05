import time
import RPi.GPIO as GPIO

Motor_A_EN = 4
Motor_A_Pin1 = 14
Motor_A_Pin2 = 15
Motor_B_EN = 17
Motor_B_Pin1 = 27
Motor_B_Pin2 = 18


pwm_A = 0
pwm_B = 0

def motorStop():
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)

def setup():
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)
    motorStop()
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)
    except:
        pass

def move(speed):
    #speed = 0~100
    if speed < 0 and speed >= -100:
        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        pwm_A.start(0)
        pwm_B.start(0)
        pwm_A.ChangeDutyCycle(-speed)
        pwm_B.ChangeDutyCycle(-speed)
        #GPIO.output(Motor_A_EN, GPIO.HIGH)
        #pwm.ChangeDutyCycle(speed)
    elif speed > 0 and speed <= 100:
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.HIGH)
        pwm_A.start(100)
        pwm_B.start(100)
        pwm_A.ChangeDutyCycle(speed)
        pwm_B.ChangeDutyCycle(speed)
        #GPIO.output(Motor_A_EN, GPIO.HIGH)
        #pwm.ChangeDutyCycle(-speed)
    else:
        motorStop()

def destroy():
    motorStop()
    GPIO.cleanup()

#if __name__ == '__main__':
#    try:
#        while True:
#            speed_set = 60 
#            setup()
            #pwm = GPIO.PWM(Motor_A_EN, 100)
            #pwm.start(0)

#            move(100)
#            print(speed_set)
#            time.sleep(3) 
#            motorStop()

            # move(0)
 #           time.sleep(0.5)

#            move(-100)
#            print(-100)
#            time.sleep(3)
#            motorStop()

            #destroy()
 #   except KeyboardInterrupt:
 #       destroy()
