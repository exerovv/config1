import argparse

def prompt(username, current_path):
    home_path = "/root"
    if current_path == home_path:
        path_display = "~"
    else:
        path_display = current_path
    return f"{username}@emulator:{path_display}$ "

def exit_shell():
    print("Exiting shell emulator...")
    exit(0)

def run_shell(username):
    current_path = "/root"
    while True:
        try:
            command = input(prompt(username, current_path)).strip().split()
            if not command:
                continue
            cmd = command[0]
            if cmd == 'exit':
                exit_shell()
            else:
                print(f"{cmd}: command not found")
        except KeyboardInterrupt:
            exit_shell()

def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument('--user', required=True, help='Имя пользователя для приглашения')
    parser.add_argument('--tar', required=True, help='Путь к tar-файлу с виртуальной файловой системой')
    return parser.parse_args()

def main():
    args = parse_args()
    run_shell(args.user)

if __name__ == "__main__":
    main()