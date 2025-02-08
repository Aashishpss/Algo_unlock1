!pip install gradio paho-mqtt pandas scikit-learn
import gradio as gr
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import paho.mqtt.client as mqtt
import json

# 📌 Train Decision Tree Model
traffic_data = pd.DataFrame({
    'speed': [10, 20, 30, 40, 50, 60, 70, 80],
    'distance': [50, 40, 35, 30, 25, 20, 15, 10],
    'traffic_level': [10, 20, 35, 50, 65, 80, 90, 100]
})

X = traffic_data[['speed', 'distance']]
y = traffic_data['traffic_level']

model = DecisionTreeRegressor()
model.fit(X, y)

# 📌 MQTT Setup
MQTT_BROKER = "test.mosquitto.org"
TOPIC_SPEED = "platoon/speed"
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

# 📌 Prediction & Sending Function
def predict_traffic(speed, distance):
    return int(model.predict([[speed, distance]])[0])

def decide_lane(congestion_level):
    return "Stay" if congestion_level < 40 else "Go Right"

def send_data(speed, distance):
    congestion_level = predict_traffic(speed, distance)
    lane_suggestion = decide_lane(congestion_level)

    data = {
        "speed": speed,
        "distance": distance,
        "congestion_level": congestion_level,
        "lane_suggestion": lane_suggestion
    }

    client.publish(TOPIC_SPEED, json.dumps(data))
    return f"📡 Sent: Speed={speed} km/h, Distance={distance} m, Traffic={congestion_level}%, Lane={lane_suggestion}"

# 📌 Gradio UI
iface = gr.Interface(
    fn=send_data,
    inputs=[gr.Number(label="Enter Speed (km/h)"), gr.Number(label="Enter Distance (m)")],
    outputs="text",
    title="🚗 Leader (Sender) - Platoon System",
    description="Enter speed and distance to send real-time data to the follower."
)

iface.launch()