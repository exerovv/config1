import argparse
import tarfile
import os

def prompt(username, current_path):
    home_path = "/root"
    if current_path == home_path:
        path_display = "~"
    else:
        path_display = current_path
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
                    list_directory(current_path, tar_file.getnames())
                elif cmd == 'cd':
                    if len(command) > 1:
                        current_path = change_directory(current_path, command[1], tar_file)
                    else:
                        print("cd: missing argument")
                else:
                    print(f"{cmd}: command not found")
            except KeyboardInterrupt:
                exit_shell()


def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument('--user', required=True, help='Имя пользователя для приглашения')
    parser.add_argument('--tar', required=True, help='Путь к tar-файлу с виртуальной файловой системой')
    return parser.parse_args()

def list_directory(current_path, tar_files):
    for file in tar_files:
        relative_path = file[len(current_path):].lstrip('/')
        if '/' not in relative_path and relative_path:
            print(relative_path)


def change_directory(current_path, target_directory, tar_file):
    if target_directory == "/":
        return "/root"

    elif target_directory == "..":
        if current_path != "/root":
            return os.path.dirname(current_path)
        return current_path
    else:
        new_path = os.path.join(current_path, target_directory).replace("\\", "/").strip('/')
        if any(f.startswith(new_path + '/') for f in tar_file.getnames()):
            return new_path
        else:
            print(f"cd: {target_directory}: No such file or directory")
            return current_path


def main():
    args = parse_args()

    if not os.path.exists(args.tar):
        print(f"tar file {args.tar} does not exist")
        exit(1)

    run_shell(args.user, args.tar)


if __name__ == "__main__":
    main()
