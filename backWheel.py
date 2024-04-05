import time
import RPi.GPIO as GPIO

Motor_A_EN = 4
Motor_A_Pin1 = 26
Motor_A_Pin2 = 21

def motorStop():
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_A_EN, GPIO.LOW)

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT) 
    motorStop()

def move(speed):
    #speed = 0~100
    if speed >= 0 and speed <= 100:
        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        pwm.ChangeDutyCycle(speed)
    elif speed < 0 and speed >= -100:
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        pwm.ChangeDutyCycle(-speed)
    else:
        motorStop()

def destroy():
    motorStop()
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        speed_set = 100 
        setup()
        pwm = GPIO.PWM(Motor_A_EN, 100)
        pwm.start(0)

        move(speed_set)
        time.sleep(1.3) 

        move(0)  # 모터 정지
        time.sleep(0.5)  # 정지 후 대기

        speed_set = -50  # 역방향으로 회전
        move(speed_set)
        time.sleep(1.3) 

        destroy()
    except KeyboardInterrupt:
        destroy()
