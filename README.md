# EN
----------------------------------------------------------------
# Password Manager

This is a password manager application that supports auto-updating from GitHub and multiple languages.

## Features
- Generate multiple passwords with various options
- Encrypt and decrypt passwords
- Save and load encrypted passwords
- Multilingual support (English and Russian)
- Auto-update from GitHub

## Requirements
- Python 3.7+
- PyQt5
- GitPython
- cryptography
- pyperclip

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/Zorahm/password_manager.git
    cd password_manager
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Compile translation files:
    ```sh
    msgfmt locale/en/LC_MESSAGES/messages.po -o locale/en/LC_MESSAGES/messages.mo
    msgfmt locale/ru/LC_MESSAGES/messages.po -o locale/ru/LC_MESSAGES/messages.mo
    ```

4. Run the application:
    ```sh
    python main.py
    ```

## Usage
- Generate passwords by specifying the number, length, and other options.
- Save generated passwords to a file or clipboard.
- Load and decrypt passwords using the generated key.
- Edit decrypted passwords and add associated services.
- Save edited passwords with services to a file.

## Auto-update
The application automatically checks for updates from the GitHub repository and pulls the latest changes.

## Multilingual Support
The application supports multiple languages and automatically detects the system language.

----------------------------------------------------------------

# RU
----------------------------------------------------------------
# Менеджер Паролей

Это приложение для управления паролями, поддерживающее автоматическое обновление с GitHub и несколько языков.

## Особенности
- Генерация множества паролей с различными опциями
- Шифрование и расшифровка паролей
- Сохранение и загрузка зашифрованных паролей
- Поддержка нескольких языков (английский и русский)
- Автоматическое обновление с GitHub

## Требования
- Python 3.7+
- PyQt5
- GitPython
- cryptography
- pyperclip

## Настройка
1. Клонируйте репозиторий:
    git clone https://github.com/Zorahm/password_manager.git

2. Установите необходимые пакеты:
    pip install -r requirements.txt

3. Скомпилируйте файлы переводов:
    msgfmt locale/en/LC_MESSAGES/messages.po -o locale/en/LC_MESSAGES/messages.mo
    msgfmt locale/ru/LC_MESSAGES/messages.po -o locale/ru/LC_MESSAGES/messages.mo

4. Запустите приложение:
    python main.py

## Использование
- Генерируйте пароли, указывая их количество, длину и другие параметры.
- Сохраняйте сгенерированные пароли в файл или буфер обмена.
- Загружайте и расшифровывайте пароли с использованием сгенерированного ключа.
- Редактируйте расшифрованные пароли и добавляйте связанные сервисы.
- Сохраняйте отредактированные пароли с сервисами в файл.

## Автообновление
Приложение автоматически проверяет наличие обновлений из репозитория GitHub и загружает последние изменения.

## Поддержка нескольких языков
Приложение поддерживает несколько языков и автоматически определяет язык системы.

----------------------------------------------------------------
