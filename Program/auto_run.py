import keyboard
import os
import tkinter as tk
from PIL import Image, ImageTk
from pynput.mouse import Controller as MouseController
import time
import threading
import subprocess
from cryptography.fernet import Fernet

# Función para cargar la clave de encriptación
def cargar_clave():
    clave_archivo = os.path.join(script_directory, "clave.key")
    with open(clave_archivo, 'rb') as file:
        return file.read()

# Función para desencriptar la contraseña
def desencriptar(mensaje_encriptado, clave):
    f = Fernet(clave)
    return f.decrypt(mensaje_encriptado).decode()

# Función que verifica la contraseña
def verify_password(password_window):
    entered_password = password_entry.get()
    
    # Cargar la clave de encriptación y desencriptar la contraseña almacenada
    clave = cargar_clave()
    with open(password_file, 'rb') as file:
        pass_correct_encrypted = file.read()
    correct_password = desencriptar(pass_correct_encrypted, clave)

    if entered_password == correct_password:
        password_window.quit()  # Cierra la ventana emergente
    else:
        error_label.config(text="Contraseña incorrecta")
        password_entry.delete(0, tk.END)  # Borra el campo de contraseña

# Obtener la ubicación del script actual
script_directory = os.path.dirname(os.path.abspath(__file__))
password_file = os.path.join(script_directory, 'password.txt')
conf_script = os.path.join(script_directory, 'Conf.py')  # Definir conf_script
verify_script = os.path.join(script_directory, 'VERIFY.py')  # Definir verify_script

# Verificar si el archivo de contraseña existe
if not os.path.exists(password_file):
    # Si el archivo de contraseña no existe, ejecuta Conf.py para crearlo
    subprocess.Popen(['python', conf_script])

# Función que se activará al presionar Ctrl+H
def on_hotkey():
    # Ejecuta VERIFY.py al presionar Ctrl+H
    subprocess.Popen(['python', verify_script])

# Registra el atajo de teclado Ctrl+H
keyboard.add_hotkey('ctrl+h', on_hotkey, suppress=True)

def show_password_window():
    password_window = tk.Toplevel()
    password_window.title("Verificar Contraseña")
    
    # Establecer el tamaño de la ventana y evitar que se redimensione
    password_window.geometry("200x100+400+300")
    password_window.resizable(False, False)
    password_window.overrideredirect(True)

    icon_filename = "Icons.png"
    icon_path = os.path.join(script_directory, icon_filename)
    if os.path.exists(icon_path):
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        password_window.iconphoto(False, icon_photo)

    global password_entry
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()

    # Vincular la tecla Enter con la función verify_password
    password_entry.bind("<Return>", lambda event: verify_password(password_window))

    verify_button = tk.Button(password_window, text="Verificar", command=lambda: verify_password(password_window))
    verify_button.pack()
    
    global error_label
    error_label = tk.Label(password_window, text="", foreground="red")
    error_label.pack()

    # Llama a la función para restringir el mouse a esta ventana
    continue_restricting_mouse(password_window)

# Función para restringir el movimiento del mouse a una ventana específica
def restrict_mouse_to_window(window):
    while True:
        current_x, current_y = mouse.position
        window_x, window_y, window_width, window_height = window.winfo_x(), window.winfo_y(), window.winfo_width(), window.winfo_height()

        if current_x < window_x:
            mouse.position = (window_x, current_y)
        elif current_x > window_x + window_width:
            mouse.position = (window_x + window_width, current_y)

        if current_y < window_y:
            mouse.position = (current_x, window_y)
        elif current_y > window_y + window_height:
            mouse.position = (current_x, window_y + window_height)

# Función para continuar restringiendo el movimiento del mouse
def continue_restricting_mouse(window):
    while True:
        restrict_mouse_to_window(window)
        time.sleep(0.01)

# Crear una ventana principal y ocultarla
root = tk.Tk()
root.withdraw()

# Registra el atajo de teclado Ctrl+Q
keyboard.add_hotkey('ctrl+q', show_password_window, suppress=True)

# Inicializa el controlador del mouse
mouse = MouseController()

root.mainloop()
