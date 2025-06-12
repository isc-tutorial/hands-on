# Container Deployment Instructions

## Overview
This guide provides instructions for building and deploying MQTT publisher and subscriber services using Podman and Kubernetes.

## Prerequisites
- Userid/password will be shared during the tutorial
- Access to a Kubernetes cluster.(https://haicgu.github.io/access.html)
    ```
    ssh guoehi-dev
    cd
    mkdir .kube
    cp /mnt/dev-lscratch/tutorial/config ~/.kube
   ```
   - Alternatively you can use the web console: https://isc-tutorial.hlrs.de/
- Check access to kubernetes cluster
  ```
  kubectl get nodes -A
   ```
- We are using a private Image Repository for this tutorial. Password for the Image Repository can be found in `/mnt/dev-lscratch/tutorial/registry.pass`

- Podman installed on your machine.
   - Podman rootless is already preinstalled on the `dev` node
   - Running unprivileged Podman won't support storage on NFS. If you get warnings (or errors) about running on NFS, configure Podman to use local storage instead. E.g. on the `dev` node: `export XDG_DATA_HOME="/mnt/dev-lscratch/$USER/local_share"; mkdir -p "$XDG_DATA_HOME"`

## Setup Instructions

1. **Navigate to Home Directory**
   ```bash
   cd ~
   ```

2. **Clone the Repository**
   ```bash
   git clone https://github.com/isc-tutorial/hands-on.git ~/demo/
   ```

3. **Navigate to the Project Directory**
   ```bash
   cd ~/demo/workflow-1
   ```

4. **Optional: Check/Edit Python Code**
   Modify the Python code within the repository if necessary.

5. **Login to Image Repository**
   Password for the Image Repository can be found in /mnt/dev-lscratch/tutorial/registry.pass
   ```bash
   cat /mnt/dev-lscratch/tutorial/registry.pass
   podman https://isc-tutorial.hlrs.de/ -u ISC25
   # enter/copy password from registry.pass
   ```

7. **Build the Publisher Docker Image**
   ```bash
   podman build -f publisher.dockerfile . -t isc-tutorial.hlrs.de/"$USER"/publisher:latest
   ```

8. **Build the Subscriber Docker Image**
   ```bash
   podman build -f subscriber.dockerfile . -t isc-tutorial.hlrs.de/"$USER"/subscriber:latest
   ```

9. **Push the Docker Images**
   - **Publisher Image**
     ```bash
     podman push isc-tutorial.hlrs.de/"$USER"/publisher:latest
     ```
   - **Subscriber Image**
     ```bash
     podman push isc-tutorial.hlrs.de/"$USER"/subscriber:latest
     ```

#### Deploying on Kubernetes

1. **Deploy the MQTT Publisher**
   ```bash
   envsubst < yaml/publisher.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
   ```

2. **Deploy the MQTT Subscriber**
   ```bash
   envsubst < yaml/subscriber.yaml | sed 's/-isc25_/-isc25-/g' | kubectl create -f -
   ```

3. **Check the Logs**
   - **Find the Pods**
     ```bash
     kubectl get pods -n decice
     ```
   - **Logs for Publisher**
     ```bash
     kubectl logs -n decice -f [publisher_pod_name]
     ```
   - **Logs for Subscriber**
     ```bash
     kubectl logs -n decice -f [subscriber_pod_name]
     ```

#### Cleanup

- **Undeploy the MQTT Publisher**
  ```bash
  envsubst < yaml/publisher.yaml | sed 's/-isc25_/-isc25-/g' | kubectl delete -f -
  ```

- **Undeploy the MQTT Subscriber**
  ```bash
  envsubst < yaml/subscriber.yaml | sed 's/-isc25_/-isc25-/g' | kubectl delete -f -
  ```

#### Additional Information

Review the YAML files to understand the assignment of pods to Kubernetes nodes and locate the connection details for the broker.

### Note
- Replace placeholders such as `[publisher_pod_name]` with actual values.
- Ensure that `envsubst` is installed and available in your environment.

This README is intended to guide you through setting up your development environment for deployment. Adjust the instructions as needed to fit your specific project requirements.
