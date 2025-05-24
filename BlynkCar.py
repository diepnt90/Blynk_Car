# BlynkCar.py - Kết nối Blynk và điều khiển ô tô mô hình qua BTS7960

import asyncio
import RPi.GPIO as GPIO
from gmqtt import Client as MQTTClient

# ==== Cấu hình Blynk ====
BLYNK_AUTH_TOKEN = "-0MKwmcMYOBTK-OaPUObJxcG6sP8n7HR"
BLYNK_BROKER = "blynk.cloud"
BLYNK_PORT = 8883
CLIENT_ID = BLYNK_AUTH_TOKEN

# ==== Cài đặt GPIO ====
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motors = {
    "motor_1": {"RPWM": 18, "LPWM": 19, "calibration_factor": 1.0, "reverse": False},
    "motor_2": {"RPWM": 20, "LPWM": 21, "calibration_factor": 1.22, "reverse": True},
    "motor_3": {"RPWM": 22, "LPWM": 23, "calibration_factor": 1.0, "reverse": False},
    "motor_4": {"RPWM": 24, "LPWM": 25, "calibration_factor": 1.22, "reverse": True},
}

for motor in motors.values():
    GPIO.setup(motor["RPWM"], GPIO.OUT)
    GPIO.setup(motor["LPWM"], GPIO.OUT)
    motor["pwm_r"] = GPIO.PWM(motor["RPWM"], 1000)
    motor["pwm_l"] = GPIO.PWM(motor["LPWM"], 1000)
    motor["pwm_r"].start(0)
    motor["pwm_l"].start(0)

def set_motor_speed(name, speed):
    motor = motors[name]
    pwm_r = motor["pwm_r"]
    pwm_l = motor["pwm_l"]
    factor = motor["calibration_factor"]
    reverse = motor["reverse"]
    real_speed = min(int(abs(speed) * factor), 100)
    if (speed >= 0 and not reverse) or (speed < 0 and reverse):
        pwm_r.ChangeDutyCycle(real_speed)
        pwm_l.ChangeDutyCycle(0)
    else:
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(real_speed)

def stop_all():
    for name in motors:
        set_motor_speed(name, 0)

# ==== Lớp thiết bị giao tiếp Blynk ====
class Device:
    def __init__(self, client):
        self.client = client
        self.joy_x = 512
        self.joy_y = 512
        self.running = False

    def on_connect(self):
        print("\n✅ Đã kết nối Blynk Cloud")
        self.client.subscribe("downlink/#")

    def on_message(self, topic, payload):
        val = payload.decode()
        print(f"📥 {topic} = {val}")

        if topic.endswith("v0"):  # switch
            self.running = val == '1'
            if not self.running:
                stop_all()
                print("🔴 Stop all motors")

        elif topic.endswith("v1"):  # joystick x
            self.joy_x = int(val)

        elif topic.endswith("v2"):  # joystick y
            self.joy_y = int(val)

        self.update_motors()

    def update_motors(self):
        if not self.running:
            stop_all()
            return

        # Chuẩn hoá giá trị joystick (512 giữa, 0-1023)
        forward_back = (self.joy_y - 512) / 512  # -1 ~ 1
        left_right = (self.joy_x - 512) / 512

        speed_l = (forward_back - left_right) * 100
        speed_r = (forward_back + left_right) * 100

        set_motor_speed("motor_1", speed_l)
        set_motor_speed("motor_2", speed_r)
        set_motor_speed("motor_3", speed_l)
        set_motor_speed("motor_4", speed_r)

        print(f"🚗 Left={speed_l:.1f}%, Right={speed_r:.1f}%")

# ==== MQTT callbacks ====
device = None

def on_connect(client, flags, rc, properties):
    device.on_connect()

def on_message(client, topic, payload, qos, properties):
    device.on_message(topic, payload)

# ==== Main loop ====
async def main():
    global device
    client = MQTTClient(CLIENT_ID)
    client.set_auth_credentials("device", BLYNK_AUTH_TOKEN)

    client.on_connect = on_connect
    client.on_message = on_message

    device = Device(client)

    await client.connect(BLYNK_BROKER, BLYNK_PORT, ssl=True)
    print("⏳ Lắng nghe dữ liệu Blynk...")

    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        print("🛑 Thoát")
        stop_all()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except:
        pass

    asyncio.run(main())
