from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QLabel
import sys
from pathlib import Path

from utils.filesystem import find_resource_path


class MainWindow(QMainWindow):
    def __init__(self, bot_task):
        super(MainWindow, self).__init__()
        self.bot_task = bot_task

        self.setWindowTitle('Абитуриент БГУ')
        self.setWindowIcon(QIcon(find_resource_path('data/icon.ico')))
        self.setMinimumSize(QSize(300, 200))
        label = QLabel('Бот запущен!')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

    def closeEvent(self, event):
        print("Закрытие окна. Останавливаем бота...")
        if not self.bot_task.done():
            self.bot_task.cancel()
        event.accept()
