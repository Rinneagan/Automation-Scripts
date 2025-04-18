
# 📁 File Organizer & Undo Script

## Overview

This project includes **two Python scripts** designed to automate file management in a specific folder:

1. **File Organizer Script** – Monitors a folder and automatically moves new files into subfolders based on their filenames.
2. **Undo Script** – Reverses the organization by moving files back to the original folder and removing empty folders.

---

## 1. 📂 `file_organizer.py`

### 🔧 Purpose

This script **monitors a specific folder** for new files and **automatically organizes** them into subfolders. Each subfolder is named after the **first 5 characters** of the file name (excluding the extension).

---

### 🔍 How It Works

- Uses `watchdog` to monitor the folder for new files.
- When a new file is created:
  - It waits briefly to ensure the file is fully copied.
  - Extracts the base filename (without extension).
  - Creates or reuses a subfolder named after the **first 5 characters** of the filename.
  - Moves the file into the appropriate subfolder.
- Logs every operation to a file (`file_mover.log`) within the monitored folder.

---

### 🗂 Example

If a file named `video12345.mp4` is added:
- The subfolder `video` will be created (if not already there).
- The file will be moved to:  
  `C:\Users\ebene\Downloads\Video\video\video12345.mp4`

---

### 🧰 Dependencies

- `watchdog`
- `os`, `shutil`, `time`, `logging`

Install watchdog if not already installed:
```bash
pip install watchdog
```

---

### ▶️ How to Run

```bash
python file_organizer.py
```

The script will keep running until interrupted (`Ctrl+C`).

---

## 2. ↩️ `undo_file_organizer.py`

### 🔧 Purpose

This script **reverses the folder organization** done by the `file_organizer.py`. It:
- Moves files from subfolders back to the main folder.
- Deletes the empty subfolders.

---

### 🔍 How It Works

- Iterates through subfolders in the monitored directory.
- For each folder, it checks if a file inside matches the folder name (e.g., `video/video12345.mp4`).
- Moves the file back to the main folder.
- If the subfolder is empty after the move, it is deleted.
- All actions are logged to `undo_file_mover.log`.

---

### 🗂 Example

If `video12345.mp4` is in:
```
C:\Users\ebene\Downloads\Video\video\
```

It will be moved back to:
```
C:\Users\ebene\Downloads\Video\
```

And the folder `video` will be removed if empty.

---

### ▶️ How to Run

```bash
python undo_file_organizer.py
```

One-time execution. Prints:  
`Undo process completed. Check log for details.`

---

## 📄 Logs

Each script writes logs to the monitored folder:

- `file_mover.log` – Activity of the organizer.
- `undo_file_mover.log` – Activity of the undo script.

These logs contain timestamps and details of each file move or error.

---

## ⚠️ Notes & Customization

- **Change the folder path** (`FOLDER_TO_WATCH`) to the one you want to monitor.
- Current logic uses the **first 5 characters** of the filename. You can adjust that by editing this line:
  ```python
  folder_name = file_base[:5]
  ```


---

**Author:** EBENEZER KWEKU ESSEL
