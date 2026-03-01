import socket
import ssl
import threading
import subprocess
import platform
import hashlib
import json
import os

# Config

HOST = '0.0.0.0'
PORT = 5000
CERT = 'cert.pem'
KEY  = 'key.pem'
DB   = 'usuarios.json'

# Base de usuarios 
def cargar_usuarios():
    if not os.path.exists(DB):
        # Usuarios por defecto: admin/admin123 y usuario1/pass1
        datos = {
            "admin":    hashlib.sha256("admin123".encode()).hexdigest(),
            "usuario1": hashlib.sha256("pass1".encode()).hexdigest()
        }
        with open(DB, 'w') as f:
            json.dump(datos, f, indent=4)
        print(f"[INFO] Archivo '{DB}' creado con usuarios por defecto.")
    with open(DB, 'r') as f:
        return json.load(f)
    
def verificar_credenciales(usuario, password):
    usuarios = cargar_usuarios()
    hash_pw  = hashlib.sha256(password.encode()).hexdigest()
    return usuarios.get(usuario) == hash_pw

def ejecutar_comand(comando):
    try:
        sistema = platform.system()
        
        if comando == 'listar_procesos':
            cmd_sys = 'tasklist' if sistema == 'Windows' else 'ps -e | head -n 20'
        elif comando.startswith('echo '):
            return comando[5:]
        elif comando == 'info_sistema':
            return f"Sistema: {sistema} - Release: {platform.release()}"
        else:
            return "Comando no reconocido. Comandos: listar_procesos, info_sistema, echo [txt]"
        resultado = subprocess.check_output(cmd_sys, shell=True, text=True)
        return resultado
    except Exception as e:
        return f"Error ejecutando comando: {str(e)}"
    
def manejar_cliente(conn, addr):
    print(f"\n[CONEXION] Cliente conectado desde {addr}")
    try:
        conn.send("USUARIO: ".encode('utf-8'))
        usuario = conn.recv(1024).decode('utf-8').strip()


        conn.send("PASSWORD: ".encode('utf-8'))
        password = conn.recv(1024).decode('utf-8').strip()


        if not verificar_credenciales(usuario, password):
            conn.send("AUTH_FAIL: Credenciales incorrectas. Conexion cerrada.\n".encode('utf-8'))
            print(f"[AUTH FALLIDO] Intento fallido con usuario '{usuario}' desde {addr}")
            return

        conn.send(f"AUTH_OK: Bienvenido, {usuario}!\n".encode('utf-8'))
        print(f"[AUTH OK] Usuario '{usuario}' autenticado desde {addr}")


        while True:
            datos = conn.recv(4096).decode('utf-8').strip()
            if not datos or datos == 'salir':
                print(f"[DESCONEXION] {usuario} ({addr}) se desconecto.")
                break

            print(f"[COMANDO] {usuario}@{addr} -> {datos}")
            respuesta = ejecutar_comand(datos)
            conn.send(respuesta.encode('utf-8'))

    except ConnectionResetError:
        print(f"[ERROR] Conexion perdida con {addr}")
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        conn.close()


def iniciar_servidor():

    if not os.path.exists(CERT) or not os.path.exists(KEY):
        print("[ERROR] No se encontraron cert.pem o key.pem")
        print("Genera los certificados con este comando:")
        print("  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj \"/CN=localhost\"")
        return


    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto.load_cert_chain(certfile=CERT, keyfile=KEY)

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    raw_socket.bind((HOST, PORT))
    raw_socket.listen(5)

    servidor = contexto.wrap_socket(raw_socket, server_side=True)

    print("=" * 45)
    print("   SERVIDOR SEGURO INICIADO (TLS/SSL)")
    print("=" * 45)
    print(f"  Escuchando en {HOST}:{PORT}")
    print(f"  Certificado : {CERT}")
    print(f"  Base usuarios: {DB}")
    print("=" * 45)
    print("Esperando conexiones...\n")

    while True:
        conn, addr = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.daemon = True
        hilo.start()
        print(f"[ACTIVOS] Conexiones activas: {threading.active_count() - 1}")

if __name__ == "__main__":
    iniciar_servidor()
