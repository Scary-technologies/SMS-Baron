from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import random
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os

app = Flask(__name__)

# User agents for random headers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Android 11; Mobile)"
]

# Logging setup
logging.basicConfig(
    filename='sms_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_random_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/json'
    }

def validate_phone(phone):
    if not phone.startswith("09") or len(phone) != 11 or not phone.isdigit():
        return False
    return True

def load_services():
    try:
        with open('SiteList.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def send_sms(service, phone):
    if service.get("is_get"):
        try:
            res = requests.get(service["url"] + phone, headers=get_random_headers(), timeout=10)
            status = res.status_code == 200
            log_entry(service["name"], "success" if status else "failed")
            return status
        except requests.exceptions.RequestException as e:
            log_entry(service["name"], f"error: {str(e)}")
            return False

    json_data = {service["json_key"]: phone}
    if service.get("extra_json"):
        json_data.update(service["extra_json"])

    try:
        res = requests.post(service["url"], json=json_data, headers=get_random_headers(), timeout=10)
        status = res.status_code == 200
        log_entry(service["name"], "success" if status else f"failed (status: {res.status_code})")
        return status
    except requests.exceptions.RequestException as e:
        log_entry(service["name"], f"error: {str(e)}")
        return False

def log_entry(service_name, status):
    logging.info(f"Service: {service_name}, Status: {status}")

def save_report(data):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sms_report_{now}.json"
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

@app.route('/')
def index():
    services = load_services()
    return render_template('index.html', service_count=len(services))

@app.route('/start_test', methods=['POST'])
def start_test():
    data = request.json
    phone = data.get('phone')
    rounds = int(data.get('rounds', 2))

    if not validate_phone(phone):
        return jsonify({'error': 'Invalid phone number. It must start with "09" and be 11 digits.'}), 400

    services = load_services()
    if not services:
        return jsonify({'error': 'SiteList.json file not found or empty!'}), 400

    logging.info(f"Starting SMS test to {phone} with {len(services)} services in {rounds} rounds")

    success = 0
    failed = 0
    error = 0
    report_log = []
    live_logs = []

    for round_num in range(1, rounds + 1):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(send_sms, service, phone): service for service in services}
            for future in futures:
                service = futures[future]
                try:
                    result = future.result()
                    status = "success" if result else "failed"
                    entry = {
                        "round": round_num,
                        "service": service["name"],
                        "status": status,
                        "time": datetime.now().isoformat()
                    }
                    report_log.append(entry)
                    live_logs.append({
                        "service": service["name"],
                        "status": status,
                        "round": round_num
                    })
                    if result:
                        success += 1
                    else:
                        failed += 1
                except Exception as e:
                    error += 1
                    report_log.append({
                        "round": round_num,
                        "service": service["name"],
                        "status": f"error: {str(e)}",
                        "time": datetime.now().isoformat()
                    })
                    live_logs.append({
                        "service": service["name"],
                        "status": "error",
                        "round": round_num
                    })

    filename = save_report(report_log)
    
    return jsonify({
        'success': success,
        'failed': failed,
        'error': error,
        'report_file': filename,
        'logs': live_logs
    })

@app.route('/download_report/<filename>')
def download_report(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)