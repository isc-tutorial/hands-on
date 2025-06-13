
import os
import paho.mqtt.client as mqtt
import ollama

# Get MQTT configuration from environment variables
mqtt_server = os.environ.get("MQTT_SERVER", "localhost")
mqtt_port = int(os.environ.get("MQTT_PORT", 1883))
subscribe_topic = os.environ.get("MQTT_SUB_TOPIC", "mic/stream")
publish_topic = os.environ.get("MQTT_PUB_TOPIC", "clock1/message")
model = os.environ.get("INFERENCE_MODEL", "tinyllama")
inference_server = os.environ.get("INFERENCE_SERVER", "http://localhost:11434")

# Set up clients
my_ollama_client = ollama.Client(host=inference_server)
my_mqtt_client = mqtt.Client()

# Callback when a message is received
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"\nReceived on topic '{msg.topic}':\n{message}")
    
    response_accumulator = ""

    try:
        # Streaming response from Ollama
        for chunk in my_ollama_client.generate(model=model, prompt=message, stream=True):
            content = chunk.get("response", "")
            response_accumulator += content
            client.publish(publish_topic, response_accumulator)
            print(content, end="", flush=True)
        print(f"\nPublished streamed response to '{publish_topic}'")
    except ollama.ResponseError as e:
        if e.status_code == 404:
            print(f"Model '{model}' not found. Attempting to pull the model...")
            try:
                my_ollama_client.pull(model)
                print(f"Successfully pulled model '{model}'. Retrying...")
                response_accumulator = ""
                for chunk in my_ollama_client.generate(model=model, prompt=message, stream=True):
                    content = chunk.get("response", "")
                    response_accumulator += content
                    client.publish(publish_topic, response_accumulator)
                    print(content, end="", flush=True)
                print(f"\nPublished streamed response to '{publish_topic}'")
            except Exception as pull_error:
                print(f"Failed to pull model '{model}': {pull_error}")
        else:
            print(f"An error occurred: {e}")

# Assign MQTT callbacks and connect
my_mqtt_client.on_message = on_message

try:
    my_mqtt_client.connect(mqtt_server, mqtt_port)
    my_mqtt_client.subscribe(subscribe_topic)
    print(f"Listening for messages on '{subscribe_topic}' from {mqtt_server}:{mqtt_port} ...")
    my_mqtt_client.loop_forever()
finally:
    print("Shutting down MQTT client...")
    my_mqtt_client.disconnect()