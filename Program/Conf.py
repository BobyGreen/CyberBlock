import os
import pyotp
import qrcode
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.messagebox as messagebox
from cryptography.fernet import Fernet
import sys
import time
import threading


class ShowBanner:
    LIGHT_BLUE = '\033[96m'
    END_COLOR = '\033[0m'
    
    def __init__(self, banner):
        self.original_stdout = sys.stdout
        self.banner = banner
        self.exit_flag = False

    def show(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        for line in self.banner.split('\n'):
            self.original_stdout.write(self.LIGHT_BLUE + line + self.END_COLOR)
            self.original_stdout.write('\n')
        self.original_stdout.flush()

    def run(self):
        while not self.exit_flag:
            self.show()
            time.sleep(0.1)

banner_text = """
   ______      __              ____  __           __  
  / ____/_  __/ /_  ___  _____/ __ )/ /___  _____/ /__
 / /   / / / / __ \/ _ \/ ___/ __  / / __ \/ ___/ //_/
/ /___/ /_/ / /_/ /  __/ /  / /_/ / / /_/ / /__/ ,<   
\____/\__, /_.___/\___/_/  /_____/_/\____/\___/_/|_|  
     /____/ 
 _           _           __               The  :  Kill.Red
|_) \/  o   |_) _ |_ \/  /__ __ _  _ __   For  :  Your security :)   
|_) /   o   |_)(_)|_)/___\_| | (/_(/_| |  Help :  ChatGPT
"""

class StdoutVerde:
    VERDE = '\033[92m'
    RESET = '\033[0m'

    def write(self, message):
        sys.__stdout__.write(self.VERDE + message + self.RESET)

    def flush(self):
        sys.__stdout__.flush()

banner = ShowBanner(banner_text)
banner.show()

sys.stdout = StdoutVerde()


# Funciones de encriptación y desencriptación
def generar_clave():
    return Fernet.generate_key()

def guardar_clave(clave, nombre_archivo):
    with open(nombre_archivo, 'wb') as file:
        file.write(clave)

def cargar_clave(nombre_archivo):
    with open(nombre_archivo, 'rb') as file:
        return file.read()

def encriptar(mensaje, clave):
    f = Fernet(clave)
    return f.encrypt(mensaje.encode())

def desencriptar(mensaje_encriptado, clave):
    f = Fernet(clave)
    return f.decrypt(mensaje_encriptado).decode()

# Funciones existentes
def generar_secreto():
    return pyotp.random_base32()

def generar_url_qr(secreto, nombre_organizacion='CyberBlock'):
    # Obtener el nombre de usuario del sistema operativo
    nombre_usuario = os.getlogin()  # Otra opción es os.environ.get('USER')
    return pyotp.totp.TOTP(secreto).provisioning_uri(nombre_usuario, issuer_name=nombre_organizacion)

def mostrar_codigo_qr(url):
    def cerrar_ventana():
        root.destroy()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    root = tk.Tk()
    root.title("Configuración de 2AF")

    icono_path = os.path.join(script_directory, 'Icons.png')  # Asegúrate de cambiar 'mi_icono.png' por el nombre de tu archivo de ícono
    icono = Image.open(icono_path)
    icono_photo = ImageTk.PhotoImage(icono)
    root.iconphoto(False, icono_photo)

    root.configure(bg='black')

    mensaje = "Por favor, escanea el siguiente código QR con tu aplicación de autenticación."
    label_mensaje = tk.Label(root, text=mensaje, font=("Arial", 12, "bold"), fg="white", bg='black')
    label_mensaje.pack(pady=(10, 0))

    tkimage_qr = ImageTk.PhotoImage(img_qr)
    label_qr = tk.Label(root, image=tkimage_qr, bg='black')
    label_qr.pack(pady=(10, 10))

    # Botón estilizado con esquinas redondeadas y aspecto 3D
    boton_cerrar = tk.Button(
        root, 
        text="Ya escaneé el código QR", 
        command=cerrar_ventana, 
        font=("Arial", 10, "bold"), 
        fg="#FFFFFF", 
        bg="#4CAF50",  
        bd=0,  
        highlightthickness=0,
        relief="flat",
        padx=10,
        pady=5,
        activebackground="#0056b3",  
        activeforeground="#FFFFFF"
    )
    boton_cerrar.pack(pady=(10, 10))

    # Redondear esquinas del botón
    boton_cerrar.config(highlightbackground=root.cget('bg'), highlightthickness=2)
    boton_cerrar.configure(borderwidth=4, relief="groove")

    root.mainloop()

def validar_codigo(secreto, codigo_usuario):
    totp = pyotp.TOTP(secreto)
    return totp.verify(codigo_usuario)

def solicitar_codigo_y_validar(secreto):
    while True:
        codigo_usuario = input("""
Introduce el código generado por tu autenticador: """)
        if validar_codigo(secreto, codigo_usuario):
            print("Código validado con éxito.")
            return True
        else:
            print("Código de autenticación incorrecto. Inténtalo de nuevo.")

def cambiar_contraseña():
    while True:
        password = input("Crea una nueva contraseña (entre 4 y 6 caracteres): ")
        password_repeat = input("Repite la nueva contraseña: ")

        if len(password) >= 4 and len(password) <= 6 and password == password_repeat:
            return password
        else:
            print("Error: La contraseña no cumple con los requisitos o no coincide.")


script_directory = os.path.dirname(os.path.abspath(__file__))
clave_archivo = os.path.join(script_directory, "clave.key")
if not os.path.exists(clave_archivo):
    clave = generar_clave()
    guardar_clave(clave, clave_archivo)
else:
    clave = cargar_clave(clave_archivo)

secret_file = os.path.join(script_directory, "secret.txt")
password_file = os.path.join(script_directory, "password.txt")

if not os.path.exists(secret_file):
    secreto = generar_secreto()
    secreto_encriptado = encriptar(secreto, clave)
    with open(secret_file, 'wb') as file:
        file.write(secreto_encriptado)
    url_qr = generar_url_qr(secreto)
    mostrar_codigo_qr(url_qr)
else:
    with open(secret_file, 'rb') as file:
        secreto_encriptado = file.read()
    secreto = desencriptar(secreto_encriptado, clave)



# Validación del código y cambio de contraseña
if solicitar_codigo_y_validar(secreto):
    nueva_contraseña = cambiar_contraseña()
    contraseña_encriptada = encriptar(nueva_contraseña, clave)
    with open(password_file, 'wb') as file:
        file.write(contraseña_encriptada)
    print("""
|La contraseña ha sido creada exitosamente.
|Ponga en funcion el programa ejecutando CyberBlock.py 
 \Si ya lo tiene ejecutado ponalo en marcha con Ctrl+h            """)
    

sys.stdout = sys.__stdout__