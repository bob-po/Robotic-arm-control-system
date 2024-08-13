# coding:utf-8
import cv2
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2, Preview

GPIO.setmode(GPIO.BCM)

servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

kp = 5
old_degree_x = 90


def calculate_offset(img_width, img_height, face):
    '''
    计算人脸在画面中的偏移量
    偏移量的取值范围：[-1,1]
    '''
    (x, y, w, h) = face
    face_x = float(x + w / 2)
    face_y = float(y + h / 2)
    offset_x = float(face_x / img_width - 0.5) * 2
    offset_y = float(face_y / img_height - 0.5) * 2
    return offset_x, offset_y


def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

s = True
if __name__ == '__main__':

    # 加载训练好的人脸检测器
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    # 打开摄像头
    picamera = Picamera2()
    picamera.start_preview(Preview.NULL)
    config = picamera.create_preview_configuration({'size': (808, 606), 'format': 'BGR888'})
    picamera.configure(config)
    picamera.start()
    time.sleep(0.5)

    fred = cv2.getTickFrequency()  # 系统频率
    while True:
        # 读取一帧图像
        # 读取一帧图像
        img = picamera.capture_array('main')

        t1 = cv2.getTickCount()
        # 转换为灰度
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 进行人脸检测
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50),
                                             flags=cv2.CASCADE_SCALE_IMAGE)

        # 画框
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            x_offset, y_offset = calculate_offset(img.shape[0], img.shape[1], face=(x, y, w, h))
            delta_degree_x = kp * x_offset
            new_degree_x = old_degree_x + delta_degree_x
            if s:
                print(new_degree_x)
                # set_angle(new_degree_x)
                s = False
            old_degree_x = new_degree_x
        t2 = cv2.getTickCount()

        fps = fred / (t2 - t1)

        # 显示速度
        cv2.putText(img, 'FPS: {:.2f}'.format(fps), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        time.sleep(2)
        # 显示检测结果
        cv2.imshow('FACE', img)

        # 按q退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    picamera.close()
