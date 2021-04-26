import socket
import threading
import concurrent.futures
from IPy import IP  # not a standard library; install required
import colorama
from colorama import Fore

colorama.init(autoreset=True)
thread_lock = threading.Lock()  # thread synchronization
count = 0  # set count as global variable and initialize it to 0


# this function validates the IP address and converts a hostname into IP address.
def validate_target(ipa):
    try:
        IP(ipa)
        return ipa
    except ValueError:
        return socket.gethostbyname(ipa)


# this function performs socket connection and banner grabbing
def portscan(_ipaddr, _port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        try:
            s.connect((_ipaddr, _port))
            try:
                banner = get_banner(s)
            except (socket.timeout, socket.error):
                pass
                # with thread_lock:
                #     print(f'[+] [{_port}] is {Fore.GREEN}Open')
            else:
                with thread_lock:
                    print(f'[+] [{_port}] is {Fore.GREEN}Open' + f': {Fore.YELLOW}{str(banner.decode().strip())}')
        except (ConnectionRefusedError, AttributeError, OSError):
            pass


# get banner
def get_banner(s):
    return s.recv(1024)  # receive response


# initiate threaded scanning
def initiate_scan(host):
    ip_addr = validate_target(host)
    global count
    print(f'\n[-_{count} Scanning Target] {host}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1, 65536):
            executor.submit(portscan, ip_addr, port)
    count += 1  # increment count after every iteration


targets = input('[+] Enter target(s) to scan(split multiple targets with ,): ')
if ',' in targets:
    for ip in targets.split(','):
        initiate_scan(ip.strip())  # for multiple targets
else:
    initiate_scan(targets)  # for a single target
count = 0  # reset the global variable

colorama.deinit()
