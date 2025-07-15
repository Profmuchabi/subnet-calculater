import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ipaddress

# CIDR to Subnet Mask table for IPv4
CIDR_TABLE = [(i, str(ipaddress.IPv4Network(f"0.0.0.0/{i}").netmask)) for i in range(1, 33)]

class SubnetCalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Subnet Calculator")
        self.geometry("600x500")
        self.configure(bg="#f4f6fb")
        self.iconbitmap('')  # Add your .ico file path here if you have one
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[10, 5])
        style.configure('TButton', font=('Segoe UI', 11), padding=6)
        style.configure('TLabel', font=('Segoe UI', 11), background='#f4f6fb')
        style.configure('TEntry', font=('Segoe UI', 11))

        notebook = ttk.Notebook(self)
        notebook.pack(expand=1, fill='both', padx=10, pady=10)

        # IPv4 Tab
        ipv4_tab = ttk.Frame(notebook)
        self.create_ipv4_tab(ipv4_tab)
        notebook.add(ipv4_tab, text='IPv4')

        # IPv6 Tab
        ipv6_tab = ttk.Frame(notebook)
        self.create_ipv6_tab(ipv6_tab)
        notebook.add(ipv6_tab, text='IPv6')

        # CIDR Table Tab
        cidr_tab = ttk.Frame(notebook)
        self.create_cidr_tab(cidr_tab)
        notebook.add(cidr_tab, text='CIDR Table')

    def create_ipv4_tab(self, tab):
        label = ttk.Label(tab, text="Enter IPv4 network (e.g., 192.168.1.0/24):")
        label.pack(pady=(20, 5))
        self.ipv4_entry = ttk.Entry(tab, width=30)
        self.ipv4_entry.pack(pady=5)
        calc_btn = ttk.Button(tab, text="Calculate", command=self.calculate_ipv4)
        calc_btn.pack(pady=10)
        list_btn = ttk.Button(tab, text="List Usable IPs", command=self.list_ipv4_ips)
        list_btn.pack(pady=5)
        # --- Subnet Mask to CIDR ---
        mask_label = ttk.Label(tab, text="Or enter Subnet Mask (e.g., 255.255.255.128):")
        mask_label.pack(pady=(20, 5))
        self.mask_entry = ttk.Entry(tab, width=20)
        self.mask_entry.pack(pady=5)
        mask_btn = ttk.Button(tab, text="Show Info for Subnet Mask", command=self.calculate_from_mask)
        mask_btn.pack(pady=5)
        # --- Results ---
        self.ipv4_result = scrolledtext.ScrolledText(tab, height=10, font=('Consolas', 10))
        self.ipv4_result.pack(pady=10, fill='both', expand=True)

    def create_ipv6_tab(self, tab):
        label = ttk.Label(tab, text="Enter IPv6 network (e.g., 2001:db8::/64):")
        label.pack(pady=(20, 5))
        self.ipv6_entry = ttk.Entry(tab, width=40)
        self.ipv6_entry.pack(pady=5)
        calc_btn = ttk.Button(tab, text="Calculate", command=self.calculate_ipv6)
        calc_btn.pack(pady=10)
        self.ipv6_result = scrolledtext.ScrolledText(tab, height=10, font=('Consolas', 10))
        self.ipv6_result.pack(pady=10, fill='both', expand=True)

    def create_cidr_tab(self, tab):
        label = ttk.Label(tab, text="CIDR to Subnet Mask Table (IPv4)")
        label.pack(pady=(20, 5))
        table = ttk.Treeview(tab, columns=("CIDR", "Mask"), show='headings', height=20)
        table.heading("CIDR", text="CIDR")
        table.heading("Mask", text="Subnet Mask")
        for cidr, mask in CIDR_TABLE:
            table.insert('', 'end', values=(f"/{cidr}", mask))
        table.pack(pady=10, fill='both', expand=True)

    def calculate_ipv4(self):
        net_str = self.ipv4_entry.get().strip()
        self.ipv4_result.delete('1.0', tk.END)
        try:
            net = ipaddress.IPv4Network(net_str, strict=False)
            result = (
                f"IPv4 Network: {net}\n"
                f"Subnet Mask: {net.netmask}\n"
                f"Network Address: {net.network_address}\n"
                f"Broadcast Address: {net.broadcast_address}\n"
                f"Number of Host bits: {32 - net.prefixlen}\n"
                f"Number of usable hosts: {max(net.num_addresses - 2, 0)}\n"
            )
            self.ipv4_result.insert(tk.END, result)
        except Exception as e:
            self.ipv4_result.insert(tk.END, f"Error: {e}")

    def list_ipv4_ips(self):
        net_str = self.ipv4_entry.get().strip()
        self.ipv4_result.delete('1.0', tk.END)
        try:
            net = ipaddress.IPv4Network(net_str, strict=False)
            if net.num_addresses > 65536:
                self.ipv4_result.insert(tk.END, "Too many IPs to display! (Limit: 65536)")
                return
            hosts = list(net.hosts())
            if not hosts:
                self.ipv4_result.insert(tk.END, "No usable hosts in this subnet.")
            else:
                self.ipv4_result.insert(tk.END, '\n'.join(str(ip) for ip in hosts))
        except Exception as e:
            self.ipv4_result.insert(tk.END, f"Error: {e}")

    def calculate_from_mask(self):
        mask_str = self.mask_entry.get().strip()
        self.ipv4_result.delete('1.0', tk.END)
        try:
            # Find prefix length from mask
            try:
                prefix = ipaddress.IPv4Network(f'0.0.0.0/{mask_str}').prefixlen
            except Exception:
                self.ipv4_result.insert(tk.END, f"Invalid subnet mask: {mask_str}")
                return
            # Show info for this mask
            num_hosts = max(2**(32 - prefix) - 2, 0)
            example_network = f"192.168.0.0/{prefix}"
            net = ipaddress.IPv4Network(example_network, strict=False)
            result = (
                f"Subnet Mask: {mask_str}\n"
                f"CIDR Prefix: /{prefix}\n"
                f"Number of usable hosts: {num_hosts}\n"
                f"Example Network: {net.network_address}/{prefix}\n"
                f"Broadcast Address: {net.broadcast_address}\n"
                f"First Usable IP: {list(net.hosts())[0] if num_hosts > 0 else 'N/A'}\n"
                f"Last Usable IP: {list(net.hosts())[-1] if num_hosts > 0 else 'N/A'}\n"
            )
            self.ipv4_result.insert(tk.END, result)
        except Exception as e:
            self.ipv4_result.insert(tk.END, f"Error: {e}")

    def calculate_ipv6(self):
        net_str = self.ipv6_entry.get().strip()
        self.ipv6_result.delete('1.0', tk.END)
        try:
            net = ipaddress.IPv6Network(net_str, strict=False)
            result = (
                f"IPv6 Network: {net}\n"
                f"Prefix Length: /{net.prefixlen}\n"
                f"Network Address: {net.network_address}\n"
                f"Number of Host bits: {128 - net.prefixlen}\n"
                f"Number of addresses: {net.num_addresses}\n"
            )
            self.ipv6_result.insert(tk.END, result)
        except Exception as e:
            self.ipv6_result.insert(tk.END, f"Error: {e}")

if __name__ == "__main__":
    app = SubnetCalculatorGUI()
    app.mainloop() 