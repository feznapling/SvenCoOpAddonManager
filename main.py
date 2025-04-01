import sys, os, shutil, errno
import addons
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from pathlib import Path

from UI.main_window.mainwindow import Ui_MainWindow

class EmittingStream(qtc.QObject):
    textWritten = qtc.Signal(str)

    def write(self, text):
        #cleaned_text = str(text).replace('\n', '')
        self.textWritten.emit(str(text))

    def flush(self):
        pass

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self): 
        super().__init__()
        self.setupUi(self)

        sys.stdout = EmittingStream(textWritten=self.print_to_log)

        self.setup_dirs()
        self.inactive_list.clear()
        self.active_list.clear()
        self.start_button.clicked.connect(lambda: self.print_to_log("testo\n"))
        self.enable_button.clicked.connect(lambda: self.enable_addon(self.inactive_list.currentItem().text()))
        self.disable_button.clicked.connect(lambda: self.disable_addon(self.active_list.currentItem().text()))

    def __del__(self):
        sys.stdout = sys.__stdout__

    def setup_dirs(self):
        pass

    @qtc.Slot()
    def print_to_log(self, string):
        self.log_box.insertPlainText(string)
        self.log_box.ensureCursorVisible()

    @qtc.Slot()
    def get_addon_list(self):
        self.inactive_list.clear()
        self.active_list.clear()
        addons_dir = Path.joinpath(Path(os.getcwd()), 'addons')
        active_addons_file = os.path.abspath(addons_dir) + "\\active_addons.txt"
        addon_list = []
        active_addon_list = []

        for addon in os.listdir(addons_dir):
            addon_src = Path.joinpath(addons_dir, addon)
            if os.path.isdir(addon_src):
                addon_list.append(addon.strip("\n"))

        with open(active_addons_file, "r") as file:
            for line in file:
                active_addon_list.append(line.strip("\n"))
                self.active_list.addItem(line.strip("\n"))

        for addon in addon_list:
            if addon not in active_addon_list:
                self.inactive_list.addItem(addon.strip("\n"))

    @qtc.Slot()
    def enable_addon(self, addon):
        addons.enable_addon(addon)
        self.get_addon_list()

    @qtc.Slot()
    def disable_addon(self, addon):
        addons.disable_addon(addon)
        self.get_addon_list()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.get_addon_list()
    #addons.enable_addon("coolmod")
    #addons.disable_addon("coolmod")
    sys.exit(app.exec())