import sys, glob, serial
from PyQt5 import QtWidgets

class MainViewController(object):

    def __init__(self):
        pass

    def updateSerialPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsuported plaftorm')

        self.list_ports.clear()

        for port in ports:
            self.list_ports.addItem(port)

    def updateSerialConfigurations(self):
        config = serial.Serial(self.list_ports.currentItem().text())
        print(config)
        self.comboBox_baudrate.addItem(str(config.baudrate), 1)
        self.comboBox_bytesize.addItem(str(config.bytesize), 1)
        self.comboBox_parity.addItem(str(config.parity), 1)
        self.comboBox_stopbits.addItem(str(config.stopbits), 1)
        self.comboBox_timeout.addItem(str(config.timeout), 1)
        config.close()

    def editPortConfig(self):
        print("Editando as configurações da porta serial")
        self.btn_savePortConfig.setEnabled(True)

    def savePortConfig(self):
        print("Configuração da porta salva")
        self.btn_savePortConfig.setEnabled(False)