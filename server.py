import socket
import math

adam6050_coils = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

def main():
    # data = b'\x00\x00\x00\x00\x00\x06\x01\x05\x00\x10\xff\x00'
    # construct_force_single_coil_status(data)
    start_server()

def start_server():
    HOST = "0.0.0.0"
    PORT = 502

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1)
        print(f"Listening on {HOST}:{PORT}")
        while True:
            try:
                conn, addr = s.accept()
            except (BlockingIOError, TimeoutError):
                continue
            try:
                with conn:
                    print(f"[+] Connected by {addr}")
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            print("[-] Client disconnected (clean)")
                            break
                        hex_str = " ".join(f"{b:02x}" for b in data)
                        print(f"[!] {len(data)} bytes: {hex_str}")
                        process_recv_data(data, conn)
            except KeyboardInterrupt:
                raise
            except ConnectionResetError:
                print(f"[-] RST from {addr} before any data")
            except BrokenPipeError:
                print(f"[-] Pipe broken by {addr}")
            except Exception as e:
                print(f"[-] Error from {addr}: {e}")

def process_recv_data(data, conn):
    hex_list = []
    for b in data:
        hex_char = f"{b:02x}"
        hex_list.append(hex_char)

    if hex_list[7] == "01":
        conn.send(construct_readcoil_status(data))
    elif hex_list[7] == "02":
        conn.send(construct_readcoil_status(data))
    elif hex_list[7] == "03":
        pass
    elif hex_list[7] == "04":
        pass
    elif hex_list[7] == "05":
        conn.send(construct_force_single_coil_status(data))
    elif hex_list[7] == "06":
        conn.send(construct_force_multi_coils_status(data))

def construct_readcoil_status(hex_list):
    dec_list = list(hex_list)

    coil_list = []
    response_bytes = b''

    start_index = dec_list[9]
    total_points = dec_list[11]

    total = min(total_points, len(adam6050_coils))
    for i in range(start_index, total):
        coil_list.append(adam6050_coils[i])

    for k in range(0, 8):
        response_bytes += hex_list[k].to_bytes(1, byteorder = 'big')

    coils_len = len(coil_list)
    byte_size = math.ceil(coils_len / 8)
    byte_array = bytearray(byte_size)

    for j in range(coils_len):
        if coil_list[j]:
            byte_idx = j // 8
            bit_pos = j % 8
            byte_array[byte_idx] |= (1 << bit_pos)

    msg_len_bytes = len(byte_array).to_bytes(1, byteorder = 'big')

    return response_bytes + msg_len_bytes + bytes(byte_array)

def construct_force_single_coil_status(hex_list):
    dec_list = list(hex_list)

    if dec_list[9] >= len(adam6050_coils):
        return b''

    adam6050_coils[dec_list[9]] = 1
    print(adam6050_coils)
    return hex_list

def construct_force_multi_coils_status(hex_list):
    dec_list = list(hex_list)

    return hex_list

if __name__ == "__main__":
    main()
