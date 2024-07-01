import gettext
import locale
import os
import sys
import logging
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QListWidget, QCheckBox, QFileDialog, QMessageBox, QTabWidget)
import pyperclip  # Для копирования в буфер обмена
from password_generator import generate_multiple_passwords
from encryption_utils import generate_key, save_encrypted_passwords, read_encrypted_passwords
import git

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Автообновление через GitHub
def update_from_github(repo_path):
    if not os.path.exists(repo_path):
        logging.error(f"Путь к репозиторию {repo_path} не существует.")
        return False

    try:
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        logging.info("Репозиторий успешно обновлен.")
        return True
    except Exception as e:
        logging.error(f"Ошибка обновления репозитория: {e}")
        return False

# Настройка многоязычной поддержки
def setup_translation():
    current_locale = locale.getlocale()[0]
    if current_locale is None:
        current_locale = 'en_US'
    locale_path = os.path.join(os.path.dirname(__file__), 'locale')
    language = gettext.translation('messages', localedir=locale_path, languages=[current_locale], fallback=True)
    language.install()
    return language.gettext

_ = setup_translation()

class PasswordManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(_('Password Manager'))
        self.setGeometry(100, 100, 850, 650)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        self.generate_tab = QWidget()
        self.decrypt_tab = QWidget()
        self.edit_tab = QWidget()

        self.tabs.addTab(self.generate_tab, _("Generate Passwords"))
        self.tabs.addTab(self.decrypt_tab, _("Decrypt Passwords"))
        self.tabs.addTab(self.edit_tab, _("Edit Passwords"))

        self.create_generate_tab()
        self.create_decrypt_tab()
        self.create_edit_tab()

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_generate_tab(self):
        layout = QVBoxLayout()

        self.num_passwords_label = QLabel(_('Number of passwords:'))
        self.num_passwords_input = QLineEdit('1')
        self.length_label = QLabel(_('Password length:'))
        self.length_input = QLineEdit('12')
        self.include_uppercase = QCheckBox(_('Include uppercase letters'))
        self.include_uppercase.setChecked(True)
        self.include_numbers = QCheckBox(_('Include numbers'))
        self.include_numbers.setChecked(True)
        self.include_special = QCheckBox(_('Include special characters'))
        self.include_special.setChecked(True)
        self.exclude_chars_label = QLabel(_('Exclude characters:'))
        self.exclude_chars_input = QLineEdit('')
        self.generate_button = QPushButton(_('Generate passwords'))
        self.generate_button.clicked.connect(self.generate_passwords)
        self.password_list = QListWidget()
        self.save_button = QPushButton(_('Save passwords'))
        self.save_button.clicked.connect(self.save_passwords)

        layout.addWidget(self.num_passwords_label)
        layout.addWidget(self.num_passwords_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.include_uppercase)
        layout.addWidget(self.include_numbers)
        layout.addWidget(self.include_special)
        layout.addWidget(self.exclude_chars_label)
        layout.addWidget(self.exclude_chars_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.password_list)
        layout.addWidget(self.save_button)

        self.generate_tab.setLayout(layout)

    def create_decrypt_tab(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.encrypted_file_path_label = QLabel(_('File with encrypted passwords:'))
        self.encrypted_file_path_input = QLineEdit()
        self.browse_encrypted_file_button = QPushButton(_('Browse'))
        self.browse_encrypted_file_button.clicked.connect(self.browse_encrypted_file)
        input_layout.addWidget(self.encrypted_file_path_label)
        input_layout.addWidget(self.encrypted_file_path_input)
        input_layout.addWidget(self.browse_encrypted_file_button)

        key_layout = QHBoxLayout()
        self.key_file_path_label = QLabel(_('Key file:'))
        self.key_file_path_input = QLineEdit()
        self.browse_key_file_button = QPushButton(_('Browse'))
        self.browse_key_file_button.clicked.connect(self.browse_key_file)
        key_layout.addWidget(self.key_file_path_label)
        key_layout.addWidget(self.key_file_path_input)
        key_layout.addWidget(self.browse_key_file_button)

        self.decrypt_button = QPushButton(_('Decrypt passwords'))
        self.decrypt_button.clicked.connect(self.decrypt_passwords)
        self.decrypted_password_list = QListWidget()

        layout.addLayout(input_layout)
        layout.addLayout(key_layout)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.decrypted_password_list)

        self.decrypt_tab.setLayout(layout)

    def create_edit_tab(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.edit_encrypted_file_path_label = QLabel(_('File with encrypted passwords:'))
        self.edit_encrypted_file_path_input = QLineEdit()
        self.browse_edit_encrypted_file_button = QPushButton(_('Browse'))
        self.browse_edit_encrypted_file_button.clicked.connect(self.browse_edit_encrypted_file)
        input_layout.addWidget(self.edit_encrypted_file_path_label)
        input_layout.addWidget(self.edit_encrypted_file_path_input)
        input_layout.addWidget(self.browse_edit_encrypted_file_button)

        key_layout = QHBoxLayout()
        self.edit_key_file_path_label = QLabel(_('Key file:'))
        self.edit_key_file_path_input = QLineEdit()
        self.browse_edit_key_file_button = QPushButton(_('Browse'))
        self.browse_edit_key_file_button.clicked.connect(self.browse_edit_key_file)
        key_layout.addWidget(self.edit_key_file_path_label)
        key_layout.addWidget(self.edit_key_file_path_input)
        key_layout.addWidget(self.browse_edit_key_file_button)

        self.load_and_decrypt_button = QPushButton(_('Load and decrypt passwords'))
        self.load_and_decrypt_button.clicked.connect(self.load_and_decrypt_passwords)
        self.edit_password_list = QListWidget()
        self.service_label = QLabel(_('Service:'))
        self.service_input = QLineEdit()
        self.add_service_button = QPushButton(_('Add service'))
        self.add_service_button.clicked.connect(self.add_service)
        self.save_with_services_button = QPushButton(_('Save decrypted passwords with services'))
        self.save_with_services_button.clicked.connect(self.save_decrypted_passwords_with_services)

        layout.addLayout(input_layout)
        layout.addLayout(key_layout)
        layout.addWidget(self.load_and_decrypt_button)
        layout.addWidget(self.edit_password_list)
        layout.addWidget(self.service_label)
        layout.addWidget(self.service_input)
        layout.addWidget(self.add_service_button)
        layout.addWidget(self.save_with_services_button)

        self.edit_tab.setLayout(layout)

    def browse_encrypted_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, _("Select file with encrypted passwords"), "", "Text files (*.txt)")
        self.encrypted_file_path_input.setText(file_path)

    def browse_key_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, _("Select key file"), "", "Key files (*.key)")
        self.key_file_path_input.setText(file_path)

    def browse_edit_encrypted_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, _("Select file with encrypted passwords"), "", "Text files (*.txt)")
        self.edit_encrypted_file_path_input.setText(file_path)

    def browse_edit_key_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, _("Select key file"), "", "Key files (*.key)")
        self.edit_key_file_path_input.setText(file_path)

    def generate_passwords(self):
        try:
            count = int(self.num_passwords_input.text())
            length = int(self.length_input.text())
            include_uppercase = self.include_uppercase.isChecked()
            include_numbers = self.include_numbers.isChecked()
            include_special = self.include_special.isChecked()
            exclude_chars = self.exclude_chars_input.text()

            passwords = generate_multiple_passwords(count, length, include_uppercase, include_numbers, include_special, exclude_chars=exclude_chars)
            self.password_list.clear()
            for password in passwords:
                self.password_list.addItem(password)
            logging.info("Passwords generated successfully.")
        except Exception as e:
            logging.error(f"Error generating passwords: {e}")
            QMessageBox.critical(self, _('Error'), _("Failed to generate passwords: ") + str(e))

    def save_passwords(self):
        passwords = [self.password_list.item(i).text() for i in range(self.password_list.count())]
        if not passwords:
            QMessageBox.warning(self, _("Warning"), _("No passwords to save"))
            return

        try:
            # Save plain passwords
            plain_file_path, _ = QFileDialog.getSaveFileName(self, _("Save plain passwords"), "", "Text files (*.txt)")
            if plain_file_path:
                with open(plain_file_path, 'w') as file:
                    for password in passwords:
                        file.write(password + "\n")
                logging.info("Plain passwords saved successfully.")

            # Save encrypted passwords and generate key
            key = generate_key()
            encrypted_file_path, _ = QFileDialog.getSaveFileName(self, _("Save encrypted passwords"), "", "Text files (*.txt)")
            if encrypted_file_path:
                save_encrypted_passwords(passwords, encrypted_file_path, key)
                with open(f"{encrypted_file_path}.key", 'wb') as key_file:
                    key_file.write(key)
                logging.info("Encrypted passwords and key saved successfully.")
                QMessageBox.information(self, _("Success"), _("Passwords saved and encrypted"))

            # Copy passwords to clipboard
            passwords_str = "\n".join(passwords)
            pyperclip.copy(passwords_str)
            logging.info("Passwords copied to clipboard.")
            QMessageBox.information(self, _("Success"), _("Passwords copied to clipboard"))
        except Exception as e:
            logging.error(f"Error saving passwords: {e}")
            QMessageBox.critical(self, _("Error"), _("Failed to save passwords: ") + str(e))

    def decrypt_passwords(self):
        encrypted_file_path = self.encrypted_file_path_input.text()
        key_file_path = self.key_file_path_input.text()

        if not encrypted_file_path or not key_file_path:
            QMessageBox.warning(self, _("Warning"), _("Please select both encrypted password file and key file"))
            return

        try:
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()

            passwords = read_encrypted_passwords(encrypted_file_path, key)
            self.decrypted_password_list.clear()
            for password in passwords:
                self.decrypted_password_list.addItem(password)
            logging.info("Passwords decrypted successfully.")
            QMessageBox.information(self, _("Success"), _("Passwords decrypted"))
        except Exception as e:
            logging.error(f"Error decrypting passwords: {e}")
            QMessageBox.critical(self, _("Error"), _("Failed to decrypt passwords: ") + str(e))

    def load_and_decrypt_passwords(self):
        encrypted_file_path = self.edit_encrypted_file_path_input.text()
        key_file_path = self.edit_key_file_path_input.text()

        if not encrypted_file_path or not key_file_path:
            QMessageBox.warning(self, _("Warning"), _("Please select both encrypted password file and key file"))
            return

        try:
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()

            self.decrypted_passwords = read_encrypted_passwords(encrypted_file_path, key)
            self.edit_password_list.clear()
            for password in self.decrypted_passwords:
                self.edit_password_list.addItem(password)
            logging.info("Passwords decrypted successfully.")
            QMessageBox.information(self, _("Success"), _("Passwords decrypted"))
        except Exception as e:
            logging.error(f"Error decrypting passwords: {e}")
            QMessageBox.critical(self, _("Error"), _("Failed to decrypt passwords: ") + str(e))

    def add_service(self):
        selected_index = self.edit_password_list.currentRow()
        if selected_index == -1:
            QMessageBox.warning(self, _("Warning"), _("Please select a password to add service"))
            return
        service = self.service_input.text().strip()
        if not service:
            QMessageBox.warning(self, _("Warning"), _("Please enter a service name"))
            return
        password = self.decrypted_passwords[selected_index]
        self.edit_password_list.takeItem(selected_index)
        self.edit_password_list.insertItem(selected_index, f"{password} - {service}")
        self.decrypted_passwords[selected_index] = f"{password} - {service}"
        logging.info("Service added successfully.")

    def save_decrypted_passwords_with_services(self):
        file_path, _ = QFileDialog.getSaveFileName(self, _("Save decrypted passwords with services"), "", "Text files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for password in self.decrypted_passwords:
                        file.write(password + "\n")
                logging.info("Decrypted passwords with services saved successfully.")
                QMessageBox.information(self, _("Success"), _("Decrypted passwords with services saved"))
            except Exception as e:
                logging.error(f"Error saving decrypted passwords with services: {e}")
                QMessageBox.critical(self, _("Error"), _("Failed to save decrypted passwords with services: ") + str(e))

if __name__ == '__main__':
    REPO_PATH = os.path.dirname(os.path.abspath(__file__))
    update_from_github(REPO_PATH)
    app = QApplication(sys.argv)
    ex = PasswordManagerApp()
    ex.show()
    sys.exit(app.exec_())
