
#!/usr/bin/env python3
# netmiko_eigrp.py - Configura EIGRP con passive-interface usando af-interface

from netmiko import ConnectHandler

DEVICE = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.103',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'cisco123!',
}

AS = 100

def main():
    conn = ConnectHandler(**DEVICE)
    conn.enable()

    print("=== CONFIGURANDO EIGRP NOMBRADO ===")
    commands = [
        "ipv6 unicast-routing",
        "router eigrp NAMED",
        f"address-family ipv4 autonomous-system {AS}",
        "network 192.168.56.0",
        "af-interface GigabitEthernet1",
        "passive-interface",
        "exit-af-interface",
        "exit-address-family",
        f"address-family ipv6 autonomous-system {AS}",
        "af-interface GigabitEthernet1",
        "passive-interface",
        "exit-af-interface",
        "exit-address-family",
        "exit",
    ]
    output = conn.send_config_set(commands)
    print(output)

    print("\n=== SHOW RUNNING-CONFIG | SECTION EIGRP ===")
    result = conn.send_command("show running-config | section eigrp")
    print(result)

    print("\n=== SHOW IP INTERFACE BRIEF ===")
    result = conn.send_command("show ip interface brief")
    print(result)

    print("\n=== SHOW RUNNING-CONFIG (primeras líneas) ===")
    result = conn.send_command("show running-config")
    print(result[:800] + "..." if len(result) > 800 else result)

    print("\n=== SHOW VERSION (primeras líneas) ===")
    result = conn.send_command("show version")
    print(result[:600] + "..." if len(result) > 600 else result)

    conn.disconnect()
    print("\nDesconectado.")

if __name__ == "__main__":
    main()
