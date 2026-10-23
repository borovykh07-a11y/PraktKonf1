"""
Эмулятор оболочки ОС. Вариант №3.
Этап 1: REPL.
Этап 2: конфигурация (CLI + XML, приоритет XML, скрипты с комментариями).
"""

import os
import getpass
import socket
import argparse
import json
import xml.etree.ElementTree as et


def parse_args():
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС. Вариант №3."
    )
    parser.add_argument("--vfs", type=str, default=None,
                        help="Путь к файлу VFS (JSON)")
    parser.add_argument("--prompt", type=str, default=None,
                        help="Пользовательское приглашение")
    parser.add_argument("--script", type=str, default=None,
                        help="Путь к стартовому скрипту")
    parser.add_argument("--config", type=str, default=None,
                        help="Путь к конфигу (XML)")
    return parser.parse_args()


def load_config(path):
    """Загружает конфиг из XML. Возвращает dict."""
    if path is None:
        return {}

    if not os.path.exists(path):
        print(f"Ошибка: конфиг '{path}' не найден.")
        return {}

    try:
        tree = et.parse(path)
        root = tree.getroot()
        result = {}
        for tag in ("vfs", "prompt", "script"):
            element = root.find(tag)
            if element is not None and element.text is not None:
                result[tag] = element.text.strip()
        return result
    except et.ParseError as e:
        print(f"Ошибка: не удалось разобрать XML: {e}")
        return {}


def merge_params(cli_args, config):
    """XML важнее CLI."""
    result = {
        "vfs": cli_args.vfs,
        "prompt": cli_args.prompt,
        "script": cli_args.script,
    }
    for key in ("vfs", "prompt", "script"):
        if key in config:
            result[key] = config[key]
    return result


def load_vfs(path):
    """Загружает VFS из JSON."""
    if path is None:
        return None
    if not os.path.exists(path):
        print(f"Ошибка: файл VFS '{path}' не найден.")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Ошибка: неверный JSON в VFS: {e}")
        return None


def get_prompt(custom_prompt=None):
    """Приглашение: custom или user@host:~$."""
    if custom_prompt:
        return custom_prompt
    user = getpass.getuser()
    host = socket.gethostname()
    return f"{user}@{host}:~$ "


def execute_command(command, args, vfs):
    """Выполняет команду. 'exit' — для выхода."""
    if command == "exit":
        print("Выход из эмулятора...")
        return "exit"

    elif command == "ls":
        print(f"Команда: {command}")
        print(f"Аргументы: {args}" if args else "Аргументы: нет")

    elif command == "cd":
        print(f"Команда: {command}")
        if len(args) == 0:
            print("Ошибка: cd требует один аргумент (путь)")
        elif len(args) > 1:
            print(f"Ошибка: cd принимает один аргумент, получено {len(args)}")
        else:
            print(f"Аргументы: {args}")

    elif command == "vfs":
        if vfs is None:
            print("VFS не загружена.")
        else:
            print(json.dumps(vfs, ensure_ascii=False, indent=2))

    else:
        print(f"Ошибка: команда '{command}' не найдена.")

    return None


def run_interactive(prompt, vfs):
    """Интерактивный REPL."""
    print("Введите 'exit' для выхода.\n")
    while True:
        try:
            user_input = input(prompt)
            if not user_input.strip():
                continue
            parts = user_input.split()
            command = parts[0]
            args = parts[1:]
            result = execute_command(command, args, vfs)
            if result == "exit":
                break
        except KeyboardInterrupt:
            print("\nЗавершение работы (Ctrl+C).")
            break


def run_script(script_path, prompt, vfs):
    """Запускает скрипт. Комментарии (#) и пустые строки пропускаются."""
    if not os.path.exists(script_path):
        print(f"Ошибка: скрипт '{script_path}' не найден.")
        return

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Ошибка чтения скрипта: {e}")
        return

    print(f"Выполнение стартового скрипта: {script_path}")
    print("-" * 40)

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        print(f"{prompt}{stripped}")

        parts = stripped.split()
        command = parts[0]
        args = parts[1:]

        result = execute_command(command, args, vfs)
        if result == "exit":
            break


def main():
    args = parse_args()
    config = load_config(args.config)
    params = merge_params(args, config)

    print("--- Запуск эмулятора оболочки (Вариант 3) ---")
    print("Параметры запуска:")
    
    vfs_val = params['vfs'] if params['vfs'] else '(не задан)'
    prompt_val = params['prompt'] if params['prompt'] else '(по умолчанию)'
    script_val = params['script'] if params['script'] else '(не задан)'

    print(f"  VFS:     {vfs_val}")
    print(f"  Prompt:  {prompt_val}")
    print(f"  Script:  {script_val}")
    print(f"  Config:  {args.config if args.config else '(не задан)'}")
    print()

    vfs = load_vfs(params["vfs"])
    prompt = get_prompt(params["prompt"])

    if params["script"]:
        run_script(params["script"], prompt, vfs)
    else:
        run_interactive(prompt, vfs)


if __name__ == "__main__":
    main()