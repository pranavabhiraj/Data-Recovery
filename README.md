

# DeepRecover - Raw Disk Scanner

**DeepRecover** is a forensic recovery tool that scans a physical drive at a low level (raw access) to identify and extract recoverable files based on known file signatures (headers and footers). This tool is primarily intended for use in digital forensics and data recovery investigations.

---

## 🚀 Features

* Scans a specified physical drive for recoverable file types.
* Extracts and saves files based on known headers and footers.
* Supports recovery of:

  * JPEG images (`.jpg`)
  * PNG images (`.png`)
  * PDF documents (`.pdf`)
  * ZIP archives (`.zip`)
* Simple and user-friendly GUI using Tkinter.
* Automatically creates a time-stamped recovery folder for outputs.

---

## ⚠️ Disclaimer

This tool is **Windows-only** and **must be run with Administrator privileges** to access physical drives. Use it responsibly and **only on drives you are authorized to access**.

---

## 🖥️ Requirements

* Python 3.x
* Windows OS
* Admin access

---

## 📦 Dependencies

* Standard Python libraries only: `os`, `sys`, `ctypes`, `tkinter`, `datetime`

No external Python packages are required.

---

## 🛠️ How to Use

### Step 1: Run as Administrator

Open Command Prompt as Administrator or double-click the script. If not already elevated, the script will re-launch itself with admin privileges.

### Step 2: Select Physical Drive

Enter the physical drive path (e.g., `\\.\PhysicalDrive1`) into the input field.

> ⚠️ You can view physical drives using `diskpart` or `wmic diskdrive list brief`.

### Step 3: Scan and Recover

Click the **Scan & Recover** button. Recovered files will be saved in a `RawRecovered_<timestamp>` folder in the current directory.

---

## 🧠 How It Works

The script scans the first 100MB of the selected physical drive and looks for byte patterns corresponding to known file headers and footers. If both are found, it extracts the chunk in between and saves it as a file with the corresponding extension.

---

## 📂 Output

Recovered files are saved in a directory named:

```
RawRecovered_YYYYMMDD_HHMMSS
```

Each file is named like:

```
recovered_0001.jpg
recovered_0002.pdf
...
```

---

## 👨‍💻 Developer Notes

You can add support for more file types by updating the `signatures` dictionary in the `scan_physical_drive` function:

```python
signatures = {
    'jpg': (b'\xff\xd8\xff', b'\xff\xd9'),
    ...
}
```

---

