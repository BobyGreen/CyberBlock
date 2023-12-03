import sys
import tkinter as tk
import os
import datetime
import threading
from PIL import Image, ImageTk
import tkinter as tk
import pygame
import cv2
from pynput.mouse import Controller as MouseController
import time
from PIL import Image, Image
from cryptography.fernet import Fernet
import subprocess

def desencriptar(mensaje_encriptado, clave):
    f = Fernet(clave)
    return f.decrypt(mensaje_encriptado).decode()

def cargar_clave():
    clave_archivo = os.path.join(script_directory, "clave.key")
    with open(clave_archivo, 'rb') as file:
        return file.read()


class StdoutVerde:
    VERDE = '\033[92m'
    RESET = '\033[0m'

    def write(self, message):
        sys.__stdout__.write(self.VERDE + message + self.RESET)

    def flush(self):
        sys.__stdout__.flush()

class ShowBanner:
    BLUE = '\033[94m'
    LIGHT_BLUE = '\033[96m'
    DARK_BLUE = '\033[34m'
    END_COLOR = '\033[0m'
    
    def __init__(self, banner):
        self.original_stdout = sys.stdout
        self.banner = banner
        self.messages = []
        sys.stdout = self
        self.exit_flag = False

    def show(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        for line in [self.banner] + self.messages:
            if "Kill.Red" in line or "Your security :)" in line:
                self.original_stdout.write(self.LIGHT_BLUE + line + self.END_COLOR)
            elif "Cyberblock" in line:
                modified_line = self._apply_zebra_effect(line)
                self.original_stdout.write(modified_line + self.END_COLOR)
            else:
                self.original_stdout.write(self.BLUE + line + self.END_COLOR)
            self.original_stdout.write('\n')
        self.original_stdout.flush()

    def _apply_zebra_effect(self, line):
        zebra_effect = ""
        zebra_pattern = [self.DARK_BLUE, self.LIGHT_BLUE, self.LIGHT_BLUE, self.DARK_BLUE]  # Ajusta según el efecto deseado
        for idx, char in enumerate(line):
            color = zebra_pattern[idx % len(zebra_pattern)]
            zebra_effect += color + char
        return zebra_effect + self.END_COLOR

    def _apply_zebra_effect(self, line):
        zebra_effect = ""
        for idx, char in enumerate(line):
            if idx % 2 == 0:  # Ajusta este valor según el espaciado de las "rayas" que desees
                zebra_effect += self.BLUE + char
            else:
                zebra_effect += self.LIGHT_GREEN + char
        return zebra_effect
    
    def restore(self):
        sys.stdout = self.original_stdout
    
    def run(self):
        while not self.exit_flag:
            self.show()
            time.sleep(0.1)  # Ajusta este valor según lo rápido que quieras que se actualice el banner

banner = """
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

banner_handler = ShowBanner(banner)
banner_thread = threading.Thread(target=banner_handler.run)
banner_thread.start()

# Obtener la ubicación de la carpeta CyberBlock relativa al script
script_directory = os.path.dirname(os.path.abspath(__file__))
cyberblock_directory = os.path.abspath(os.path.join(script_directory, os.pardir))
photo_directory = os.path.join(cyberblock_directory, "Foto-INTRUSO")

# Crear la carpeta Foto-INTRUSO si no existe
if not os.path.exists(photo_directory):
    os.makedirs(photo_directory)

password_file = os.path.join(script_directory, "password.txt")
alarm_sound_file = os.path.join(script_directory, "alarm-clock.wav")

def execute_conf_if_password_missing():
    if not os.path.exists(password_file):
        print("El archivo de contraseña no existe.")

execute_conf_if_password_missing()

# Inicializar el controlador del mouse
mouse = MouseController()

def restrict_cursor():
    while True:
        # Verificar si la ventana está activa
        if root.focus_displayof() is not None:
            x, y = mouse.position
            # Coordenadas de la esquina superior izquierda de la ventana
            wx, wy = root.winfo_rootx(), root.winfo_rooty()
            # Dimensiones de la ventana
            width, height = root.winfo_width(), root.winfo_height()
            # Restringir el cursor dentro de la ventana
            if not (wx < x < wx + width and wy < y < wy + height):
                mouse.position = (wx + width / 2, wy + height / 2)
        time.sleep(0.01)

def cargar_clave():
    clave_archivo = os.path.join(script_directory, "clave.key")
    with open(clave_archivo, 'rb') as file:
        return file.read()

def verify_password(event=None):
    global count, counting, timer_thread

    # Cargar la clave de encriptación
    clave = cargar_clave()

    # Desencriptar la contraseña almacenada
    with open(password_file, 'rb') as file:
        pass_correct_encrypted = file.read()
    pass_correct = desencriptar(pass_correct_encrypted, clave)

    # Obtener la contraseña ingresada por el usuario
    pass_user = entry.get()

    # Verificación de la contraseña
    if pass_user == pass_correct:
        label_result.config(text="Contraseña válida", fg="green")
        root.after(1000, root.destroy)
    else:
        count += 1
        entry.delete(0, tk.END)
        if count == 3:
            disable_input()
            label_result.config(text="Contraseña incorrecta. Volver a intentar en 30 segundos", fg="red")
            capture_photo()
            play_alarm_sound(alarm_sound_file)  # Aquí se pasa el argumento necesario
            counting = False
            if timer_thread:
                timer_thread.join()
            timer_thread = threading.Thread(target=countdown, args=(30,))
            timer_thread.start()
        else:
            label_result.config(text="Contraseña incorrecta. Intento {}/3".format(count), fg="red")


def disable_input():
    entry.config(state=tk.DISABLED)
    button.config(state=tk.DISABLED)

def enable_input():
    entry.config(state=tk.NORMAL)
    button.config(state=tk.NORMAL)

def countdown(seconds):
    global counting, count

    counting = True
    while seconds >= 0 and counting:
        label_result.config(text="Volver a intentar en {} segundos".format(seconds), fg="blue")
        root.update()
        seconds -= 1
        if seconds < 0:
            break
        time.sleep(1)
    if counting:
        counting = False
        count = 0
        enable_input()
        label_result.config(text="", fg="black")
        entry.delete(0, tk.END)

def capture_photo():
    file_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
    file_path = os.path.join(photo_directory, file_name)

    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(file_path, frame)
        print("Foto guardada en {}".format(file_path))
    camera.release()

def set_system_volume(volume):
    try:
        subprocess.run(["amixer", "set", "Master", f"{volume}%"])
    except subprocess.SubprocessError as e:
        print(f"Error al ajustar el volumen: {e}")

def play_alarm_sound(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"No se pudo inicializar el audio: {e}")

def on_closing():
    global counting
    if counting:
        counting = False
        if timer_thread:
            timer_thread.join()
    root.destroy()

count = 0
counting = False
timer_thread = None

root = tk.Tk()
root.title("Desbloqueo de seguridad")
root.geometry("400x200")
root.configure(bg="light gray")
root.resizable(False, False)

# Establecer el ícono de la ventana
icon_path = os.path.join(script_directory, "Icons.png")
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)

# Establecer el ícono de la ventana
root.iconphoto(False, icon_photo)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

label = tk.Label(main_frame, text="Ingrese la contraseña:")
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

entry = tk.Entry(main_frame, show="*")
entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

button = tk.Button(main_frame, text="Verificar", command=verify_password)
button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

label_result = tk.Label(main_frame, text="", anchor="center")
label_result.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

entry.bind("<Return>", verify_password)

# Iniciar el hilo para restringir el cursor
threading.Thread(target=restrict_cursor, daemon=True).start()

root.mainloop()
