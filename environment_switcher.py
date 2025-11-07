import tkinter as tk
from tkinter import messagebox
import os
import shutil
import subprocess
import webbrowser
import time
import sys
import signal
import psutil

class EnvironmentSwitcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Masterpost.io - Selector de Entorno")
        self.processes = []
        self.current_env = tk.StringVar(value="NO DEFINIDO")
        
        # Configurar la ventana principal
        self.root.configure(bg='#f0f0f0')
        
        # Centrar la ventana
        window_width = 400
        window_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Crear la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title = tk.Label(
            self.root,
            text="Selector de Entorno",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0'
        )
        title.pack(pady=10)
        
        # Estado actual
        status_frame = tk.Frame(self.root, bg='#f0f0f0')
        status_frame.pack(pady=5)
        
        tk.Label(
            status_frame,
            text="Estado actual:",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            status_frame,
            textvariable=self.current_env,
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            fg='#1976D2'
        ).pack(side=tk.LEFT, padx=5)
        
        # Frame para botones principales
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        # Botón LOCAL
        tk.Button(
            button_frame,
            text="LOCAL",
            command=self.switch_to_local,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=10)
        
        # Botón PRODUCCIÓN
        tk.Button(
            button_frame,
            text="PRODUCCIÓN",
            command=self.switch_to_production,
            bg='#2196F3',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=10)
        
        # Frame para botones de utilidad
        utility_frame = tk.Frame(self.root, bg='#f0f0f0')
        utility_frame.pack(pady=5)
        
        # Botón Verificar Estado
        tk.Button(
            utility_frame,
            text="Verificar Estado",
            command=self.check_status,
            bg='#FF9800',
            fg='white',
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón Ver Log
        tk.Button(
            utility_frame,
            text="Ver Log",
            command=self.view_log,
            bg='#9C27B0',
            fg='white',
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Área de log
        self.log_text = tk.Text(self.root, height=4, width=45, font=("Consolas", 8))
        self.log_text.pack(pady=10, padx=20)
        self.log_text.config(state=tk.DISABLED)

    def add_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def verify_environment(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.add_log(f"Verificando entorno en: {current_dir}")
        
        errors = []
        
        # 1. Verificar archivos requeridos
        required_files = [
            ("backend/server.py", "Servidor Python (backend)"),
            ("package.json", "Configuración de Node.js"),
            (".env.development", "Configuración de desarrollo"),
            (".env.production", "Configuración de producción")
        ]
        
        missing_files_log = []
        for rel_path, description in required_files:
            full_path = os.path.join(current_dir, rel_path)
            if not os.path.exists(full_path):
                missing_files_log.append(f"- {description} ({rel_path})")

        if missing_files_log:
            errors.append("Archivos faltantes:\n" + "\n".join(missing_files_log))

        # 2. Verificar si npm está instalado
        try:
            subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True, shell=True)
            self.add_log("✓ npm está instalado.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.add_log("✗ npm NO está instalado.")
            errors.append("npm no está instalado o no se encuentra en el PATH del sistema.")
            if messagebox.askyesno("npm no encontrado", 
                                 "npm no está instalado, pero es necesario para el entorno local.\n\n"
                                 "¿Deseas abrir la página de descarga de Node.js?"):
                webbrowser.open("https://nodejs.org")

        # 3. Si hay errores, mostrarlos y detener la ejecución
        if errors:
            error_message = "Se encontraron problemas de configuración:\n\n" + "\n\n".join(errors)
            self.add_log(f"ERROR: {error_message}")
            messagebox.showerror("Error de Configuración", error_message)
            raise RuntimeError(error_message)
            
        self.add_log("✓ Verificación del entorno completada sin problemas.")

    def switch_environment(self, env_type):
        try:
            source = f".env.{env_type}"
            target = ".env"
            
            if not os.path.exists(source):
                messagebox.showerror(
                    "Error",
                    f"No se encuentra el archivo {source}. Asegúrate de que existe en el directorio."
                )
                return
            
            if os.path.exists(target):
                backup = f"{target}.backup"
                shutil.copy2(target, backup)
            
            shutil.copy2(source, target)
            
            self.current_env.set(env_type.upper())
            self.add_log(f"Cambiado entorno a {env_type.upper()}")
            
            messagebox.showinfo(
                "Éxito",
                f"¡Entorno cambiado a {env_type.upper()}!"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar el entorno: {str(e)}")

    def run_local_servers(self):
        try:
            self.add_log("Iniciando servidores locales...")
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.add_log(f"Directorio de trabajo: {current_dir}")
            
            backend_path = os.path.join(current_dir, "backend", "server.py")
            
            if not os.path.exists(backend_path):
                raise FileNotFoundError(f"No se encuentra el archivo del servidor backend en: {backend_path}")
            
            self.add_log("Iniciando servidor backend...")
            # Usar sys.executable para garantizar que se usa el mismo intérprete de Python
            backend_cmd = [sys.executable, backend_path]
            backend_process = subprocess.Popen(
                backend_cmd,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=current_dir
            )
            self.processes.append(backend_process)
            
            time.sleep(2)
            
            self.add_log("Iniciando servidor frontend...")
            # Detectar el SO para usar el script de npm correcto (dev vs dev:win)
            if sys.platform == "win32":
                frontend_cmd = "npm run dev:win"
            else:
                frontend_cmd = "npm run dev"
            
            self.add_log(f"Ejecutando comando frontend: {frontend_cmd}")
            frontend_process = subprocess.Popen(
                frontend_cmd,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=current_dir,
                shell=True
            )
            self.processes.append(frontend_process)
            
            time.sleep(5)
            webbrowser.open("http://localhost:3000")
            
        except Exception as e:
            self.add_log(f"Error al iniciar servidores: {str(e)}")
            raise

    def switch_to_local(self):
        try:
            self.verify_environment()
            self.switch_environment("development")
            self.run_local_servers()
        except Exception as e:
            self.add_log(f"Error en la configuración: {str(e)}")
            # El mensaje de error ya se muestra en verify_environment, 
            # así que aquí solo registramos el fallo general.
            messagebox.showerror(
                "Error de Configuración",
                f"No se pudo iniciar el entorno local.\n\nConsulte el log para más detalles."
            )

    def switch_to_production(self):
        self.kill_processes()
        self.switch_environment("production")
        messagebox.showinfo(
            "Cambio a Producción",
            "Se ha cambiado al entorno de producción y se han detenido los servidores locales."
        )

    def kill_processes(self):
        for proc in self.processes:
            try:
                process = psutil.Process(proc.pid)
                for child in process.children(recursive=True):
                    child.terminate()
                process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        self.processes = []

    def check_status(self):
        status_message = "Estado del sistema:\n"
        
        ports = [3000, 8002]
        for port in ports:
            try:
                for conn in psutil.net_connections():
                    if conn.laddr.port == port:
                        status_message += f"✓ Puerto {port} activo\n"
                        break
                else:
                    status_message += f"✗ Puerto {port} inactivo\n"
            except:
                status_message += f"? Puerto {port} estado desconocido\n"
        
        messagebox.showinfo("Estado del Sistema", status_message)

    def view_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Log de Operaciones")
        log_window.geometry("500x300")
        
        log_content = tk.Text(log_window, wrap=tk.WORD, font=("Consolas", 10))
        log_content.pack(expand=True, fill='both', padx=10, pady=10)
        
        log_content.insert('1.0', self.log_text.get('1.0', tk.END))
        log_content.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnvironmentSwitcher(root)
    
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?\nEsto detendrá todos los servidores locales."):
            app.kill_processes()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()