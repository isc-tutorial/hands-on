
# 🐮 Running a Basic Pod on InterLink with Slurm

This guide walks you through submitting a simple Kubernetes pod using [InterLink](https://github.com/grycap/interlink) and the Slurm virtual-kubelet plugin on the HAICGU cluster.

---

## ✅ Prerequisites

Make sure you have:

- A Kubernetes cluster with **InterLink** and **virtual-kubelet** configured
- The **Slurm virtual kubelet plugin** installed and running
- Access to the namespace where your virtual nodes (e.g., `decice`) are deployed
- `kubectl` configured to point to the right cluster

If the prerequisites are fulfilled, it’s possible to submit SLURM jobs in the form of standard K8s resources (e.g., pod) by using specific flags which will schedule the workload appropriately:

- Use nodeSelector to pick the virtual kubelet node
- Use annotations to pass SLURM-specific options which will be embedded into the BASH SLURM script.

---

## 📄 Example Pod YAML

Below is a sample pod manifest. It submits a Slurm job that writes a message to a file and prints it.

> 📌 **Attention**: The pod uses a randomized name. If you want to assign a specific name, replace `generateName` with `name` and then assign a value of your liking. 

```yaml
apiVersion: v1
kind: Pod
metadata:
  generateName: interlinkpod-
  namespace: decice
  annotations:
    slurm-job.vk.io/flags: "--partition=cn-ib --job-name=testsl -t 30  --ntasks=1 --nodes=1"
spec:
  restartPolicy: Never
  containers:
  - image: docker://ghcr.io/grycap/cowsay
    command: ["/bin/sh"]
    args: ["-c", "echo \\\"Hello ISC2025 Participants!!\\\" > /tmp/test.txt && cat /tmp/test.txt"]
    imagePullPolicy: Always
    name: isc2025_hello
    resources:
      limits:
         memory: 100Mi
         cpu: 2
  dnsPolicy: ClusterFirst
  nodeSelector:
    kubernetes.io/hostname: cn04
  tolerations:
  - key: virtual-node.interlink/no-schedule
    operator: Exists
```

> 📌 **Note**: The annotation `slurm-job.knoc.io/flags` directly maps to Slurm CLI job options.

---

## 🚀 Deploy the Pod

Apply the manifest with:

```bash
kubectl apply -f interlink-pod.yaml
```

---

## 🔍 Monitor Pod and Slurm Job

Check the pod status:

```bash
kubectl get pods -n decice
```

Check logs when the pod is running or completed:

```bash
kubectl logs test-pod -n decice
```

Check Slurm jobs (from the virtual node host or API):

```bash
squeue -u <your-user>
```

---

## 📦 View Job Output (if stored)

If the pod writes output to a file system mounted from the host or network storage:

```bash
kubectl exec -n decice interlinkpod-<random_string> -- cat /tmp/test.txt
```

Or collect logs/output from a shared directory configured via PVC.

---

## 🧼 Clean Up

Delete the pod once done:

```bash
kubectl delete pod interlinkpod-<random_string> -n decice
```

---

## 🛠 Tips

- Modify Slurm flags in the annotation to customize CPU, memory, time, etc.
- Logs may be buffered or delayed due to Slurm scheduling behavior.
- Use `kubectl describe pod` for debugging scheduling or annotation issues.

---
