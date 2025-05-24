import asyncio
from gmqtt import Client as MQTTClient

BLYNK_AUTH_TOKEN = "-0MKwmcMYOBTK-OaPUObJxcG6sP8n7HR"
CLIENT_ID = BLYNK_AUTH_TOKEN
BLYNK_BROKER = "blynk.cloud"
BLYNK_PORT = 8883

class Device:
    def __init__(self, client):
        self.client = client

    def on_connect(self):
        print("✅ Đã kết nối với Blynk Cloud")
        self.client.subscribe("downlink/#")

    def on_message(self, topic, payload):
        payload_str = payload.decode()
        print(f"📥 {topic} = {payload_str}")

        if topic.endswith("v0"):
            print(f"🟢 Switch: {'ON' if payload_str == '1' else 'OFF'}")
        elif topic.endswith("v1"):
            print(f"📍 Joystick X: {payload_str}")
        elif topic.endswith("v2"):
            print(f"📍 Joystick Y: {payload_str}")

# Global
device = None

def handle_connect(client, flags, rc, properties):
    device.on_connect()

def handle_message(client, topic, payload, qos, properties):
    device.on_message(topic, payload)

async def main():
    global device
    client = MQTTClient(CLIENT_ID)
    client.set_auth_credentials("device", BLYNK_AUTH_TOKEN)
    
    client.on_connect = handle_connect
    client.on_message = handle_message

    device = Device(client)

    await client.connect(BLYNK_BROKER, BLYNK_PORT, ssl=True)
    print("⏳ Đang lắng nghe dữ liệu từ Blynk...")

    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        print("🛑 Thoát chương trình")

if __name__ == "__main__":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except:
        pass

    asyncio.run(main())
