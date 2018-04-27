import sys
from PyQt5 import QtWidgets

from views.MainView import MainView
from controllers.MainViewController import MainViewController

class App(QtWidgets.QApplication):

    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_ctrl = MainViewController()
        self.main_ctrl.show()


if __name__ == '__main__':

    app = App(sys.argv)
    sys.exit(app.exec_())