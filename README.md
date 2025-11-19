# AI-Powered Cloud Threat Triage Pipeline

## 🚀 Project Overview
This project demonstrates an automated security operations pipeline that integrates **Runtime Security (Falco)** with **Local Large Language Models (Ollama/Llama3)** to perform real-time threat analysis and incident response without data leaving the local environment.

**Goal:** Reduce Level-1 Analyst fatigue by automating the triage and remediation suggestion phase for Kubernetes alerts.

## 🛠️ Tech Stack
* **OS:** Kali Linux (SecOps Environment)
* **Container Security:** Minikube (K8s), Falco (Runtime Detection)
* **AI Engine:** Ollama running Llama3 (Local LLM)
* **Orchestration:** Python (Custom Triage Script)
* **Data Pipeline:** Unix Piping (`tail -f` -> JSON Stream -> AI Analysis -> Audit Log)

## 📂 File Structure
* `triage.py`: The core logic script. Listens for logs, queries the AI, and generates reports.
* `attack_simulation.sh`: A bash script that generates synthetic Falco alerts (High & Critical) to test the pipeline.
* `incidents.json`: The "database" where the AI automatically saves its findings.

## ⚡ Quick Start
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
   ollama pull llama3:8b
   ```

2. **Start the Triage Engine:**
   ```bash
   touch alerts.log
   tail -f alerts.log | python3 triage.py
   ```

3. **Run the Simulation (In a new terminal):**
   ```bash
   chmod +x attack_simulation.sh
   ./attack_simulation.sh
   ```

## 📸 Operational Workflow

### Phase 1: Infrastructure Setup
Deploying a local Kubernetes cluster using Minikube to simulate a production cloud environment.
![Minikube Setup](Screenshot%202025-11-19%20124916.png)

### Phase 2: Security Tool Deployment
Installing Falco via Helm charts to monitor kernel-level system calls for suspicious behavior.
![Falco Deployment](Screenshot%202025-11-19%20125434.png)

### Phase 3: The Problem (Raw Telemetry)
Security tools like Falco output raw JSON logs. Without automation, a human analyst must manually parse thousands of these lines to find the signal in the noise.
![Raw Logs](Screenshot%202025-11-19%20135222.png)

### Phase 4: AI Logic Demonstration
The core engine (Python + Llama3) analyzes alerts in real-time. Here is how it handles different threat levels:

**Case A: High Severity (Shell in Container)**
The AI detects a `Notice` level alert. It identifies the threat as an "Unauthorized Terminal" and suggests deleting the specific pod.
![High Severity Alert](Screenshot%202025-11-19%20143513.png)

**Case B: Critical Severity (Container Escape + Integration)**
The AI detects a `Critical` level alert (writing to `/host/etc`).
1. It escalates the threat level correctly.
2. It identifies the intent as "Privilege Escalation/Persistence."
3. It generates a specialized remediation command.
4. **Integration:** The script automatically saves this critical finding to `incidents.json` for audit compliance.
![Critical Analysis and DB Save](Screenshot%202025-11-19%20145918.png)
