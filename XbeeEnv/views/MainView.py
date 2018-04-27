import sys, os
import serial, glob
from PyQt5 import QtWidgets, uic


class MainView(QtWidgets.QMainWindow):

    def __init__(self, main_controller):
        super(MainView, self).__init__()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'XbeeTestFrame/mainwindow.ui')
        uic.loadUi(filename, self)

        self.init_comboboxes()
        self.connect_actions()

    def init_comboboxes(self):
        self.uart_edit_toggle()

        baudrate_list = [
            '1200',
            '2400',
            '4800',
            '9600',
            '19200',
            '38400',
            '57600',
            '115200'
        ]

        parity_list = [
            'No Parity',
            'Even Parity',
            'Odd Parity',
            'Mark Parity'
        ]

        stopbits_list = [
            '1',
            '2'
        ]

        flowcontrol_list = [
            'No Flow',
            'CTS Flow',
            'Transmit Enable on Low Signal',
            'Transmit Enable on High Signal'
        ]
        # TODO verificar como pode ser setado um valor inicial padrão
        self.comboBox_baudrate.addItems(baudrate_list)
        self.comboBox_parity.addItems(parity_list)
        self.comboBox_stopbits.addItems(stopbits_list)

    def connect_actions(self):
        self.btn_connect.clicked.connect(self.hello)
        self.btn_refresh.clicked.connect(self.update_serial_ports)
        self.list_ports.itemClicked.connect(self.update_serial_configurations)
        self.btn_editPortConfig.clicked.connect(self.edit_uart_config)
        self.btn_savePortConfig.clicked.connect(self.save_uart_config)

    def update_serial_ports(self):
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

    def update_serial_configurations(self):
        config = serial.Serial(self.list_ports.currentItem().text())
        print(config)

        # TODO verificar como instanciar esses valores dinamicamente

        self.comboBox_baudrate.addItem(str(config.baudrate), 1)
        self.comboBox_bytesize.addItem(str(config.bytesize), 1)
        self.comboBox_parity.addItem(str(config.parity), 1)
        self.comboBox_stopbits.addItem(str(config.stopbits), 1)
        self.comboBox_timeout.addItem(str(config.timeout), 1)
        config.close()

    # TODO definir como podem ser gravados os novos dados
    def edit_uart_config(self):
        print("Editando as configurações da porta serial")
        self.uart_edit_toggle(True)
        self.btn_savePortConfig.setEnabled(True)

    # TODO definir como salvar
    def save_uart_config(self):
        print("Configuração da porta salva")
        self.uart.edit_toggle()
        self.btn_savePortConfig.setEnabled(False)

    def uart_edit_toggle(self, editable=False):
        self.comboBox_baudrate.setEnabled(editable)
        self.comboBox_bytesize.setEnabled(editable)
        self.comboBox_parity.setEnabled(editable)
        self.comboBox_stopbits.setEnabled(editable)
        self.comboBox_timeout.setEnabled(editable)

    def serial_connect(self):
        conn = serial.Serial(self.list_ports.currentItem().text())
        print(conn)

    def hello(self):
        print("HELLO")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.setWindowTitle('Xbee Test Environment')
    window.updateSerialPorts()

    sys.exit(app.exec_())