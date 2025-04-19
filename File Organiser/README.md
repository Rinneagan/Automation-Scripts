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
2. Configure Your Folder Path
Inside both scripts, update this line to your desired folder:
FOLDER_TO_WATCH = r"C:\Users\YourName\Downloads\Video"
💡 Make sure the same path is used in both file_organizer.py and file_restore.py.

▶️ Usage
📂 Run the Organizer
Starts watching your folder for new files and groups them automatically.

python file_organizer.py
Keep it running in the background.

Stop anytime with Ctrl+C.

🔁 Run the Restore
Moves all files back into the main folder, cleaning up any created folders.


python file_restore.py
📋 Folder Behavior Examples
Before Organizer Runs:

📁 Video/
├── ABCDE_01.mp4
├── ABCDE_02.mp4
├── WXYZA_01.mp4
After Organizer Runs:

📁 Video/
├── 📁 ABCDE/
│   ├── ABCDE_01.mp4
│   └── ABCDE_02.mp4
├── 📁 SingularS/
│   └── WXYZA_01.mp4
After Running Restore:

📁 Video/
├── ABCDE_01.mp4
├── ABCDE_02.mp4
├── WXYZA_01.mp4
📄 Logs
All activity is logged to these files in your watch folder:

📄 file_mover.log – Organizer activity

📄 file_restore.log – Restore activity

⚠️ Notes & Tips
Files are grouped strictly by their first 5 characters (e.g., ABCDE_filename.ext).

Avoid manually creating 5-letter-named folders in the watch directory unless intended.

Always run file_restore.py before deleting or archiving organized files, to bring everything back to its original state.

👨‍💻 Author
Crafted with 💻 and ☕ by [Your Name]
For automation lovers and folder minimalists.

📬 Feedback & Contributions
Have suggestions or improvements? Open an issue or submit a pull request!

✅ License
This project is free to use and modify — no strings attached.