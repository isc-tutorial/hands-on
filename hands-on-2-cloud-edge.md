# Heterogenous Deployment

## MQTT Data Aggregation and Collection at the Edge

### Overview
This guide details the steps for setting up and deploying MQTT data aggregators and collectors in a Kubernetes environment, specifically tailored for edge computing scenarios.

## Prerequisites 

Same as for workflow-1

## Setup Instructions

1. **Prepare Your Environment**
   - Navigate to the demo folder and desired workflow:
     ```bash
     cd demo/hands-on/workflow-2
     ```
2. **Build and Push Docker Images**
   - **Aggregator Image**
     - Build the Docker image:
       ```bash
       podman build -f aggregator.dockerfile . -t isc-tutorial.hlrs.de/"$USER"/aggregator:latest
       ```
     - Push to the registry:
       ```bash
       podman push isc-tutorial.hlrs.de/"$USER"/aggregator:latest
       ```
   - **Collector Image**
     - Build the Docker image:
       ```bash
       podman build -f collector.dockerfile . -t isc-tutorial.hlrs.de/"$USER"/collector:latest
       ```
     - Push to the registry:
       ```bash
       podman push isc-tutorial.hlrs.de/"$USER"/collector:latest
       ```
   - **Client Image**
     - Build the Docker image:
       ```bash
       podman build -f client.dockerfile . -t isc-tutorial.hlrs.de/"$USER"/client-wf:latest
       ```
     - Push to the registry:
       ```bash
       podman push isc-tutorial.hlrs.de/"$USER"/client-wf:latest
       ```

4. **Deploy on Kubernetes**
   - Apply the Kubernetes YAML files to deploy the aggregator and collector:
     ```bash
     envsubst < yaml/aggregator_cloud.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
     envsubst < yaml/collector_edge.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
     envsubst < yaml/client.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
     ```

5. **Monitoring and Logs**
   - Check the logs of the pods to monitor operations:
   - Find the pod name of your client
     ```bash
     kubectl get pods -n decice
     ```
     - Check the logs of the client
     ```bash
     kubectl logs -n decice -f [client_pod_name]
      ```
6. **Cleanup Resources**
   - To remove deployed resources: MQTT aggregator, collector and client
     ```bash
     envsubst < yaml/aggregator_cloud.yaml | sed 's/-isc25_/-isc25-/g' | kubectl delete -f -
     envsubst < yaml/collector_edge.yaml | sed 's/-isc25_/-isc25-/g' | kubectl delete -f -
     envsubst < yaml/client.yaml | sed 's/-isc25_/-isc25-/g' | kubectl delete -f -    
     ```

#### Additional Information
- Review the YAML files to understand how the aggregator and collector are scheduled on the Kubernetes edge node.
- Check the difference in the yaml files workflow-2/yaml/collector_edge.yaml workflow-1/yaml/publisher.yaml. What change is needed to run using KubeEdge on the Edge node?


### Note
Replace placeholders such as `[pod_name]` with actual values from your Kubernetes cluster.


---

## Interactive Competition

Be the first to show your name on the display.

### Setup Description

[Dispaly firmware](https://github.com/isc-tutorial/infrastructure/tree/main/arduino-screen) interacts with the edge devices via serial interface using certain [protocol](https://github.com/isc-tutorial/infrastructure/blob/main/arduino-screen/PROTOCOL.md).

On the edge node [MQTT ↔ Serial Bridge](https://github.com/isc-tutorial/infrastructure/tree/main/mqtt2serial) is deployed. **Warning:** it is connected to a **local** MQTT server on the edge device (Raspberry pi), so it can only be accessed from the edge device.

### Competition Task

Show your name on the specified dislay by deploying an app on the same edge node.

Some hints:

1. Explore the code of the [MQTT ↔ Serial Bridge](https://github.com/isc-tutorial/infrastructure/tree/main/mqtt2serial), explore the [serial protocol](https://github.com/isc-tutorial/infrastructure/blob/main/arduino-screen/PROTOCOL.md) if needed.
2. Find the internal IP of the node, MQTT server is listening on that IP, port is defaul (`1883`)
3. Modify the publisher code from hands-on 1 (or implement your own app) to connect to the MQTT broker, and publish your name to the correct topic
4. Deploy you app to the correct edge node
