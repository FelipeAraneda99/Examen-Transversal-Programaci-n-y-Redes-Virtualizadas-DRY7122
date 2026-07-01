
#!/usr/bin/env python3
# integrantes.py - Muestra los integrantes del grupo

integrantes = [
    "Felipe Araneda",
    "Angelo Boitano"
]

print("=== Integrantes del Grupo ===")
for i, nombre in enumerate(integrantes, 1):
    print(f"{i}. {nombre}")
