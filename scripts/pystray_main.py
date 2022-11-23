import subprocess
import ctypes
import pystray
from PIL import Image

CONSOLE_VISIBLE = True

def show_hide_console_window(icon, item):
    global CONSOLE_VISIBLE
    CONSOLE_VISIBLE = not item.checked
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), CONSOLE_VISIBLE)
    return

def launch_g_diffuser_cli(icon):
    print("Launching G-Diffuser CLI...")
    subprocess.run(("python", "g_diffuser_cli.py"), cwd="./g-diffuser")
    return

def launch_g_diffuser_bot(icon):
    print("Launching G-Diffuser Bot...")
    subprocess.run(("python", "g_diffuser_bot.py"), cwd="./g-diffuser")
    return

def launch_g_diffuser_gui(icon):
    print("Launching G-Diffuser GUI...")
    subprocess.run(("python", "g_diffuser_gui.py"), cwd="./g-diffuser")
    return

def close(icon):
    icon.stop()
    return

def start_pystray():
    icon_img = Image.open("app_icon.ico")
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