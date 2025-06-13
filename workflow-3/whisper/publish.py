import os
import subprocess
import threading
import time
import re
import paho.mqtt.client as mqtt

# Get MQTT broker info and topics from environment variables
mqtt_server = os.environ.get("MQTT_SERVER", "localhost")
mqtt_port = int(os.environ.get("MQTT_PORT", 1883))
mqtt_button_topic = os.environ.get("MQTT_BUTTON_TOPIC", "clock1/button")
mqtt_whisper_topic = os.environ.get("MQTT_WHISPER_TOPIC", "mic/stream")

# Setup MQTT client
client = mqtt.Client()

# Regex to strip [anything]
bracket_pattern = re.compile(r"\[.*?\]")

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(text):
    return ansi_escape.sub('', text)

# Whisper command
cmd = [
    "whisper-stream",
    "-m", "/models/ggml-base.bin",
    "-t", "8",
    "--step", "3000",
    "--length", "3000",
]


# Add device number from environment variable if set
whisper_device = os.environ.get("WHISPER_DEVICE")
if whisper_device:
    cmd.extend(["-c", whisper_device])

# Process running flag (to avoid overlapping subprocesses)
process_running = threading.Lock()

def kill_process_after(proc, timeout):
    time.sleep(timeout)
    if proc.poll() is None:
        proc.terminate()

def run_whisper_process():
    if not process_running.acquire(blocking=False):
        print("Process is already running. Ignoring request.")
        return

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        timer = threading.Thread(target=kill_process_after, args=(proc, 10))
        timer.start()

        output_lines = []

        try:
            for line in proc.stdout:
                print(f"[RAW] {line.strip()}")
                line = strip_ansi(line)
                no_brackets = bracket_pattern.sub("", line)
                cleaned_line = no_brackets.lstrip("> ").strip()
                print(f"[CLEAN] {cleaned_line}")
                if cleaned_line and not cleaned_line.lower().startswith("("):
                    output_lines.append(cleaned_line)
        finally:
            proc.stdout.close()
            proc.wait()
            timer.join()
        print(output_lines)
        # Join all lines with spaces for a single-line output
        combined_output = " ".join(output_lines)
        client.publish(mqtt_whisper_topic, combined_output)
        print("Published message:")
        print(combined_output)
    finally:
        process_running.release()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_button_topic)

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    threading.Thread(target=run_whisper_process).start()

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server, mqtt_port)
client.loop_forever()