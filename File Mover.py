import time
import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folder to monitor
FOLDER_TO_WATCH = r"C:\Users\ebene\Downloads\Video"  # Change this to your path

# Setup logging
LOG_FILE = os.path.join(FOLDER_TO_WATCH, "file_mover.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FileMoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)  # Let the file finish copying

            file_path = event.src_path
            file_name = os.path.basename(file_path)

            # Use first five characters of the filename (excluding extension) as folder name
            file_base, _ = os.path.splitext(file_name)
            folder_name = file_base[:5]

            target_folder = os.path.join(FOLDER_TO_WATCH, folder_name)
            os.makedirs(target_folder, exist_ok=True)

            dest_path = os.path.join(target_folder, file_name)

            try:
                shutil.move(file_path, dest_path)
                logging.info(f"Moved '{file_name}' to '{target_folder}'")
            except Exception as e:
                logging.error(f"Error moving '{file_name}': {e}")

if __name__ == "__main__":
    event_handler = FileMoverHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=False)

    logging.info(f"Started monitoring folder: {FOLDER_TO_WATCH}")
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped monitoring.")
    observer.join()
