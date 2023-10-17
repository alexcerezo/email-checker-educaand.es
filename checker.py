import dns.resolver
import smtplib
import socket
import time
import random

def generar_usuario():
    nombre = input("Nombre: ")
    apellido1 = input("Primer apellido: ")
    apellido2 = input("Segundo apellido: ")
    inicial = nombre[0]
    primera_parte = apellido1[:3]
    segunda_parte = apellido2[:3]
    usuario = (inicial + primera_parte + segunda_parte).lower()
    return usuario

def generar_correos():
    usuario = generar_usuario()
    with open('emails.txt', 'w') as f:
        for i in range(1000):
            correo = usuario + '{:03d}'.format(i) + '@g.educaand.es'
            f.write(correo + '\n')
        for dia in range(1, 32):
            for mes in range(1, 13):
                if mes == 2 and dia > 29:
                    continue
                elif mes in (4, 6, 9, 11) and dia > 30:
                    continue
                correo = usuario + '{:02d}{:02d}'.format(dia, mes) + '@g.educaand.es'
                f.write(correo + '\n')
    print("Correos exportados correctamente.")

def verificar_correos():
    with open('emails.txt', 'r') as archivo:
        contenido = archivo.read().strip()
        email_list = contenido.split('\n')
    verificados = []
    for email in email_list:
        if check_email(email):
            print(f"{email} existe")
            verificados.append(email)
        else:
            print(f"{email} no existe")
    if verificados:
        with open('Verificados.txt', 'w') as f:
            for email in verificados:
                f.write(email + '\n')
        print("Correos verificados exportados correctamente.")
    else:
        print("No se encontraron correos verificados.")


def check_email(email):
    # Dividir la dirección de correo electrónico en usuario y dominio
    username, domain = email.split('@')

    # Búsqueda del servidor MX del dominio
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange.to_text().strip('.')
    except dns.resolver.NoAnswer:
        time.sleep(random.uniform(1, 3))
        return False

    # Conexión al servidor MX y verificación de la dirección de correo electrónico
    try:
        with smtplib.SMTP(timeout=10) as server:
            server.connect(mx_record)
            server.helo(socket.gethostname())
            server.mail('test@test.com')
            code, _ = server.rcpt(str(email))
            return code == 250
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, socket.gaierror):
        time.sleep(random.uniform(1, 3))
        return False

while True:
    opcion = input("\nSelecciona una opción:\n1. Generar correos\n2. Verificar correos\n3. Salir\n")
    if opcion == "1":
        generar_correos()
    elif opcion == "2":
        verificar_correos()
    elif opcion == "3":
        break
    else:
        print("Opción no válida. Introduce un número del 1 al 3.")
