import sys
import os
import ntpath
import shutil
import img_processing as imgp
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from functools import partial
import uuid


class GUI(QWidget):
    # instance variable

    OUTPUT_PATH = os.path.expanduser('~{}Pictures{}pnu-newsletter'.format(os.path.sep,os.path.sep))

    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):

        """
        layout:
            1. uploading: image that could be clicked
            2. input_details: grid layout
            3. output_details: grid layout
            4. start: a button to start the image processing
        """
        self.start_process()

        uploading_image = QPixmap('image/drag-drop-file.png')
        uploading_label = QLabel(self)
        uploading_label.setPixmap(uploading_image)

        self.input_details = QVBoxLayout()

        output_details = QGridLayout()
        path_label = QLabel('output path:')
        self.path = QLabel(self.OUTPUT_PATH)
        change_button = QPushButton('change')
        output_details.addWidget(path_label, 1, 0)
        output_details.addWidget(self.path, 1, 2)
        output_details.addWidget(change_button, 1, 10)

        self.start_button = QPushButton('Start!')
        self.err_message = "To start, there must be exactly 5 ads"
        self.error_label = QLabel(self.err_message)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(uploading_label)
        self.layout.addLayout(self.input_details)
        self.layout.addLayout(output_details)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.error_label)

        self.setLayout(self.layout)

        self.setAcceptDrops(True)
        self.setFixedWidth(700)

        self.show()

        uploading_label.mousePressEvent = self.load_image_folder
        change_button.clicked.connect(self.change_path)
        self.start_button.clicked.connect(self.start)
        self.start_button.setEnabled(False)
        return

    def start_process(self):
        self.process_id = str(uuid.uuid4())
        print("new process {}".format(self.process_id))
        self.setWindowTitle('PNU newsletter by reem-codes | process {}'.format(self.process_id))
        self.img_process_path = 'image/proc_{}/'.format(self.process_id)
        self.filenames = []
        self.imgs = []
        return

    def change_path(self):
        self.OUTPUT_PATH = str(QFileDialog.getExistingDirectory(self, 'choose'))
        if self.OUTPUT_PATH:
            self.path.setText(self.OUTPUT_PATH)
        return

    def load_image_folder(self, event):
        filters = "Images (*.png *.xpm *.jpg *.jpeg *.gif)"
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open file', filter=filters)
        self.filenames.extend(filenames)
        self.load_image()
        return

    def load_image(self):

        for i in reversed(range(self.input_details.count())):
            layout = self.input_details.itemAt(i).layout()
            for j in reversed(range(layout.count())):
                layout.itemAt(j).widget().setParent(None)
            self.input_details.removeItem(layout)

        for x in range(len(self.filenames)):
            img_detail = dict()
            img_id = str(uuid.uuid4())[:8]
            f = self.filenames[x]
            head, filename = ntpath.split(f)
            fn, ext = os.path.splitext(filename)
            img_detail['img_id'] = img_id
            img_detail['ext'] = ext
            img_detail['path'] = os.path.abspath(self.img_process_path)
            img_detail['filepath'] = os.path.abspath(self.img_process_path) + '/' + img_id + ext
            self.imgs.append(img_detail)

            newpath = os.path.abspath(self.img_process_path)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            # shutil.copy2(f, os.path.abspath(self.img_process_path))
            shutil.copy(f, img_detail['filepath'])

            pixmap = QPixmap(f)
            pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(pixmap)
            filepath = QLabel(f)

            del_btn = QPushButton("x")
            del_btn.setFixedSize(25, 25)
            input = QHBoxLayout()
            input.addWidget(label)
            input.addWidget(filepath)
            input.addWidget(del_btn)
            del_btn.clicked.connect(partial(self.delete_img, img_id, input, f))  # self.delete_img

            self.input_details.addLayout(input)

        if len(self.filenames) is 5:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)
            self.error_label.setText(self.err_message)
        return

    def delete_img(self, img_id, layout, f):
        for i in range(len(self.imgs)):
            if img_id is self.imgs[i]['img_id']:
                x = i
        img_pth = self.img_process_path + img_id
        if os.path.exists(img_pth):
            os.remove(img_pth)

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        self.input_details.removeItem(layout)
        self.filenames.remove(f)
        self.imgs.pop(x)

        if len(self.filenames) is 5:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)
            self.error_label.setText(self.err_message)
        return

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
        return

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
        return

    def dropEvent(self, e):
        if e.mimeData().hasUrls:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            print(self.filenames)
            for url in e.mimeData().urls():
                self.filenames.append(str(url.toLocalFile()))
            print(self.filenames)

            self.load_image()
        else:
            e.ignore()
        return

    def start(self):
        imgp.main(self.path.text(), self.imgs, self.process_id)
        self.error_label.setText('process {} is Done :D'.format(self.process_id))
        if os.path.exists(self.img_process_path):
            shutil.rmtree(self.img_process_path)
        for i in reversed(range(self.input_details.count())):
            layout = self.input_details.itemAt(i).layout()
            for j in reversed(range(layout.count())):
                layout.itemAt(j).widget().setParent(None)
            self.input_details.removeItem(layout)
        self.start_process()
        return

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == (Qt.Key_Enter or Qt.Key_Space):
            self.start()
        return

    def closeEvent(self, event):
        if os.path.exists(self.img_process_path):
            shutil.rmtree(self.img_process_path)
        return


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())

