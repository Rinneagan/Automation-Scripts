import os
import shutil
import unittest
import tempfile
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestFileRestore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock logging.basicConfig before importing file_restore to prevent writing logs to real files
        cls.patcher_logging = patch('logging.basicConfig')
        cls.patcher_logging.start()
        global file_restore
        import file_restore

    @classmethod
    def tearDownClass(cls):
        cls.patcher_logging.stop()

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        # Override the variables in file_restore
        self.patcher_folder = patch('file_restore.FOLDER_TO_RESTORE', self.temp_dir)
        self.patcher_singular = patch('file_restore.SINGULAR_FOLDER', os.path.join(self.temp_dir, 'SingularS'))

        self.patcher_folder.start()
        self.patcher_singular.start()

    def tearDown(self):
        self.patcher_folder.stop()
        self.patcher_singular.stop()
        shutil.rmtree(self.temp_dir)

    def test_restore_from_regular_folders(self):
        # Create a regular folder with a file
        regular_folder = os.path.join(self.temp_dir, "PREFIX")
        os.makedirs(regular_folder)
        test_file_path = os.path.join(regular_folder, "PREFIX_file.txt")
        with open(test_file_path, 'w') as f:
            f.write("test content")

        file_restore.restore_files()

        # Check if the file was moved to the main folder
        restored_file_path = os.path.join(self.temp_dir, "PREFIX_file.txt")
        self.assertTrue(os.path.exists(restored_file_path))

        # Check if the empty regular folder was deleted
        self.assertFalse(os.path.exists(regular_folder))

    def test_restore_from_singular_folder(self):
        # Create the SingularS folder with a file
        singular_folder = os.path.join(self.temp_dir, "SingularS")
        os.makedirs(singular_folder)
        test_file_path = os.path.join(singular_folder, "SINGULAR_file.txt")
        with open(test_file_path, 'w') as f:
            f.write("test content")

        file_restore.restore_files()

        # Check if the file was moved to the main folder
        restored_file_path = os.path.join(self.temp_dir, "SINGULAR_file.txt")
        self.assertTrue(os.path.exists(restored_file_path))

        # Check if the empty SingularS folder was deleted
        self.assertFalse(os.path.exists(singular_folder))

    def test_restore_handles_move_error(self):
        # Create a folder with a file
        regular_folder = os.path.join(self.temp_dir, "PREFIX")
        os.makedirs(regular_folder)
        test_file_path = os.path.join(regular_folder, "PREFIX_file.txt")
        with open(test_file_path, 'w') as f:
            f.write("test content")

        # Mock shutil.move to raise an Exception
        with patch('shutil.move', side_effect=Exception("Mocked move error")):
            file_restore.restore_files()

        # File should still be in the regular folder
        self.assertTrue(os.path.exists(test_file_path))
        # Folder should not be deleted since it's not empty
        self.assertTrue(os.path.exists(regular_folder))

    def test_restore_from_singular_folder_handles_move_error(self):
        # Create the SingularS folder with a file
        singular_folder = os.path.join(self.temp_dir, "SingularS")
        os.makedirs(singular_folder)
        test_file_path = os.path.join(singular_folder, "SINGULAR_file.txt")
        with open(test_file_path, 'w') as f:
            f.write("test content")

        # Mock shutil.move to raise an Exception
        with patch('shutil.move', side_effect=Exception("Mocked move error in SingularS")):
            file_restore.restore_files()

        # File should still be in the SingularS folder
        self.assertTrue(os.path.exists(test_file_path))
        # Folder should not be deleted since it's not empty
        self.assertTrue(os.path.exists(singular_folder))

if __name__ == '__main__':
    unittest.main()
