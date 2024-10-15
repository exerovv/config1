import argparse
import tarfile
import os
from collections import deque

def prompt(username, current_path):
    home_path = "/root"
    if current_path == home_path:
        path_display = "~"
    else:
        path_display = current_path.lstrip('/')
    return f"{username}@emulator:{path_display}$ "

def exit_shell():
    exit(0)

def run_shell(username, tar):
    current_path = "/root"
    with tarfile.open(tar, "r") as tar_file:
        while True:
            try:
                command = input(prompt(username, current_path)).strip().split()
                if not command:
                    continue
                cmd = command[0]
                if cmd == 'exit':
                    exit_shell()
                elif cmd == 'ls':
                    list_directory(current_path, tar_file)
                elif cmd == 'cd':
                    if len(command) > 1:
                        current_path = change_directory(current_path, command[1], tar_file)
                    else:
                        print("cd: missing argument")
                elif cmd == 'tree':
                    tree(current_path, tar_file.getnames())
                elif cmd == 'tail':
                    if len(command) > 1:
                        tail(tar_file, command[1])
                    else:
                        print("tail: missing argument")
                else:
                    print(f"{cmd}: command not found")
            except KeyboardInterrupt:
                exit_shell()

def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument('--user', required=True, help='Имя пользователя для приглашения')
    parser.add_argument('--tar', required=True, help='Путь к tar-файлу с виртуальной файловой системой')
    return parser.parse_args()

def list_directory(current_path, tar_file):
    current_path = current_path.strip('/')
    current_path_len = len(current_path)
    for file in tar_file.getnames():
        if file.startswith(current_path):
            relative_path = file[current_path_len:].lstrip('/')
            if relative_path and '/' not in relative_path:
                print(relative_path)


import os


def change_directory(current_path, target_directory, tar_file):
    if target_directory == "/":
        return "/root"
    if target_directory.startswith("/"):
        new_dir = "/root"
    else:
        new_dir = current_path
    parts = target_directory.split('/')
    for part in parts:
        if part == '' or part == '.':
            continue
        elif part == "..":
            if new_dir != "/root":
                new_dir = "/".join(new_dir.strip('/').split('/')[:-1])
                if not new_dir:
                    new_dir = "/root"
        else:
            new_dir = os.path.join(new_dir, part).replace("\\", "/").strip('/')

    if any(f.startswith(new_dir + '/') for f in tar_file.getnames()):
        return "/" + new_dir if not new_dir.startswith("/") else new_dir
    else:
        print(f"cd: no such file or directory: {target_directory}")
        return current_path

def tree(current_path, tar_files, indent=0):
    prefix = " " * indent
    sub_dirs = {}
    for file in tar_files:
        relative_path = file[len(current_path):].lstrip('/').split('/')
        if len(relative_path) > 1:
            sub_dir = relative_path[0]
            if sub_dir not in sub_dirs:
                sub_dirs[sub_dir] = []
            sub_dirs[sub_dir].append(file)
    for file in tar_files:
        relative_path = file[len(current_path):].lstrip('/').split('/')
        if relative_path[0] not in sub_dirs and relative_path[0] != "":
            print(f"{prefix}{relative_path[0]}")
    for sub_dir, files in sub_dirs.items():
        print(f"{prefix}{sub_dir}/")
        tree(f"{current_path}/{sub_dir}".rstrip('/'), files, indent + 4)

def tail(tar_file, file_name, n=10):
    matching_files = [name for name in tar_file.getnames() if name.endswith(f"/{file_name}") or name == file_name]
    if not matching_files:
        print(f"Файл {file_name} не найден в архиве.")
        return
    if len(matching_files) > 1:
        print("Найдено несколько файлов с именем", file_name)
        for i, file in enumerate(matching_files, 1):
            print(f"{i}. {file}")
        choice = int(input("Выберите номер файла: ")) - 1
        selected_file = matching_files[choice]
    else:
        selected_file = matching_files[0]
    with tar_file.extractfile(selected_file) as file:
        lines = deque(file, maxlen=n)
    for line in lines:
        print(line.decode('utf-8'), end='')

def main():
    args = parse_args()
    if not os.path.exists(args.tar):
        print(f"tar file {args.tar} does not exist")
        exit(1)
    run_shell(args.user, args.tar)

if __name__ == "__main__":
    main()