# Эмулятор командной оболочки ОС

Учебный проект по разработке эмулятора командной оболочки ОС.

## Этап 1 — REPL

На первом этапе реализован минимальный прототип командной оболочки с интерактивным CLI.

### Возможности

- интерактивный режим REPL;
- приглашение формируется на основе имени пользователя и имени компьютера;
- разбор команды и аргументов по пробелам;
- команда `ls` — заглушка;
- команда `cd` — заглушка;
- команда `exit` — завершение работы;
- обработка неизвестных команд;
- обработка неверного количества аргументов.

## Запуск

Для запуска выполните:

```bash
python3 main.py
Пример работы
username@hostname:~$ ls
ls

username@hostname:~$ ls -l
ls -l

username@hostname:~$ cd test
cd test

username@hostname:~$ hello
ERROR: Unknown command 'hello'

username@hostname:~$ exit test
ERROR: 'exit' command does not take any arguments!

username@hostname:~$ exit
Exiting program
Структура проекта
.
├── main.py
├── README.md
└── .gitignore
Требования
Python 3.x
Git
Автор
Учебный проект.