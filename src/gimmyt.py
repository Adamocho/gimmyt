import sys
from datetime import date

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                             QVBoxLayout, QWidget, QWizard)
from pytube import YouTube


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.yt = None
        self.video = None
        self.a = 4
        self.first = True
        self.setGeometry(800, 300, 451, 156)  # position x, position y, width, height
        self.setFixedWidth(451)
        self.setFixedHeight(156)
        self.setWindowTitle("YT Downloader")

        self.tbox1 = QtWidgets.QLineEdit(self)
        self.tbox2 = QtWidgets.QLineEdit(self)
        self.button1 = QtWidgets.QPushButton(self)
        self.button2 = QtWidgets.QPushButton(self)
        self.button3 = QtWidgets.QPushButton(self)
        self.buttona = QtWidgets.QPushButton(self)
        self.buttonb = QtWidgets.QPushButton(self)
        self.buttonc = QtWidgets.QPushButton(self)
        self.buttond = QtWidgets.QPushButton(self)
        self.combobox = QtWidgets.QComboBox(self)

        self.initUI()

    def initUI(self):
        self.tbox1.setGeometry(0, 0, 450, 35)
        self.tbox1.setPlaceholderText("Here you paste your YT link")
        self.tbox1.setFont(QFont('MS Shell Dlg 2', 12))

        self.tbox2.setGeometry(0, 36, 414, 35)
        self.tbox2.setPlaceholderText("Here you paste/choose your directory")
        self.tbox2.setFont(QFont('MS Shell Dlg 2', 12))

        self.button1.setGeometry(414, 35, 37, 37)
        self.button1.setText("...")
        self.button1.clicked.connect(self.on_click1)

        self.button2.setGeometry(-1, 126, 352, 30)
        self.button2.setText("Download")
        self.button2.clicked.connect(self.on_click2)

        self.button3.setGeometry(351, 126, 100, 30)
        self.button3.setText("Reset")
        self.button3.clicked.connect(self.on_click3)

        self.buttona.setGeometry(-1, 71, 116, 25)
        self.buttonb.setGeometry(112, 71, 115, 25)
        self.buttonc.setGeometry(224, 71, 115, 25)
        self.buttond.setGeometry(336, 71, 115, 25)
        self.buttona.setText("Audio")
        self.buttonb.setText("Video")
        self.buttonc.setText("Both")
        self.buttond.setText("All")
        self.buttona.clicked.connect(self.on_clicka)
        self.buttonb.clicked.connect(self.on_clickb)
        self.buttonc.clicked.connect(self.on_clickc)
        self.buttond.clicked.connect(self.on_clickd)

        self.combobox.setGeometry(-1, 96, 451, 30)

        self.show()

    # Selecting directory
    def on_click1(self):
        self.tbox2.setText(QFileDialog.getExistingDirectory(self, 'Choose Folder', 'C\\'))

    # Reset everything
    def on_click3(self):
        self.tbox1.clear()
        self.yt = None
        self.combobox.clear()
        self.tbox2.clear()

    # User choices
    def on_clicka(self):
        self.a = 1
        self.on_click4()

    def on_clickb(self):
        self.a = 2
        self.on_click4()

    def on_clickc(self):
        self.a = 3
        self.on_click4()

    def on_clickd(self):
        self.a = 4
        self.on_click4()

    # Text appearing in combobox
    def on_click4(self):
        if self.tbox1.text():
            try:
                ytlist = []
                if self.yt is None:  # self.first or self.yt is None:
                    self.yt = YouTube(self.tbox1.text())
                    self.first = False

                # If it's the shorter version of yt link, check this
                elif len(self.tbox1.text()) == 28 and self.tbox1.text()[17:] != self.yt.watch_url[28:]:
                    self.yt = YouTube(self.tbox1.text())

                # If it's the longer version, check this
                elif len(self.tbox1.text()) > 28 and self.tbox1.text()[32:43] != self.yt.watch_url[28:]:
                    self.yt = YouTube(self.tbox1.text())

                self.combobox.clear()

                # Check which option user picked, and loop through + add that list to combobox
                if self.a == 1:
                    for i in self.yt.streams.filter(only_audio=True):
                        ytlist.append(str(i))

                elif self.a == 2:
                    for i in self.yt.streams.filter(only_video=True):
                        ytlist.append(str(i))

                elif self.a == 3:
                    for i in self.yt.streams.filter(progressive=True):
                        ytlist.append(str(i))

                elif self.a == 4:
                    for i in self.yt.streams:
                        ytlist.append(str(i))

                self.combobox.addItems(ytlist)
                # For debug purposes
                print(ytlist)

            except Exception as ex: # Exception will appear in console
                print(ex)

    # Downloading process // dir mustn't be empty
    def on_click2(self):
        if self.tbox2.text():
            try:
                path = ''
                today = date.today()
                tag = self.combobox.currentText()[13: 20].split('"')
                self.video = self.yt.streams.get_by_itag(int(tag[1]))

                for i in self.tbox2.text():
                    if i == chr(92):
                        path += i * 2
                    else:
                        path += i
                print(path)

                self.video.download(path)  # filename=self.yt.title + today.strftime("%d/%m/%Y")

            except Exception as ex:  # Exception will appear in console
                print(ex)


# If this is the only file
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
