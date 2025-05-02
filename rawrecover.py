import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def scan_physical_drive(drive_path, output_dir, log_widget):
    signatures = {
        'jpg': (b'\xff\xd8\xff', b'\xff\xd9'),
        'png': (b'\x89PNG\r\n\x1a\n', b'IEND\xaeB`\x82'),
        'pdf': (b'%PDF-', b'%%EOF'),
        'zip': (b'PK\x03\x04', b'PK\x05\x06')
    }

    recovered = 0
    try:
        with open(drive_path, 'rb') as f:
            data = f.read(1024 * 1024 * 100)  # Read 100MB at once
    except PermissionError:
        messagebox.showerror("Error", "Permission denied. Run as Administrator.")
        return

    for ext, (header, footer) in signatures.items():
        start = 0
        while True:
            header_index = data.find(header, start)
            if header_index == -1:
                break
            footer_index = data.find(footer, header_index + len(header))
            if footer_index == -1:
                break
            end_index = footer_index + len(footer)
            chunk = data[header_index:end_index]

            output_file = os.path.join(output_dir, f"recovered_{recovered:04}.{ext}")
            with open(output_file, 'wb') as out:
                out.write(chunk)
            log_widget.insert(tk.END, f"[+] Recovered: {output_file}\n")
            log_widget.see(tk.END)
            recovered += 1
            start = end_index

    log_widget.insert(tk.END, f"\nTotal files recovered: {recovered}\n")
    log_widget.see(tk.END)
    messagebox.showinfo("Done", f"Recovered {recovered} files.")

def start_raw_recovery():
    drive_path = entry.get()
    if not drive_path.startswith('\\\\.\\'):
        messagebox.showerror("Error", "Invalid physical drive path. Example: \\\\.\\PhysicalDrive1")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.getcwd(), f"RawRecovered_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    scan_physical_drive(drive_path, output_dir, log)

def main_gui():
    global entry, log

    root = tk.Tk()
    root.title("DeepRecover - Raw Disk Scanner")
    root.geometry("600x400")

    tk.Label(root, text="Enter physical drive (e.g., \\\\.\\PhysicalDrive1):").pack(pady=5)
    entry = tk.Entry(root, width=60)
    entry.pack()

    btn = tk.Button(root, text="Scan & Recover", command=start_raw_recovery, bg="red", fg="white")
    btn.pack(pady=10)

    log = tk.Text(root, height=15, width=70)
    log.pack()

    root.mainloop()

if __name__ == "__main__":
    if not is_admin():
        print("You need to run this script as Administrator.")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
    else:
        main_gui()
