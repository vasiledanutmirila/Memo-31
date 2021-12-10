from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QLabel, \
    QLineEdit, QTextEdit
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initialWindow()

    def initialWindow(self):
        self.setWindowTitle("Memo")
        self.setGeometry(200, 200, 1080, 720)

        vbox = QVBoxLayout()
        textButton = QPushButton("Text")
        textButton.setFont(QFont("Arial", 14))
        textButton.setFixedSize(150, 50)
        textButton.clicked.connect(self.textButtonAction)

        shopButton = QPushButton("Lista cumparaturi")
        shopButton.setFont(QFont("Arial", 14))
        shopButton.setFixedSize(250, 50)

        vbox.addWidget(textButton, alignment=Qt.AlignCenter)
        vbox.addWidget(shopButton, alignment=Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def textButtonAction(self):
        print("text button pressed")
        vbox = QVBoxLayout()
        label = QLabel("TEXT", self)
        label.setFont(QFont("Arial", 14))
        labelBox = QVBoxLayout()
        labelBox.addWidget(label, alignment=Qt.AlignHCenter)
        vbox.addLayout(labelBox)

        text = QTextEdit()
        textBox = QVBoxLayout()
        textBox.addWidget(text)

        vbox.addLayout(textBox)

        bottomBox = QHBoxLayout()
        backButton = QPushButton("Inapoi")
        backButton.setFont(QFont("Arial", 12))
        backButton.clicked.connect(self.backButtonAction)
        bottomBox.addWidget(backButton)

        saveButton = QPushButton("Salveaza")
        saveButton.setFont(QFont("Arial", 12))
        bottomBox.addWidget(saveButton)

        vbox.addLayout(bottomBox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def backButtonAction(self):
        print("back button pressed")
        self.initialWindow()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec()
