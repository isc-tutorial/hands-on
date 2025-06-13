# Container Deployment Instructions

## Overview
We record the speech and transcribe them at edge (using Whisper.cpp) and send them to the cloud or edge for inference (models served using ollama).
The whisper.cpp is compiled while building the dockerfile. 
For ollama, we use the offical docker image for pulling and serving the model. The ollama pod will have two containers. One does the inference 

## Prerequisites
In addition to the prerequisites for hand-on 1 and 2, we will also need microphone attached to the Raspberry Pi.

## Build and push the images

1. **Build and push the Whisper.cpp Docker Image**
   ```bash
   cd ~/demo/workflow-3/whisper
   podman build -f dockerfile . -t isc-tutorial.hlrs.de/"$USER"/whisper:latest
   podman push isc-tutorial.hlrs.de/"$USER"/whisper:latest
   ```

2. **Build the ollama client Docker Image**
   ```bash
   cd ~/demo/workflow-3/ollama
   podman build -f dockerfile . -t isc-tutorial.hlrs.de/"$USER"/mqttollamaclient:latest
   podman push isc-tutorial.hlrs.de/"$USER"/mqttollamaclient:latest
   ```

#### Deploying on Kubernetes

1. **Deploy the Whisper.cpp Publisher**
   ```bash
   Open the 
   envsubst < ~/demo/workflow-3/whisper/deployment.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
   ```

2. **Deploy the MQTT Subscriber**
   ```bash
   envsubst < ~/demo/workflow-3/ollama/deployment.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
   ```

3. **Check the Logs**
   - **Find the Pods**
     ```bash
     kubectl get pods -n decice
     ```
   - **Logs for Publisher**
     ```bash
     kubectl logs -n decice -f [whisper_pod_name]
     ```
   - **Logs for Subscriber**
     ```bash
     kubectl logs -n decice -f [ollama_pod_name]
     ```

#### Cleanup

- **Undeploy the whisper pod**
  ```bash
   envsubst < ~/demo/workflow-3/whisper/deployment.yaml | sed 's/-isc25_/-isc25-/g' | kubectl delete -f -
  ```

- **Undeploy the ollama pod**
  ```bash
   envsubst < ~/demo/workflow-3/ollama/deployment.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
  ```

### Note
This README is intended to guide you through setting up your development environment for deployment. Adjust the instructions as needed to fit your specific project requirements.
