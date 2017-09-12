# -*- coding: utf-8 -*-

import sys
# import FileDialog # important to exe build!
from PyQt5.QtWidgets import QApplication, QMainWindow
from controllers.main_window import MainWindow

if __name__ == "__main__":
    # base qt init
    qtApp = QApplication(sys.argv)
    qtWindow = QMainWindow()
    mainWindow = MainWindow()
    mainWindow.setupUi(qtWindow)

    # TODO: it is a really dirty solution for closing all the dialogs (non-modal, non-blocking) when the main window
    # closes. It should be solved by connecting or overriding the main windows' closeEvent.
    # Should be fixed soon, it is really an abusive solution.
    qtWindow.__setattr__('closeEvent', lambda x: qtApp.quit())

    # additional init
    mainWindow.init_component(qtWindow)

    # show & run
    qtWindow.show()
    sys.exit(qtApp.exec())