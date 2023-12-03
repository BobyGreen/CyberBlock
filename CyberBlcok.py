import os
import subprocess

def find_and_execute_auto_run():
    script_directory = os.path.dirname(os.path.abspath(__file__))

    folder_name = "Program"  

    auto_run_file = os.path.join(script_directory, folder_name, "auto_run.py")
    if os.path.exists(auto_run_file):
        subprocess.run(["python", auto_run_file])
    else:
        print(f"El archivo 'auto_run.py' no se encontró en la carpeta '{folder_name}'.")

if __name__ == "__main__":
    find_and_execute_auto_run()
