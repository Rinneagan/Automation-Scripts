import os
import shutil
import logging

# Folder to reverse the file organization
FOLDER_TO_WATCH = r"C:\Users\ebene\Downloads\Video"  # Change this to your path

# Setup logging
LOG_FILE = os.path.join(FOLDER_TO_WATCH, "undo_file_mover.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def undo_file_mover():
    # Loop through items in the main folder
    for entry in os.listdir(FOLDER_TO_WATCH):
        folder_path = os.path.join(FOLDER_TO_WATCH, entry)

        # Check if entry is a folder (potentially created by the file organizer)
        if os.path.isdir(folder_path):
            # Loop through files in the subfolder
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                dest_path = os.path.join(FOLDER_TO_WATCH, file)

                try:
                    shutil.move(file_path, dest_path)
                    logging.info(f"Moved '{file}' back to '{FOLDER_TO_WATCH}'")
                except Exception as e:
                    logging.error(f"Failed to move '{file}': {e}")

            # Try to delete the folder if it’s empty now
            try:
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)
                    logging.info(f"Deleted empty folder: {folder_path}")
            except Exception as e:
                logging.warning(f"Could not delete folder '{folder_path}': {e}")

if __name__ == "__main__":
    undo_file_mover()
    print("Undo process completed. Check log for details.")
