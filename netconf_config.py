
#!/usr/bin/env python3
# netconf_config.py - Configura CSR1000v via NETCONF

from ncclient import manager
import xml.dom.minidom

HOST = "192.168.56.103"
PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"
APELLIDOS = "ARANEDA_BOITANO"

def connect():
    return manager.connect(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    )

def change_hostname(m, new_name):
    config = f'''
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>{new_name}</hostname>
        </native>
    </config>'''
    return m.edit_config(target="running", config=config)

def create_loopback(m, num, ip):
    config = f'''
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>{num}</name>
                    <ip>
                        <address>
                            <primary>
                                <address>{ip}</address>
                                <mask>255.255.255.255</mask>
                            </primary>
                        </address>
                    </ip>
                </Loopback>
            </interface>
        </native>
    </config>'''
    return m.edit_config(target="running", config=config)

def main():
    print("Conectando a " + HOST + "...")
    m = connect()
    print("Conexion establecida")

    new_host = "CSR-" + APELLIDOS
    print("Cambiando hostname a " + new_host)
    change_hostname(m, new_host)
    print("Hostname actualizado")

    print("Creando loopback 11 con IP 11.11.11.11/32")
    create_loopback(m, 11, "11.11.11.11")
    print("Loopback 11 creada")

    m.close_session()
    print("Sesion NETCONF cerrada")

if __name__ == "__main__":
    main()
