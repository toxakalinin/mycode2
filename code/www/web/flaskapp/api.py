from flask import Flask, Blueprint, request, jsonify, render_template, flash
import subprocess
import psutil
import ssl
import socket
from datetime import datetime
import re
import logging
import requests
from .models import db, FirewallRule, LogEntry
from .utils import Utils

api_bp = Blueprint("api", __name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'


@api_bp.route('/loginadmin', methods=['POST'])
def loginadmin():
    honeypot = request.form.get('honeypot', '')
    if honeypot:
        ip = request.remote_addr
        log_trap(ip, "Honeypot triggered")
        block_ip(ip)
        return jsonify({"error": "Access Denied"}), 403

@api_bp.route('/trap')
def trap():
    ip = request.remote_addr
    log_ip_access(ip, "Fake link triggered")
    ban_ip(ip)
    return jsonify({"error": "Bot detected and logged"}), 403

def log_trap(ip, message):
    log_file = "/var/www/web/logs/app.log"
    with open(log_file, 'a') as f:
        f.write(f"{message} by IP: {ip}\n")

def make_response(data=None, error=None, status=200):
    if error:
        return jsonify({"success": False, "error": error}), status
    return jsonify({"success": True, "data": data}), status

def validate_target(target):
    ip_regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    domain_regex = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}$"
    if not re.match(ip_regex, target) and not re.match(domain_regex, target):
        raise ValueError("Invalid target. Must be a valid IP or domain.")

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')

    try:
        if command == "terminal_help":
            result = (
                "Available Commands:\n"
                "/df - Disk Usage\n"
                "/free - Memory Usage\n"
                "/top - CPU Stats\n"
                "Type any shell command to execute it."
            )
        elif command == "uptime":
            result = subprocess.check_output("uptime", shell=True).decode().strip()
        # Обработка других команд
        else:
            result = "Unknown command."

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"}), 500


#async def terminal_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    help_text = (
#        "Available Commands:\n"
 #       "/df - Disk Usage\n"
 #       "/free - Memory Usage\n"
 #       "/top - CPU Stats\n"
 #       "Type any shell command to execute it."
  #  )
  #  await update.message.reply_text(help_text)#
#
#
#@app.route('/api/command', methods=['POST'])
#def handle_command():
#    data = request.json
 #   command = data.get('command')
#
#    try:
  #      if command == "uptime":
  #     33#     result = subprocess.check_output("uptime", shell=True).decode().strip()
  #    #  elif command == "disk":
  #  #       result = subprocess.check_output("df -h", shell=True).decode().strip()
   ###     elif command == "memory":
 #           result = subprocess.check_output("free -m", shell=True).decode().strip()
 #       elif command == "cpu":
 #           result = subprocess.check_output("top -b -n 1 | head -5", shell=True).decode().strip()
 #       elif command == "netstat":
  #          result = subprocess.check_output("netstat -tuln", shell=True).decode().strip()
  #      elif command.startswith("ping"):
  #          host = command.split(" ")[1]
  #         result = subprocess.check_output(f"ping -c 4 {host}", shell=True).decode().strip()
  #      elif command == "scan":
   #         result = "Starting a security scan... (integration needed)"
   #     elif command == "terminal_help":
   #         await update.message.reply_text(help_text)
#        
#        else:
#            result = "Unknown command."
#
##        return jsonify({"result": result})
# 3   except Exception as e:
#3       return jsonify({"result": f"Error: {str(e)}"}), 500


@api_bp.route("/scan", methods=["POST"])
def perform_scan():
    scan_type = request.form.get("scan_type")
    target = request.form.get("target")

    try:
        validate_target(target)

        scan_command = {
            "ping": ["ping", "-c", "4", target],
            "traceroute": ["traceroute", target],
            "port_scan": ["nmap", "-p", "1-1000", target],
            "nikto": ["nikto", "-h", target],
            "whois": ["whois", target],
        }.get(scan_type)

        if scan_type == "ssl_checker":
            context = ssl.create_default_context()
            with socket.create_connection((target, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    expiration = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    return make_response(data={
                        "SSL Expiration": expiration,
                        "Issuer": cert.get("issuer"),
                        "Subject": cert.get("subject")
                    })

        if not scan_command:
            return make_response(error="Invalid scan type", status=400)

        result = subprocess.run(scan_command, capture_output=True, text=True)
        return make_response(data=result.stdout)

    except ValueError as ve:
        return make_response(error=str(ve), status=400)
    except Exception as e:
        logging.error(f"Error during scan: {e}")
        return make_response(error="Scan failed", status=500)


def ban_ip(ip):
    try:
        jail_name = "custom-trap"
        command = f"'fail2ban-client set' '{jail_name}' 'banip {ip}'"
        subprocess.run(command, shell=True, check=True)
        print(f"IP {ip} заблокирован через fail2ban.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при блокировке IP {ip}: {e}")


@api_bp.route("/block_ip", methods=["POST"])
def block_ip():
    data = request.json
    ip = data.get("ip")
    try:
        if not ip:
            raise ValueError("IP address is required.")
        Utils.add_ip_block(ip)
        return make_response(data=f"Blocked IP: {ip}")
    except Exception as e:
        logging.error(f"Failed to block IP: {e}")
        return make_response(error=str(e), status=500)

@api_bp.route("/unblock_ip", methods=["POST"])
def unblock_ip():
    data = request.json
    ip = data.get("ip")
    try:
        Utils.remove_ip_block(ip)
        return make_response(data=f"Unblocked IP: {ip}")
    except Exception as e:
        logging.error(f"Failed to unblock IP: {e}")
        return make_response(error=str(e), status=500)

@api_bp.route("/dns_lookup", methods=["POST"])
def dns_lookup():
    data = request.json
    domain = data.get("domain")
    try:
        dns_records = socket.gethostbyname_ex(domain)
        return make_response(data={"dns_records": dns_records})
    except Exception as e:
        logging.error(f"DNS lookup failed: {e}")
        return make_response(error="DNS lookup failed", status=500)

@api_bp.route("/reverse_dns_lookup", methods=["POST"])
def reverse_dns_lookup():
    data = request.json
    ip = data.get("ip")
    try:
        reverse_dns = socket.gethostbyaddr(ip)
        return make_response(data={"reverse_dns": reverse_dns})
    except Exception as e:
        logging.error(f"Reverse DNS lookup failed: {e}")
        return make_response(error="Reverse DNS lookup failed", status=500)

@api_bp.route("/system_metrics", methods=["GET"])
def get_system_metrics():
    try:
        metrics = {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_received": psutil.net_io_counters().bytes_recv,
            },
        }
        return make_response(data=metrics)
    except Exception as e:
        logging.error(f"Failed to fetch system metrics: {e}")
        return make_response(error="Failed to fetch metrics", status=500)

@api_bp.route("/processes", methods=["GET", "POST"])
def manage_processes():
    if request.method == "GET":
        try:
            processes = [{"pid": p.pid, "name": p.name()} for p in psutil.process_iter()]
            return make_response(data=processes)
        except Exception as e:
            logging.error(f"Failed to list processes: {e}")
            return make_response(error="Failed to list processes", status=500)
    elif request.method == "POST":
        action = request.json.get("action")
        process_name = request.json.get("process_name")
        pid = request.json.get("pid")
        try:
            if action == "start" and process_name:
                result = subprocess.Popen([process_name])
                return make_response(data={"message": f"Started process {process_name}", "pid": result.pid})
            elif action == "kill" and pid:
                psutil.Process(int(pid)).terminate()
                return make_response(data={"message": f"Killed process with PID {pid}"})
            else:
                return make_response(error="Invalid action or parameters", status=400)
        except Exception as e:
            logging.error(f"Failed to manage process: {e}")
            return make_response(error=f"Failed to {action} process", status=500)

@api_bp.route("/get_ip_info", methods=["POST"])
def get_ip_info():
    data = request.json
    ip = data.get("ip", request.remote_addr)
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return make_response(data=response.json())
        return make_response(error="Failed to fetch IP information", status=500)
    except Exception as e:
        logging.error(f"Failed to fetch IP info: {e}")
        return make_response(error=str(e), status=500)

@api_bp.route("/firewall_rules", methods=["GET", "POST"])
def manage_firewall_rules():
    if request.method == "GET":
        try:
            rules = FirewallRule.query.all()
            return make_response(data=[rule.to_dict() for rule in rules])
        except Exception as e:
            logging.error(f"Failed to fetch firewall rules: {e}")
            return make_response(error="Failed to fetch rules", status=500)
    elif request.method == "POST":
        data = request.json
        try:
            rule = FirewallRule(
                direction=data['direction'],
                protocol=data['protocol'],
                source_ip=data.get('source_ip', 'any'),
                source_port=data.get('source_port', 'any'),
                destination_ip=data.get('destination_ip', 'any'),
                destination_port=data.get('destination_port', 'any'),
            )
            db.session.add(rule)
            db.session.commit()
            return make_response(data=rule.to_dict(), status=201)
        except Exception as e:
            logging.error(f"Failed to add firewall rule: {e}")
            return make_response(error="Failed to add rule", status=500)

@api_bp.route("/logs", methods=["GET"])
def get_logs():
    try:
        logs = LogEntry.query.all()
        return make_response(data=[log.to_dict() for log in logs])
    except Exception as e:
        logging.error(f"Failed to fetch logs: {e}")
        return make_response(error="Failed to fetch logs", status=500)
