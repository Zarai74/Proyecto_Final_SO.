# Proyecto Final – Sistemas Operativos**  
> Ingeniería en Desarrollo de Software  
> Fecha: Febrero 2026

---

## Equipo de Desarrollo

| Nombre | Matrícula |
|--------|-----------|
| Ana María Olvera Salinas | 07200501 |
| Ana Saraí Zuñiga Esquivel | 03049128 |
| Arantza Guerrero Arellano | 02962091 |

---


## Descripción General

Este proyecto consiste en el diseño e implementación de una solución tecnológica avanzada para la **administración remota de sistemas operativos**, construida bajo una arquitectura **Cliente-Servidor** y expandida hacia un modelo de **Sistemas Distribuidos**.

El sistema permite monitorear y controlar procesos de manera remota, con seguridad TLS/SSL, soporte para entornos virtualizados (Red Hat) y una interfaz gráfica de escritorio desarrollada con Tkinter.

---
## Funcionalidades Implementadas

**Administración de Procesos**

- Listado de procesos activos

- Monitoreo de CPU

- Monitoreo de RAM

- Creación de procesos

- erminación por PID

**Comunicación en Red**

- TCP/IP

- Sockets Python

- Sockets POSIX en C

- Comunicación bidireccional

**Seguridad**

- TLS/SSL

- Certificados digitales

- Autenticación por usuario

- Firewall (firewalld)

- SSH con claves

- HTTPS con Apache

**Sistemas Distribuidos**

- Middleware de enrutamiento

- Múltiples servidores

- Desacoplamiento cliente-servidor

- Sistema de archivos distribuido (Samba)

- Modelo P2P (BitTorrent)

**Virtualización**

- Docker

- Dockerfile

- docker-compose

- Red interna entre contenedores

## Arquitectura del Sistema

```

             +-------------------+
             |     Cliente       |
             | (CLI / GUI)       |
             +---------+---------+
                       |
                       | TLS
                       |
             +---------v---------+
             |     Middleware    |
             |   (Broker Central)|
             +---------+---------+
                       |
          -----------------------------
          |                           |
  +-------v-------+           +-------v-------+
  |  Servidor 1   |           |  Servidor 2   |
  | Procesos SO   |           | Procesos SO   |
  +---------------+           +---------------+

```
## Tecnologías Utilizadas

- **Python** – Lenguaje principal de desarrollo
- **C** – Interacción de bajo nivel con el sistema operativo
- **psutil** – Monitoreo de procesos y recursos del sistema
- **subprocess** – Creación y gestión de procesos
- **Sockets TCP/IP** – Comunicación cliente-servidor
- **TLS/SSL** – Cifrado y seguridad del canal de comunicación
- **Tkinter** – Interfaz gráfica de usuario (GUI)
- **Red Hat / SELinux / Firewalld** – Entorno de virtualización y seguridad
- **uv** – Gestión del entorno de ejecución Python

---

## Estructura del Repositorio

```
proyecto-final-so/
│
├── fase1/
│   ├── servidor/          # Aplicación servidor para administración de procesos
│   ├── cliente/           # Aplicación cliente TCP/IP
│   ├── middleware/         # Capa middleware y descubrimiento de servicios
│   └── README_fase1.md
│
├── fase2/
│   ├── seguridad/          # Módulos de autenticación y cifrado TLS/SSL
│   ├── virtualizacion/     # Scripts de despliegue en Red Hat
│   ├── gui/                # Interfaz gráfica con Tkinter
│   └── README_fase2.md
│
├── docs/
│   └── so_avance_proyecto.pdf   # Documento de avance del proyecto
│
└── README.md
```

---

## Funcionalidades Principales

- Listar procesos activos con PID, nombre, CPU y memoria
- Monitoreo global de CPU y RAM en tiempo real
- Iniciar nuevos procesos de forma remota
- Terminar procesos por PID con manejo de excepciones (`AccessDenied`, `NoSuchProcess`)
- Comunicación bidireccional cliente-servidor vía TCP/IP
- Middleware para gestión de múltiples servidores distribuidos
- Autenticación de usuarios y cifrado TLS/SSL
- Dashboard gráfico con tablas dinámicas, alertas y registro de actividades

---

## Instalación y Ejecución

**Ejecutar Broker**
```bash
python3 broker.py
```
**Ejecutar Servidor**
```bash
python3 servidorFinalT.py
```
**Ejecutar Cliente**
```bash
python3 clienteFinal.py
```
**Ejecutar Interfaz Gráfica**
```bash
python3 interfaz_cliente_dashboard.py
```
**Ejecución con Docker**
```bash
docker-compose up --build
```

## Documentación

El documento completo del proyecto Incluye:
- Fundamentación teórica
- Diseño de arquitectura
- Implementación detallada por etapas
- Evidencias de pruebas y solución de problemas

---

## Conclusión

El proyecto evolucionó desde una aplicación local de administración de procesos hasta un sistema distribuido seguro, escalable y virtualizado.

Se integraron conceptos de:

- Gestión de procesos

- Redes

- Middleware

- Seguridad informática

- Sistemas distribuidos

- Virtualización

- Modelos Cliente-Servidor y P2P

Constituye una solución robusta y profesional alineada a los principios modernos de arquitectura distribuida.
