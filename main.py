import os
import sys

from PyQt5 import QtWidgets

import encode
import decode
from main_ui import Ui_MainWindow


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.browse_btn.clicked.connect(self.get_filepath)
        self.browse_btn2.clicked.connect(self.get_filepath)
        self.browse_btn3.clicked.connect(self.get_filepath)
        self.encode_btn.clicked.connect(self.encode_img)
        self.recoverqr_btn.clicked.connect(self.recover_qr)
        self.decrypt_btn.clicked.connect(self.decrypt)

        self.show()

    def get_filepath(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'File', os.getenv('HOME'))

        if self.sender().objectName() == "browse_btn":
            self.lineEdit_cover_tab1.setText(filename[0])
        elif self.sender().objectName() == "browse_btn2":
            self.lineEdit_cover_tab2.setText(filename[0])
        elif self.sender().objectName() == "browse_btn3":
            self.lineEdit_stego_tab2.setText(filename[0])

    def encode_img(self):
        encode.embed(self.lineEdit_cover_tab1.text(), self.lineEdit_key_tab1.text(),
                     self.plainTextEdit_data_tab1.toPlainText())

    def recover_qr(self):
        decode.recover(self.lineEdit_stego_tab2.text(), self.lineEdit_cover_tab2.text())

    def decrypt(self):
        msg = decode.aes_decrypt(self.lineEdit_key_tab2.text(), self.plainTextEdit_enc_tab2.toPlainText())
        QtWidgets.QMessageBox.about(self, "Message", msg)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
