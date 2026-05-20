# 📂 Auto File Organizer & 🔁 One-Click Restore

A pair of powerful Python scripts to **automatically organize** your files based on filename prefixes — and **instantly undo** the grouping with a single command.

---

## 🚀 Overview

These scripts are designed for users who download or accumulate lots of files and need a clean, automatic way to:

✅ **Organize files** with matching prefixes into grouped folders
🕒 **Handle unmatched files** after a timeout period
♻️ **Recover from premature folder creation mistakes**
🔁 **Restore all files** back to their original, flat structure at any time

---

## 🧠 How It Works

### 🟢 `file_organizer.py`

> Continuously watches a target folder and organizes files as they arrive.

| Feature | Description |
|--------|-------------|
| 📛 Prefix-Based Grouping | Groups files with the same **first 5 characters** into a subfolder named after that prefix. |
| ⏳ Singular Timeout | Files without a match after **30 seconds** go to the `SingularS/` folder. |
| 🔄 Dynamic Regrouping | If a matching file shows up later, previously singular files are **automatically regrouped**. |
| 🚫 Premature Folder Detection | If a folder was mistakenly created for a single file, it gets **reverted and redirected**. |
| 🧾 Logging | All activity is recorded in a clean, timestamped log file for easy monitoring. |

---

### 🔁 `file_restore.py`

> Instantly reverts all folder changes made by the organizer.

| Feature | Description |
|--------|-------------|
| 📦 Folder Flattening | Moves all files back from prefix-named folders to the main directory. |
| 🧹 Cleanup | Deletes empty folders after restoring their contents. |
| 🗃️ Singular Recovery | Also restores files from the `SingularS/` folder. |
| 🧾 Logging | Keeps a detailed restore log so you can see what was moved. |

---

## 🛠️ Setup & Configuration

### 1. Install Dependencies

```bash
pip install watchdog
```

### 2. Configure Your Folder Path

Inside both scripts in the `File Organiser/` directory (`file_organiser.py` and `file_restore.py`), update this line to your desired folder to watch and restore:
```python
FOLDER_TO_WATCH = r"C:\Users\YourName\Downloads\Video" # file_organiser.py
FOLDER_TO_RESTORE = r"C:\Users\YourName\Downloads\Video" # file_restore.py
```
💡 Make sure the same path is used in both scripts.

---

## ▶️ Usage

The scripts are located inside the `File Organiser/` directory.

### 📂 Run the Organizer
Starts watching your folder for new files and groups them automatically.

```bash
python "File Organiser/file_organiser.py"
```
Keep it running in the background. Stop anytime with `Ctrl+C`.

### 🔁 Run the Restore
Moves all files back into the main folder, cleaning up any created folders.

```bash
python "File Organiser/file_restore.py"
```

---

## 📋 Folder Behavior Examples
Before Organizer Runs:

```text
📁 Video/
├── ABCDE_01.mp4
├── ABCDE_02.mp4
├── WXYZA_01.mp4
```

After Organizer Runs:

```text
📁 Video/
├── 📁 ABCDE/
│   ├── ABCDE_01.mp4
│   └── ABCDE_02.mp4
├── 📁 SingularS/
│   └── WXYZA_01.mp4
```

After Running Restore:

```text
📁 Video/
├── ABCDE_01.mp4
├── ABCDE_02.mp4
├── WXYZA_01.mp4
```

---

## 📄 Logs
All activity is logged to these files in your watch folder:

* 📄 `file_mover.log` – Organizer activity
* 📄 `file_restore.log` – Restore activity

---

## ⚠️ Notes & Tips
* Files are grouped strictly by their first 5 characters (e.g., `ABCDE_filename.ext`).
* Avoid manually creating 5-letter-named folders in the watch directory unless intended.
* Always run `file_restore.py` before deleting or archiving organized files, to bring everything back to its original state.
