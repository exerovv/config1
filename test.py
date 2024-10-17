import tarfile
import io
from contextlib import redirect_stdout
import unittest
from main import *

class TestShellCommands(unittest.TestCase):

    def setUp(self):
        self.tar = tarfile.open('root.tar', 'r')

    def tearDown(self):
        self.tar.close()

    def test_cd_root(self):
        current_path = "/root"
        new_path = change_directory(current_path, "/", self.tar)
        self.assertEqual(new_path, "/root")

    def test_cd_to_projectB(self):
        current_path = "/root/home/user/documents"
        new_path = change_directory(current_path, "projects/projectB", self.tar)
        self.assertEqual(new_path, "/root/home/user/documents/projects/projectB")

    def test_cd_to_parent_directory(self):
        current_path = "/root/home/user/documents/projects/projectA"
        new_path = change_directory(current_path, "..", self.tar)
        self.assertEqual(new_path, "/root/home/user/documents/projects")

    def test_ls_in_documents(self):
        current_path = "/root/home/user/documents"
        with io.StringIO() as buf, redirect_stdout(buf):
            list_directory(current_path, self.tar)
            output = buf.getvalue().strip().split('\n')
        expected_output = ['downloads', 'images', 'notes', 'projects', 'reports']
        self.assertEqual(sorted(output), sorted(expected_output))

    def test_ls_in_projectA(self):
        current_path = "/root/home/user/documents/projects/projectA"
        with io.StringIO() as buf, redirect_stdout(buf):
            list_directory(current_path, self.tar)
            output = buf.getvalue().strip().split('\n')
        expected_output = ['src']
        self.assertEqual(sorted(output), sorted(expected_output))

    def test_ls_in_empty_directory(self):
        current_path = "/root/home/user/empty_folder"
        with io.StringIO() as buf, redirect_stdout(buf):
            list_directory(current_path, self.tar)
            output = buf.getvalue().strip()
        self.assertEqual(output, "")

    def test_tree(self):
        current_path = "/root/home/user/documents"
        with io.StringIO() as buf, redirect_stdout(buf):
            tree(current_path, self.tar.getnames())
            output = buf.getvalue().strip()
        self.assertIn('projects/', output)
        self.assertIn('report.pdf', output)

    def test_tree_in_projectA(self):
        current_path = "/root/home/user/documents/projects/projectA"
        with io.StringIO() as buf, redirect_stdout(buf):
            tree(current_path, self.tar.getnames())
            output = buf.getvalue().strip()
        self.assertIn('src/', output)

    def test_tree_empty_directory(self):
        current_path = "/root/home/user/empty_folder"
        with io.StringIO() as buf, redirect_stdout(buf):
            tree(current_path, self.tar.getnames())
            output = buf.getvalue().strip()
        self.assertEqual(output, "")

    def test_tail_valid_file(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            tail(self.tar, 'todolist.txt', n=2)
            output = buf.getvalue().strip().split('\n')
        self.assertEqual(len(output), 2)

    def test_tail_nonexistent_file(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            tail(self.tar, 'nonexistent.txt', n=2)
            output = buf.getvalue().strip()
        self.assertIn('File nonexistent.txt not found in archive.', output)

    def test_tail_less_than_n_lines(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            tail(self.tar, 'short_file.txt', n=5)
            output = buf.getvalue().strip().split('\n')
        self.assertLessEqual(len(output), 5)

    def test_exit(self):
        with self.assertRaises(SystemExit):
            exit_shell()

if __name__ == '__main__':
    unittest.main()
