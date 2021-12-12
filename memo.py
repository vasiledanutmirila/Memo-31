from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QLabel, \
    QLineEdit, QTextEdit, QScrollArea, QFormLayout, QGroupBox
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        self.shopList = []
        self.dbConnection = sqlite3.connect("memo.db")
        self.dbCursor = self.dbConnection.cursor()
        super(MainWindow, self).__init__()
        self.initialWindow()

    def initialWindow(self):
        self.setWindowTitle("Memo")
        self.setGeometry(200, 200, 1080, 720)

        vbox = QVBoxLayout()
        createButton("Text", 14, self.textButtonAction, vbox, 150, 50, Qt.AlignCenter)
        createButton("Lista de cumparaturi", 14, self.shopListButtonAction, vbox, 250, 50, Qt.AlignCenter)
        createButton("Istoric", 14, self.historyButtonAction, vbox, 200, 50, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def textButtonAction(self):
        vbox = QVBoxLayout()
        createLabel("TEXT", 14, vbox, Qt.AlignHCenter)

        self.text = QTextEdit()
        vbox.addWidget(self.text)

        bottomBox = QHBoxLayout()
        createButton("Inapoi", 12, self.backButtonAction, bottomBox)
        createButton("Salveaza", 12, self.textSaveButtonAction, bottomBox)

        vbox.addLayout(bottomBox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        self.text.setFocus()

    def backButtonAction(self):
        self.shopList = []
        self.initialWindow()

    def shopListButtonAction(self):
        vbox = QVBoxLayout()
        createLabel("LISTA DE CUMPARATURI", 14, vbox, Qt.AlignHCenter)

        formLayout = QFormLayout()
        groupBox = QGroupBox()
        scroll = QScrollArea()

        for item in self.shopList:
            itemLabel = QLabel(item)
            formLayout.addRow(itemLabel)

        self.itemInputText = QLineEdit()
        formLayout.addRow(self.itemInputText)

        createButton("+", 12, self.plusButtonAction, formLayout)
        groupBox.setLayout(formLayout)

        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        vbox.addWidget(scroll)
        vbar = scroll.verticalScrollBar()
        vbar.setValue(vbar.maximum())

        bottomBox = QHBoxLayout()
        createButton("Inapoi", 12, self.backButtonAction, bottomBox)
        createButton("Salveaza", 12, self.shopListSaveButtonAction, bottomBox)

        vbox.addLayout(bottomBox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        self.itemInputText.setFocus()

    def plusButtonAction(self):
        print(self.itemInputText.text())
        if self.itemInputText.text() != "":
            self.shopList.append(self.itemInputText.text())
        self.shopListButtonAction()

    def textSaveButtonAction(self):
        data = self.text.toPlainText()
        if len(data) != 0:
            print(data)
            self.dbCursor.execute("insert into history values (?, ?)", ("TEXT", data))
            self.dbConnection.commit()
        self.textButtonAction()

    def shopListSaveButtonAction(self):
        if len(self.shopList) != 0:
            data = ",".join(self.shopList)
            print(data)
            self.dbCursor.execute("insert into history values (?, ?)", ("LISTA DE CUMPARATURI", data))
            self.dbConnection.commit()
            self.shopList = []
        self.shopListButtonAction()

    def historyButtonAction(self):
        vbox = QVBoxLayout()
        createLabel("Istoric", 14, vbox, Qt.AlignHCenter)

        formLayout = QFormLayout()
        groupBox = QGroupBox()
        scroll = QScrollArea()

        for row in self.dbCursor.execute('SELECT * FROM history'):
            createLabel(row[0], 16, formLayout, Qt.AlignLeft)
            if row[0] == "TEXT":
                createLabel(row[1], 12, formLayout, Qt.AlignLeft)
            if row[0] == "LISTA DE CUMPARATURI":
                shopListItems = row[1].split(",")
                for item in shopListItems:
                    createLabel(item, 12, formLayout, Qt.AlignLeft)

        groupBox.setLayout(formLayout)
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        vbox.addWidget(scroll)

        createButton("Inapoi", 12, self.backButtonAction, vbox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        self.dbConnection.close()


def createButton(name, size, action, parent, width=0, height=0, align=0):
    button = QPushButton(name)
    button.setFont(QFont("Arial", size))
    if width != 0 and height != 0:
        button.setFixedSize(width, height)
    button.clicked.connect(action)
    if align == 0:
        parent.addWidget(button)
    else:
        parent.addWidget(button, alignment=align)


def createLabel(name, size, parent, align):
    label = QLabel(name)
    label.setFont(QFont("Arial", size))
    if isinstance(parent, QVBoxLayout):
        parent.addWidget(label, alignment=align)
    if isinstance(parent, QFormLayout):
        parent.addRow(label)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec()
