# subnet_calculator.py
import ipaddress
import os

def calculate_ipv4(network_str):
    try:
        net = ipaddress.IPv4Network(network_str, strict=False)
        print(f"\n📌 IPv4 Network: {net}")
        print(f"Subnet Mask: {net.netmask}")
        print(f"Network Address: {net.network_address}")
        print(f"Broadcast Address: {net.broadcast_address}")
        print(f"Number of Host bits: {32 - net.prefixlen}")
        print(f"Number of usable hosts: {net.num_addresses - 2}")
    except Exception as e:
        print(f"Error: {e}")

def calculate_ipv6(network_str):
    try:
        net = ipaddress.IPv6Network(network_str, strict=False)
        print(f"\n📌 IPv6 Network: {net}")
        print(f"Prefix Length: /{net.prefixlen}")
        print(f"Network Address: {net.network_address}")
        print(f"Number of Host bits: {128 - net.prefixlen}")
        print(f"Number of addresses: {net.num_addresses}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("==== Subnet Calculator ====")
    ip_type = input("IPv4 or IPv6? (v4/v6): ").strip().lower()

    if ip_type == 'v4':
        network = input("Enter IPv4 network (e.g., 192.168.1.0/24): ").strip()
        calculate_ipv4(network)
    elif ip_type == 'v6':
        network = input("Enter IPv6 network (e.g., 2001:db8::/64): ").strip()
        calculate_ipv6(network)
    else:
        print("Invalid option. Please choose 'v4' or 'v6'.")

if __name__ == "__main__":
    main()

    # Run the GUI app
    os.chdir("C:\\Users\\ADMIN\\Desktop\\SUBNET\\dist")
    os.system("pyinstaller --onefile --windowed subnet_calculator_gui.py")
