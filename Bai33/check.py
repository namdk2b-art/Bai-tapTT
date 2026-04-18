import subprocess
import re
from collections import Counter
from datetime import datetime, timedelta
import socket
import time

log_file = "/var/log/nginx/access.log"
threshold = 120
set_name = "blacklist_dos"
list_bot = ['googlebot.com', 'bingbot.com', 'facebookbot.com']

socket.setdefaulttimeout(5)

def verify_bot(ip):
    try:
        #Reverse DNS
        hostname, _, _ = socket.gethostbyaddr(ip)
        hostname = hostname.lower()
        #kiem tra bot
        legit_name = any(keyword in hostname for keyword in list_bot)
        if legit_name:
            #chong gia user agent
            ip_confirmed = socket.gethostbyname(hostname)
            return ip_confirmed == ip
    except (socket.herror, socket.gaierror):
        return False
    return False 

def check():
    start_time = time.time()

    now = datetime.now()
    second = now - timedelta(seconds= 60)
    time_str = second.strftime("%d/%b/%Y:%H:%M")

    ip_counts = Counter()

    try:
        raw_log = subprocess.check_output(["tail", "-n", "20000", log_file]).decode("utf-8 ")

        for line in raw_log.splitlines():
            if time_str in line and "GET" in line:
                match = re.search(r'^(\S+)', line)
                if match:
                    ip = match.group(1)
                    ip_counts[ip] += 1
    except Exception as e:
        print(f"Lỗi: {e}")
        return
    for ip, count in ip_counts.items():
        if count > threshold:
            if verify_bot(ip):
                print(f"Boq qua bot: {ip}")
                continue
            print(f"[Block] IP: {ip} - Request: {count}")
            subprocess.run(["sudo", "ipset", "add", set_name, ip], stderr=subprocess.DEVNULL)
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("-" *30)
    print(f"Thời gian chạy: {execution_time:.2f} giây")
if __name__ == "__main__":
    check()
                
                

