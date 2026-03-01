import socket
import threading
import subprocess
import platform

# Config 

HOST = '0.0.0.0'
PORT = 22

def ejecutar_comand(comando):
    try:
        sistema = platform.system()
        
        if comando == 'listar_procesos':
            cmd_sys = 'tasklist' if sistema == 'Windows' else 'ps -e | head -n 10'
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
    
def manejar_cliente(conn, addr) :
    print(f"[NUEVA CONEXIÓN] Cliente conectado desde {addr}")
    
    connected = True
    while connected:
        try:
            msg = conn.recv(1024).decode('utf-8').strip()
            
            if not msg or msg == 'salir':
                connected = False
                print(f"[DESCONEXIÓN] {addr} se desconectó.")
                
            print (f"[{addr}] Comando recibido: {msg}")
            
            respuesta = ejecutar_comand(msg)
            conn.send(respuesta.encode('utf-8'))
        except ConnectionResetError:
            print(f"[ERROR] Conexión perdida con {addr}")
            break
    conn.close()
    
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    
    print(f"--- SERVIDOR DE MONITOREO INICIADO ---")
    print(f"Escuchando en {HOST}:{PORT}")
    
    while True:
        conn, addr = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()
        print(f"[ACTIVOS] Conexiones activas: {threading.active_count() - 1}")
        
if __name__ == "__main__":
    iniciar_servidor()
