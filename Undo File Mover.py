import os
import shutil
import logging

# === Configuration ===
FOLDER_TO_RESTORE = r"C:\Users\ebene\Downloads\Video"
SINGULAR_FOLDER = os.path.join(FOLDER_TO_RESTORE, "SingularS")
LOG_FILE = os.path.join(FOLDER_TO_RESTORE, "file_restore.log")

# === Logging Setup ===
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def restore_files():
    # Step 1: Restore from regular prefix folders
    for item in os.listdir(FOLDER_TO_RESTORE):
        item_path = os.path.join(FOLDER_TO_RESTORE, item)
        if os.path.isdir(item_path) and item != "SingularS":
            for file in os.listdir(item_path):
                src = os.path.join(item_path, file)
                dst = os.path.join(FOLDER_TO_RESTORE, file)
                try:
                    shutil.move(src, dst)
                    logging.info(f"Restored '{file}' from '{item}' to main folder")
                except Exception as e:
                    logging.error(f"Error restoring '{file}' from '{item}': {e}")
            # Delete the empty folder
            try:
                os.rmdir(item_path)
                logging.info(f"Deleted empty folder '{item}'")
            except Exception as e:
                logging.warning(f"Could not delete folder '{item}': {e}")

    # Step 2: Restore from SingularS
    if os.path.exists(SINGULAR_FOLDER):
        for file in os.listdir(SINGULAR_FOLDER):
            src = os.path.join(SINGULAR_FOLDER, file)
            dst = os.path.join(FOLDER_TO_RESTORE, file)
            try:
                shutil.move(src, dst)
                logging.info(f"Restored singular file '{file}' to main folder")
            except Exception as e:
                logging.error(f"Error restoring singular file '{file}': {e}")
        # Delete SingularS folder
        try:
            os.rmdir(SINGULAR_FOLDER)
            logging.info("Deleted 'SingularS' folder")
        except Exception as e:
            logging.warning("Could not delete 'SingularS' folder: " + str(e))

if __name__ == "__main__":
    logging.info("Starting restore operation...")
    restore_files()
    logging.info("Restore operation completed.")
