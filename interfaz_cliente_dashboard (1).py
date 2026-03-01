import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import socket, ssl, threading, platform

# --------------------- Configuración inicial ---------------------
HOST = "127.0.0.1"  # Cambia a IP remota si no es localhost
PORT = 5000
CERT_FILE = "cert.pem"

# Variables globales
cliente = None
procesos = []

# --------------------- Función de conexión segura ---------------------
def conectar_servidor(usuario, password):
    global cliente
    try:
        contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        contexto.load_verify_locations(CERT_FILE)
        contexto.check_hostname = False
        contexto.verify_mode = ssl.CERT_REQUIRED

        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente = contexto.wrap_socket(raw_socket, server_hostname=HOST)
        cliente.connect((HOST, PORT))

        # Login
        cliente.recv(1024)  # USUARIO:
        cliente.send(usuario.encode('utf-8'))
        cliente.recv(1024)  # PASSWORD:
        cliente.send(password.encode('utf-8'))

        resp = cliente.recv(1024).decode('utf-8')
        if "AUTH_FAIL" in resp:
            messagebox.showerror("Login fallido", "Usuario o contraseña incorrectos")
            cliente.close()
            return False
        log_text.insert(tk.END, f"[INFO] {resp}\n")
        return True
    except Exception as e:
        messagebox.showerror("Error conexión", f"No se pudo conectar al servidor: {e}")
        return False

# --------------------- Función para enviar comando ---------------------
def enviar_comando(cmd):
    if not cliente:
        log_text.insert(tk.END, "[ERROR] No estás conectado\n")
        return
    if not cmd:
        return
    try:
        cliente.send(cmd.encode('utf-8'))
        log_text.insert(tk.END, f"[ENVÍO] {cmd}\n")
        respuesta = cliente.recv(4096).decode('utf-8')
        log_text.insert(tk.END, f"[SERVIDOR] {respuesta}\n")
        log_text.see(tk.END)
        if cmd == "listar_procesos":
            actualizar_tabla_procesos(respuesta)
    except Exception as e:
        log_text.insert(tk.END, f"[ERROR] {e}\n")

# --------------------- Función para actualizar tabla de procesos ---------------------
def actualizar_tabla_procesos(respuesta):
    procesos.clear()
    tabla_procesos.delete(*tabla_procesos.get_children())
    lineas = respuesta.splitlines()
    for l in lineas[1:]:  # Saltamos cabecera si hay
        partes = l.split()
        if len(partes) >= 2:
            pid = partes[0]
            nombre = partes[1]
            estado = "RUNNING" if len(partes) > 2 else "STOPPED"
            cpu = partes[2] if len(partes) > 2 else "0"
            ram = partes[3] if len(partes) > 3 else "0"
            procesos.append({"pid": pid, "nombre": nombre, "estado": estado, "cpu": cpu, "ram": ram})
            tabla_procesos.insert("", "end", values=(pid, nombre, estado, cpu, ram))

# --------------------- Funciones botones rápidos ---------------------
def servicio_listar():
    enviar_comando("listar_procesos")

def servicio_info():
    enviar_comando("info_sistema")

def servicio_echo():
    enviar_comando("echo Hola desde GUI")

# --------------------- Inicio de interfaz ---------------------
root = tk.Tk()
root.title("Cliente Seguro - Dashboard de Procesos")
root.geometry("1000x650")
root.configure(bg="#f0f0f0")

# --------------------- Panel comandos ---------------------
frame_cmd = tk.LabelFrame(root, text="Comandos manuales", bg="#ffffff", padx=10, pady=10)
frame_cmd.pack(fill="x", padx=20, pady=10)

entry_cmd = tk.Entry(frame_cmd, width=80)
entry_cmd.pack(side="left", padx=5)

tk.Button(frame_cmd, text="Enviar", bg="#4CAF50", command=lambda: enviar_comando(entry_cmd.get())).pack(side="left", padx=5)

# --------------------- Panel servicios rápidos ---------------------
frame_serv = tk.LabelFrame(root, text="Servicios rápidos", bg="#ffffff", padx=10, pady=10)
frame_serv.pack(fill="x", padx=20, pady=10)

tk.Button(frame_serv, text="Listar procesos", bg="#2196F3", command=servicio_listar).pack(side="left", padx=5)
tk.Button(frame_serv, text="Info Sistema", bg="#FF9800", command=servicio_info).pack(side="left", padx=5)
tk.Button(frame_serv, text="Echo", bg="#4CAF50", command=servicio_echo).pack(side="left", padx=5)

# --------------------- Panel tabla de procesos ---------------------
frame_tabla = tk.LabelFrame(root, text="Procesos", bg="#ffffff", padx=10, pady=10)
frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

cols = ("PID", "Nombre", "Estado", "CPU %", "RAM")
tabla_procesos = ttk.Treeview(frame_tabla, columns=cols, show="headings")
for c in cols:
    tabla_procesos.heading(c, text=c)
tabla_procesos.pack(fill="both", expand=True)

# --------------------- Panel registro ---------------------
frame_log = tk.LabelFrame(root, text="Registro de Actividades", bg="#ffffff", padx=10, pady=10)
frame_log.pack(fill="both", expand=True, padx=20, pady=10)

log_text = tk.Text(frame_log, height=10)
log_text.pack(fill="both", expand=True)

# --------------------- Pedir login ---------------------
usuario = simpledialog.askstring("Login", "Usuario:", parent=root)
password = simpledialog.askstring("Login", "Contraseña:", parent=root, show='*')

if usuario and password:
    conectado = conectar_servidor(usuario, password)
    if not conectado:
        root.destroy()
else:
    root.destroy()

# --------------------- Ejecutar GUI ---------------------
root.mainloop()
