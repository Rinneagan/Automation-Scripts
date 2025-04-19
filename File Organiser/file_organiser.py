import time
import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === Configuration ===
FOLDER_TO_WATCH = r"C:\Users\ebene\Downloads\Video"
SINGULAR_TIMEOUT = 30  # seconds
SINGULAR_FOLDER = os.path.join(FOLDER_TO_WATCH, "SingularS")

# === Logging Setup ===
LOG_FILE = os.path.join(FOLDER_TO_WATCH, "file_mover.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Caches ===
file_cache = {}  # prefix -> {timestamp, files}
moved_files = set()  # track already moved full paths
singular_history = {}  # prefix -> (full_path, file_name)


class FileMoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        time.sleep(1)  # Ensure file is fully copied
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        file_base, _ = os.path.splitext(file_name)
        prefix = file_base[:5]
        now = time.time()

        logging.info(f"Detected file: {file_name} (prefix: {prefix})")

        group_folder = os.path.join(FOLDER_TO_WATCH, prefix)

        # If folder already exists for prefix, move it in directly
        if os.path.exists(group_folder) and os.path.isdir(group_folder):
            try:
                shutil.move(file_path, os.path.join(group_folder, file_name))
                moved_files.add(file_path)
                logging.info(f"Moved '{file_name}' directly into existing folder '{prefix}'")
            except Exception as e:
                logging.error(f"Error moving '{file_name}' into existing folder '{prefix}': {e}")
            return

        # If file with same prefix was in SingularS, regroup
        if prefix in singular_history:
            old_path, old_name = singular_history.pop(prefix)
            os.makedirs(group_folder, exist_ok=True)
            try:
                shutil.move(old_path, os.path.join(group_folder, old_name))
                shutil.move(file_path, os.path.join(group_folder, file_name))
                moved_files.update([old_path, file_path])
                logging.info(f"Regrouped '{old_name}' and '{file_name}' into folder '{prefix}'")
            except Exception as e:
                logging.error(f"Error regrouping files for prefix '{prefix}': {e}")
            return

        # Otherwise, add to cache
        if prefix not in file_cache:
            file_cache[prefix] = {"timestamp": now, "files": [(file_path, file_name)]}
        else:
            file_cache[prefix]["files"].append((file_path, file_name))

    def process_cache(self):
        now = time.time()
        os.makedirs(SINGULAR_FOLDER, exist_ok=True)
        to_remove = []

        for prefix, entry in list(file_cache.items()):
            files = [(p, n) for p, n in entry["files"] if p not in moved_files]
            file_cache[prefix]["files"] = files  # update cache with only unmoved

            if not files:
                to_remove.append(prefix)
                continue

            if len(files) >= 2:
                group_folder = os.path.join(FOLDER_TO_WATCH, prefix)
                os.makedirs(group_folder, exist_ok=True)

                for f_path, f_name in files:
                    try:
                        shutil.move(f_path, os.path.join(group_folder, f_name))
                        moved_files.add(f_path)
                        logging.info(f"Grouped '{f_name}' into folder '{prefix}'")
                    except Exception as e:
                        logging.error(f"Error grouping '{f_name}': {e}")

                to_remove.append(prefix)

            elif len(files) == 1:
                age = now - entry["timestamp"]
                if age >= SINGULAR_TIMEOUT:
                    f_path, f_name = files[0]
                    dest = os.path.join(SINGULAR_FOLDER, f_name)
                    try:
                        shutil.move(f_path, dest)
                        moved_files.add(f_path)
                        singular_history[prefix] = (dest, f_name)
                        logging.info(f"Moved singular '{f_name}' to 'SingularS'")
                    except Exception as e:
                        logging.error(f"Error moving singular '{f_name}': {e}")
                    to_remove.append(prefix)

        for prefix in to_remove:
            file_cache.pop(prefix, None)

    def fix_premature_folders(self):
        # Detect folders with only one file and revert them
        for item in os.listdir(FOLDER_TO_WATCH):
            path = os.path.join(FOLDER_TO_WATCH, item)
            if os.path.isdir(path) and item not in ["SingularS"]:
                files_inside = os.listdir(path)
                if len(files_inside) == 1:
                    file_inside = files_inside[0]
                    full_path = os.path.join(path, file_inside)
                    new_location = os.path.join(FOLDER_TO_WATCH, file_inside)

                    try:
                        shutil.move(full_path, new_location)
                        shutil.rmtree(path)
                        logging.info(f"Moved mistakenly grouped '{file_inside}' back to main folder")

                        time.sleep(1)  # Ensure file is visible to OS

                        # Immediately move to SingularS
                        if os.path.exists(new_location):
                            os.makedirs(SINGULAR_FOLDER, exist_ok=True)
                            dest = os.path.join(SINGULAR_FOLDER, file_inside)
                            shutil.move(new_location, dest)

                            prefix = item
                            moved_files.add(dest)
                            singular_history[prefix] = (dest, file_inside)
                            logging.info(f"Moved mistakenly grouped '{file_inside}' directly to 'SingularS'")
                        else:
                            logging.warning(f"File '{file_inside}' missing in main folder after move")
                    except Exception as e:
                        logging.error(f"Error reverting folder '{item}': {e}")


# === Main Script ===
if __name__ == "__main__":
    handler = FileMoverHandler()
    observer = Observer()
    observer.schedule(handler, FOLDER_TO_WATCH, recursive=False)
    observer.start()
    logging.info("Started watching folder...")

    try:
        while True:
            time.sleep(5)
            handler.fix_premature_folders()
            handler.process_cache()
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped monitoring.")
    observer.join()
