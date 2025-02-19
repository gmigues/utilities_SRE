#script para descubrir los dispositivos en la red

import os
import sys
import time
import socket
import subprocess
import platform
import threading
import netifaces as ni
import ipaddress
import json

# Variables globales
ip = ''
mask = ''
ip_range = []
devices = []
threads = []
lock = threading.Lock()

# Función para obtener la dirección IP y la máscara de red

def get_ip_and_mask():
    global ip
    global mask

    # Obtener la interfaz de red
    gateway = ni.gateways()['default'][ni.AF_INET][1]
    interface = ni.gateways()['default'][ni.AF_INET][1]

    # Obtener la dirección IP y la máscara de red
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    mask = ni.ifaddresses(interface)[ni.AF_INET][0]['netmask']

    print('IP:', ip)
    print('Máscara:', mask)

# Función para obtener el rango de direcciones IP
    
def get_ip_range():
    global ip
    global mask
    global ip_range

    # Obtener la dirección de red y la dirección de broadcast
    network = ipaddress.IPv4Network(ip + '/' + mask, False)
    network_address = network.network_address
    broadcast_address = network.broadcast_address

    # Obtener el rango de direcciones IP
    ip_range = list(network.hosts())
    ip_range.insert(0, network_address)
    ip_range.append(broadcast_address)

    #print('Rango de direcciones IP:', ip_range)

# Función para escanear una dirección IP
    
def scan(ip):
    global devices

    # Realizar un ping a la dirección IP
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', ip]
    response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Verificar si el dispositivo está activo
    if response == 0:
        hostname = ''
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = ip

        with lock:
            devices.append({'ip': ip, 'hostname': hostname})

# Función para escanear un rango de direcciones IP
            
def scan_ip_range():
    global ip_range
    global threads

    # Crear un hilo para cada dirección IP
    for ip in ip_range:
        thread = threading.Thread(target=scan, args=(str(ip),))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

# Función para guardar los dispositivos en un archivo JSON
        
def save_to_file():
    global devices

    with open('devices.json', 'w') as file:
        json.dump(devices, file, indent=4)

    print('Dispositivos guardados en el archivo devices.json')

# Función principal
    
def main():
    get_ip_and_mask()
    get_ip_range()
    scan_ip_range()
    save_to_file()

if __name__ == '__main__':
    main()
  
