#!/usr/bin/env python3
import socket
import sys


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.190"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 502

    payload = b'\x00\x00\x00\x00\x00\x06\x01\x05\x00\x10\xff\x00'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(payload)
        response = s.recv(4096)

    if not response:
        print("[-] No response from server")
        return

    hex_str = " ".join(f"{b:02x}" for b in response)
    print(f"[+] Response ({len(response)} bytes): {hex_str}")


if __name__ == "__main__":
    main()
