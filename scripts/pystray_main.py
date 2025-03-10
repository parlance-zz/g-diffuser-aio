import subprocess
import ctypes
import pystray
from PIL import Image
import os

CONSOLE_VISIBLE = True

def show_hide_console_window(icon, item):
    global CONSOLE_VISIBLE
    CONSOLE_VISIBLE = not item.checked
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), CONSOLE_VISIBLE)
    return

def launch_g_diffuser_cli(icon):
    print("Launching G-Diffuser CLI...")
    subprocess.Popen(("python", "g-diffuser/g_diffuser_cli.py"), creationflags=subprocess.CREATE_NEW_CONSOLE)
    return

def launch_g_diffuser_bot(icon):
    print("Launching G-Diffuser Bot...")
    subprocess.Popen(("python", "g-diffuser/g_diffuser_bot.py"),creationflags=subprocess.CREATE_NEW_CONSOLE)
    return

def launch_g_diffuser_gui(icon):
    print("Launching G-Diffuser GUI...")
    subprocess.Popen(("python", "g-diffuser/g_diffuser_gui.py"), creationflags=subprocess.CREATE_NEW_CONSOLE)
    return

def close(icon):
    icon.stop()
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0) # hide some error barf
    os._exit(0)

def start_pystray():
    icon_img = Image.open("g-diffuser/app_icon.ico")
    icon_menu=pystray.Menu(
        pystray.MenuItem('Show Server Console', show_hide_console_window, checked=lambda item: CONSOLE_VISIBLE),
        pystray.MenuItem('Launch G-Diffuser CLI', launch_g_diffuser_cli),
        pystray.MenuItem('Launch G-Diffuser Bot', launch_g_diffuser_bot),
        pystray.MenuItem('Launch G-Diffuser GUI', launch_g_diffuser_gui),
        pystray.MenuItem('Exit', close),
        )

    icon = pystray.Icon('G-Diffuser', icon=icon_img, menu=icon_menu)
    icon.run()
    return