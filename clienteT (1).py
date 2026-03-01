import socket

#Config

HOST = '0.0.0.0' 
PORT = 22

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((HOST, PORT))
        print(f"--- CONECTADO AL SERVIDOR {HOST}:{PORT} ---")
        print("Escribe 'salir' para terminar la conexión.")
        print("Comandos disponibles: listar_procesos, info_sistema, echo [mensaje]")
        
        while True:
            try:
                mensaje = input("\nUsuario> ")
            except EOFError:
                break
            
            if mensaje.strip() == "":
                continue
            
            cliente.send(mensaje.encode('utf-8'))
            
            if mensaje == 'salir':
                break
            respuesta = cliente.recv(4096).decode('utf-8')
            print(f"\nRespuesta del Servidor: \n{'-'*20}\n{respuesta}\n{'-'*20}")
            
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        cliente.close()
        print("Conexión cerrada.")
        
if __name__ == "__main__":
    iniciar_cliente()
