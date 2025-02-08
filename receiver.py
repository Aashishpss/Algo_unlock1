import gradio as gr
import paho.mqtt.client as mqtt
import json

# 📌 Global variables to store received data
traffic_level = "Waiting for data..."
lane_suggestion = "Waiting for data..."

# 📌 MQTT Setup
MQTT_BROKER = "test.mosquitto.org"
TOPIC_SPEED = "platoon/speed"

def on_message(client, userdata, msg):
    global traffic_level, lane_suggestion
    data = json.loads(msg.payload)

    traffic_level = f"🚦 Traffic Level: {data['congestion_level']}%"
    lane_suggestion = f"🚗 Lane Suggestion: {data['lane_suggestion']}"

def get_data():
    return traffic_level, lane_suggestion

# 📌 MQTT Client Setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(TOPIC_SPEED)
client.loop_start()

# 📌 Gradio UI
iface = gr.Interface(
    fn=get_data,
    inputs=[],
    outputs=["text", "text"],
    title="🚘 Follower (Receiver) - Platoon System",
    description="Displays real-time traffic congestion and lane suggestions received from the Leader.",
    live=True  # Auto-refresh data
)

iface.launch()
