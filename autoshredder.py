import getpass
import os
import subprocess
import sys
from typing import Callable
import argparse

def traverse_file_tree(root: str, callback: Callable) -> None:
     for root, dirs, files in os.walk(root, topdown=True):
          for file in files:
               current_file_path = os.path.join(root, file)
               print(f"Trying to shred file: {current_file_path}")
               res = callback(current_file_path)
               if res:
                    print("Success!")
               else:
                    print(f"Error shredding {current_file_path}")

def quoted(s):
     return f'"{s}"'


class FileShredder:
     
    def __init__(self, sudo_password):
         self.sudo_password = sudo_password

    def __call__(self, file_path: str) -> bool:
         absoulute_path = os.path.abspath(file_path)
         return subprocess.Popen(f"echo {self.sudo_password} | sudo -S shred -vzun 3 {quoted(absoulute_path)}", stdout=sys.stdout, shell=True) == 0



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="File shredder for Linux", 
                                     description="Shredding all files in target directory recursively")
    
    parser.add_argument("directory")
    args = parser.parse_args()
    print(f"Root is : {args.directory}")
    
    sudo_password=getpass.getpass("Enter the Sudo password: ")

    traverse_file_tree(args.directory, FileShredder(sudo_password))
