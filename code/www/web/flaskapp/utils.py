import logging
import re
import subprocess
import requests

class Utils:

    @staticmethod
    def log_ip_access(endpoint_name):
        """Logs visitor IP access for a given endpoint."""
        user_ip = (
            request.headers.get("X-Real-IP")
            or request.headers.get("X-Forwarded-For")
            or request.remote_addr
        )
        if user_ip:
            logging.info(f"Visitor with IP {user_ip} accessed {endpoint_name}")
        else:
            logging.warning(f"Unable to retrieve visitor's IP address for {endpoint_name}")

    @staticmethod
    def is_valid_ip(ip):
        """Validates IP address format."""
        ip_regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        return bool(re.match(ip_regex, ip))

    @staticmethod
    def execute_whois(ip):
        """Executes a WHOIS lookup for an IP and returns the result."""
        try:
            result = subprocess.run(
                ["whois", ip], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"WHOIS lookup failed for IP {ip}: {e}")
            return f"Error: {str(e)}"


    @staticmethod
    def network_activity():
        net_io = psutil.net_io_counters()
        return f"Bytes Sent: {net_io.bytes_sent}, Bytes Received: {net_io.bytes_recv}"

    @staticmethod
    def detect_intrusions(suspicious_ips=["192.168.1.100"], suspicious_ports=[22, 23]):
        intrusions = []
        try:
            for conn in psutil.net_connections():
                if conn.raddr:
                    remote_ip = conn.raddr.ip
                    remote_port = conn.raddr.port
                    if remote_ip in suspicious_ips or remote_port in suspicious_ports:
                        intrusions.append(f"IP: {remote_ip}, Port: {remote_port}")
        except psutil.AccessDenied:
            return "Access Denied to network connections."
        except Exception as e:
            return f"Error checking intrusions: {e}"

        if intrusions:
            alert_message = f"Suspicious activity detected from: {', '.join(intrusions)}"
            logging.warning(alert_message)
            return alert_message
        return "No suspicious activity detected."
