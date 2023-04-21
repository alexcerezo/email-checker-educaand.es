import dns.resolver
import smtplib
import socket
import time
import random

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

# Nombre del archivo que contiene la lista de correos electrónicos
nombre_archivo = 'emails.txt'

# Leer el contenido del archivo y dividirlo en una lista de correos electrónicos
with open(nombre_archivo, 'r') as archivo:
    contenido = archivo.read().strip()
    email_list = contenido.split('\n')

# Verificación de cada dirección de correo electrónico en la lista
for email in email_list:
    if check_email(email):
        print(f"{email} existe")
    else:
        print(f"{email} no existe")
