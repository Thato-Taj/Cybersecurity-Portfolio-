import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

closed_ports = 0
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

target = input("Enter the host to scan (IP or Domain): ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Hostname could not be resolved")
    exit()

print(f"Starting Scan on {target_ip}")
print("Scanning ports from 1 to 1024")  # smaller range for demo

start_time = datetime.now()

def grab_banner(sock):
    try:
        sock.settimeout(1)
        return sock.recv(1024).decode().strip()
    except:
        return None

def scan_port(port):
    global closed_ports
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target_ip, port))

        if result == 0:
            service = common_ports.get(port, "Unknown")
            banner = grab_banner(s)
            if banner:
                service += f" ({banner})"
            print(f"[OPEN] Port {port} → {service}")
        else:
            # Try to check if filtered or just closed
            try:
                s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s2.settimeout(1)
                s2.connect((target_ip, port))
                s2.close()
                print(f"[CLOSED] Port {port}")
            except socket.timeout:
                print(f"[FILTERED] Port {port} (No response - firewall?)")
            except ConnectionRefusedError:
                print(f"[CLOSED] Port {port}")
            closed_ports += 1
        s.close()
    except:
        pass

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(1, 1025))

end_time = datetime.now()
print(f"Scanning completed in {end_time - start_time}")
print(f"Open ports: {1024 - closed_ports}")
