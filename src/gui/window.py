import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, \
                        QLabel, QPushButton, QFileDialog, QLineEdit
from functools import partial
import uuid
import ntpath
import shutil
from src.processing import layout


class GridLayout(QWidget):
    def __init__(self, num, p_id, p_path, parent=None):
        super(GridLayout, self).__init__(parent)
        self.num = num
        self.process_id = p_id
        self.img_process_path = p_path
        self.filenames = [None] * self.num
        self.imgs = [None] * self.num
        self.init_ui()

    def init_ui(self):
        self.start_button = QPushButton('next', self)
        self.start_button.setEnabled(False)
        self.err_message = 'you need to fill them all before proceeding'
        self.error_lbl = QLabel(self)

        grid = QGridLayout()
        for x in range(0, self.num):
            btn = QPushButton('{}'.format(x))
            grid.addWidget(btn, x / 2,  0 if x % 2 == 0 else 1)
            btn.clicked.connect(partial(self.load_image_folder, x))

        self.layout = QVBoxLayout()
        self.layout.addLayout(grid)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.error_lbl)

        self.setLayout(self.layout)

    def load_image_folder(self, x, event):
        sender = self.sender()
        filters = "Images (*.png *.xpm *.jpg *.jpeg *.gif)"
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', filter=filters)
        if filename:
            if self.filenames[x]:
                os.remove(self.imgs[x]['filepath'])
            self.filenames[x] = filename
            self.load_image(x)
            sender.setText("edit")

    def load_image(self, x):
        img_detail = dict()
        f = self.filenames[x]
        head, filename = ntpath.split(f)
        fn, ext = os.path.splitext(filename)
        img_detail['filename'] = fn
        img_detail['ext'] = ext
        img_detail['position'] = x
        img_detail['filepath'] = os.path.abspath(self.img_process_path) + '/' + filename
        self.imgs[x] = img_detail

        newpath = os.path.abspath(self.img_process_path)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        shutil.copy(f, img_detail['filepath'])

        if len(self.imgs) is self.num:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)
            self.error_lbl.setText(self.err_message)
        return


class GeneralInfo(QWidget):

    def __init__(self, id, out_path, parent=None):
        super(GeneralInfo, self).__init__(parent)
        # number of pictures layout
        self.process_id = id
        self.OUTPUT_PATH = os.path.expanduser('~{0}Pictures{0}pnu-newsletter'.format(os.path.sep))
        self.NUMBER = 10

        self.init_ui()

    def init_ui(self):

        input_details = QHBoxLayout()
        input_label = QLabel("number of pictures:")
        self.qle = QLineEdit(str(self.NUMBER))
        self.qle.textChanged[str].connect(self.on_number_input)
        input_details.addWidget(input_label)
        input_details.addWidget(self.qle)

        # output path layout
        output_details = QGridLayout()
        path_label = QLabel('output path:')
        self.path = QLabel(self.OUTPUT_PATH)
        change_button = QPushButton('change')
        output_details.addWidget(path_label, 1, 0)
        output_details.addWidget(self.path, 1, 2)
        output_details.addWidget(change_button, 1, 10)
        change_button.clicked.connect(self.change_path)

        self.choose_layout = QPushButton("next", self)
        self.error_lbl = QLabel(self)

        self.layout = QVBoxLayout()
        self.layout.addLayout(input_details)
        self.layout.addLayout(output_details)
        self.layout.addWidget(self.choose_layout)
        self.layout.addWidget(self.error_lbl)

        self.setLayout(self.layout)

    def change_path(self):
        p = str(QFileDialog.getExistingDirectory(self, 'choose', self.OUTPUT_PATH))
        if p:
            self.OUTPUT_PATH = p
            self.path.setText(self.OUTPUT_PATH)
        return

    def on_number_input(self, text):
        try:
            if text is '':
                self.qle.setText(None)

            else:
                self.NUMBER = int(text)
                print(self.get_number())
        except ValueError:
            self.error_lbl.setText('The value entered is not an integer')
            self.qle.setText(str(self.NUMBER))


class Done(QWidget):
    def __init__(self, parent=None):
        super(Done, self).__init__(parent)
        # self.process = process
        self.init_ui()

    def init_ui(self):
        self.make_another = QPushButton("make another")
        self.close_btn = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.make_another)
        hbox.addWidget(self.close_btn)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 400, 450)
        self.setFixedSize(500, 450)
        self.imgs = []

        self.start_general_ui()

    def start_process(self):

        self.process_id = str(uuid.uuid4())
        print("new process {}".format(self.process_id))
        self.img_process_path = '../../image/proc_{}/'.format(self.process_id)

    def start_general_ui(self):
        self.start_process()

        self.general = GeneralInfo(self.process_id, self.img_process_path)
        self.setWindowTitle('PNU newsletter by reem-codes | process {}'.format(self.process_id))
        self.setCentralWidget(self.general)
        self.general.choose_layout.clicked.connect(self.load_grid_images)
        self.show()
        self.NUMBER = self.general.NUMBER
        self.OUTPUT_PATH = self.general.OUTPUT_PATH

    def load_grid_images(self):
        self.grid_layout = GridLayout(self.NUMBER, self.process_id,
                                      self.img_process_path)
        self.setWindowTitle('Chose positions | process {}'.format(self.process_id))

        self.setCentralWidget(self.grid_layout)
        self.grid_layout.start_button.clicked.connect(self.start_process)
        self.show()

    def start_process(self):
        self.image_process = layout.GridLayout(self.grid_layout.imgs, self.OUTPUT_PATH, self.process_id)
        self.done = Done(self)

        self.setCentralWidget(self.done)
        self.done.close_btn.clicked.connect(self.closeEvent)
        self.done.make_another.clicked.connect(self.redo)
        self.show()

    def redo(self):
        self.end_process()
        self.start_general_ui()

    def end_process(self):
        n = os.path.abspath(self.img_process_path)
        print("end process {}".format(self.process_id))
        if os.path.exists(n):
            shutil.rmtree(n)

    def closeEvent(self, event):
        self.end_process()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
