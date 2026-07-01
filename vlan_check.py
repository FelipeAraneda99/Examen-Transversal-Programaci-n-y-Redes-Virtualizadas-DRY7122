
#!/usr/bin/env python3
# vlan_check.py - Verifica rango de VLAN (normal o extendido)

while True:
    vlan = input("Ingrese el numero de VLAN (o 's' para salir): ")
    
    if vlan.lower() == 's':
        print("Hasta luego!")
        break
    
    try:
        num = int(vlan)
        if 1 <= num <= 1005:
            print(f"VLAN {num} -> RANGO NORMAL (1-1005)")
        elif 1006 <= num <= 4094:
            print(f"VLAN {num} -> RANGO EXTENDIDO (1006-4094)")
        else:
            print(f"VLAN {num} -> FUERA DE RANGO (1-4094)")
    except ValueError:
        print("Error: Ingrese un numero valido")
    print()
