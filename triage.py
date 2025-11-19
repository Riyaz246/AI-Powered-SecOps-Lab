import sys
import json
import ollama
from datetime import datetime

# Configuration
# The specific model version downloaded in the lab
MODEL = "llama3:8b"  
# The output file where incidents are recorded (Simulating a SIEM/Database)
LOG_FILE = "incidents.json"

print(f"--- AI Triage Started (Model: {MODEL}) ---")
print(f"--- Logging incidents to: {LOG_FILE} ---")
print("Waiting for Falco alerts...")

def save_incident(alert, analysis):
    """
    Saves the raw alert and the AI's analysis to a JSON line file.
    This simulates sending the data to an Elasticsearch or Splunk backend for long-term storage.
    """
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "original_alert": alert,
        "ai_assessment": analysis
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

# Main Pipeline Loop
# Reads from Stdin (Unix Pipe) to allow real-time streaming from 'tail -f'
for line in sys.stdin:
    try:
        # 1. Parse the incoming log line
        alert = json.loads(line)
        
        # Extract key fields (Falco standard output fields)
        rule = alert.get("rule", "Unknown Rule")
        priority = alert.get("priority", "Unknown")
        output_log = alert.get("output", "")

        print(f"\n[!] Alert Detected: {rule}")
        print("   >> Sending to AI for analysis ... (Please Wait)")

        # 2. Construct the Contextual Prompt
        # This prompt guides the LLM to act as a Tier 2 Security Analyst.
        prompt = f"""
        You are a Senior Security Analyst. Analyze this Kubernetes security alert.
        
        ALERT DETAILS:
        Rule: {rule}
        Priority: {priority}
        Log Output: {output_log}
        
        TASK:
        1. Explain what is happening in 1 sentence.
        2. Assess the Threat Level (Low, Medium, High, Critical).
        3. Provide a specific kubectl command to remediate or isolate the pod.
        
        Output format: Markdown.
        """

        # 3. Query the Local AI (Ollama)
        response = ollama.chat(model=MODEL, messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        analysis = response['message']['content']

        # 4. Print the Report to the Console (Dashboard)
        print("\n" + "="*20 + " AI TRIAGE REPORT " + "="*20)
        print(analysis)
        print("="*60)

        # 5. Integration Step (Save to Database)
        save_incident(alert, analysis)
        print(f"   [+] Incident saved to {LOG_FILE}")

    except json.JSONDecodeError:
        # Gracefully handle lines that aren't JSON (like empty lines)
        continue 
    except Exception as e:
        print(f"Error: {e}")
