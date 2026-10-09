#!/usr/bin/env python3
"""Multi-threaded TCP port scanner."""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from colorama import Fore, Style, init

init(autoreset=True)


def parse_port_range(value: str) -> tuple[int, int]:
    """Parse 'start-end' or a single port into a validated (start, end) tuple."""
    try:
        if "-" in value:
            start, end = (int(p) for p in value.split("-", 1))
        else:
            start = end = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid port range: '{value}' (use e.g. 1-1024)")

    if not (1 <= start <= 65535 and 1 <= end <= 65535):
        raise argparse.ArgumentTypeError("Ports must be between 1 and 65535")
    if start > end:
        raise argparse.ArgumentTypeError("Start port must be <= end port")
    return start, end


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-threaded TCP port scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument(
        "-p", "--ports", type=parse_port_range, default=(1, 1024),
        help="Port range to scan, e.g. 1-1024 or 80 (default: 1-1024)",
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=100,
        help="Number of worker threads (default: 100)",
    )
    parser.add_argument(
        "--timeout", type=float, default=1.0,
        help="Socket timeout in seconds (default: 1.0)",
    )
    return parser.parse_args()


def resolve_target(target: str) -> str:
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{Fore.RED}[-] Could not resolve host: {target}")
        sys.exit(1)


def get_service_name(port: int) -> str:
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def scan_port(ip: str, port: int, timeout: float) -> int | None:
    """Return the port if open, otherwise None."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((ip, port)) == 0:
                return port
    except (socket.timeout, ConnectionRefusedError):
        pass
    except OSError as exc:
        print(f"{Fore.YELLOW}[!] Port {port}: {exc}")
    return None


def main() -> None:
    args = parse_args()
    start_port, end_port = args.ports

    if args.threads < 1:
        print(f"{Fore.RED}[-] Thread count must be at least 1")
        sys.exit(1)

    ip = resolve_target(args.target)

    print(f"{Fore.CYAN}{'=' * 50}")
    print(f"{Fore.CYAN}[*] Target   : {args.target} ({ip})")
    print(f"{Fore.CYAN}[*] Ports    : {start_port}-{end_port}")
    print(f"{Fore.CYAN}[*] Threads  : {args.threads}")
    print(f"{Fore.CYAN}[*] Started  : {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"{Fore.CYAN}{'=' * 50}")

    open_ports: list[int] = []
    start_time = datetime.now()

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = [
                executor.submit(scan_port, ip, port, args.timeout)
                for port in range(start_port, end_port + 1)
            ]
            for future in as_completed(futures):
                port = future.result()
                if port is not None:
                    open_ports.append(port)
                    print(f"{Fore.GREEN}[+] Port {port:<5} OPEN   ({get_service_name(port)})")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted by user")
        sys.exit(130)

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"{Fore.CYAN}{'=' * 50}")
    if open_ports:
        ports_str = ", ".join(map(str, sorted(open_ports)))
        print(f"{Style.BRIGHT}{Fore.GREEN}[+] {len(open_ports)} open port(s): {ports_str}")
    else:
        print(f"{Fore.RED}[-] No open ports found")
    print(f"{Fore.CYAN}[*] Scan completed in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
