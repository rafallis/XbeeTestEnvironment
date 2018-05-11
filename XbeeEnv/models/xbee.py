from digi.xbee.devices import XBeeDevice
from digi.xbee.util import utils
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.models.status import PowerLevel
import serial
import time
import logging


class Device:
    PORT = ''
    BAUD_RATE = ''

    # Grupo de parametros que podem ser setados, nota-se que não são necessariamente os mesmo que podem ser obtidos do xbee.------
    PARAM_NODE_ID = "NI"
    PARAM_PAN_ID = "ID"
    PARAM_DEST_ADDRESS_H = "DH"
    PARAM_DEST_ADDRESS_L = "DL"
    # Valores exemplo
    PARAM_VALUE_NODE_ID = "Yoda"
    PARAM_VALUE_PAN_ID = utils.hex_string_to_bytes("1234")
    PARAM_VALUE_DEST_ADDRESS_H = utils.hex_string_to_bytes("00")
    PARAM_VALUE_DEST_ADDRESS_L = utils.hex_string_to_bytes("FFFF")
    # -------------

    local_xbee = None
    remote_xbee = None
    SixFourBitAddress = ""

    def __init__(self):
        super(Device, self).__init__()

    # Precisa ser chamado toda vez que um xbee remoto for criado. O endereço deve ser previamente conhecido. Pode ser que haja uma maneira melhor.
    def set_64bitaddres(self, adress):
        self.SixFourBitAddress = adress

    def set_port(self, porta):
        self.PORT = porta

    def get_port(self):
        return self.PORT

    def set_baudrate(self, baud):
        self.BAUD_RATE = baud

    def get_baudrate(self):
        return self.BAUD_RATE

    def create_nodes(self, numero):
        self.local_xbee = XBeeDevice(PORT, BAUND_RATE)
        for x in range(0, numero - 2):
            self.remote_xbee[x] = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string(SixFourBitAddress))

    def open_connection(self):
        self.local_xbee.open()

    # retorna uma lista com os parâmetros
    def get_Device_Information(self, xbee):
        addr_64 = xbee.get_64bit_addr()
        node_id = xbee.get_node_id()
        hardware_version = xbee.get_hardware_version()
        firmware_version = xbee.get_firmware_version()
        protocol = xbee.get_protocol()
        operating_mode = xbee.get_operating_mode()
        dest_addr = xbee.get_dest_address()
        pan_id = xbee.get_pan_id()
        power_lvl = xbee.get_power_level()
        lista_result = [addr_64, node_id, hardware_version, firmware_version, protocol, operating_mode, dest_addr,
                        pan_id, power_lvl]
        return lista_result

    # Recebe um dicionário com parâmetros
    def set_Device_Information(self, xbee, dicionario_paramentros):
        for key in dicionario_parametros:
            if key == 'PARAM_VALUE_NODE_ID':
                self.PARAM_VALUE_NODE_ID = dicionario_parametros.get('PARAM_VALUE_NODE_ID')
            if key == 'PARAM_VALUE_PAN_ID':
                self.PARAM_VALUE_PAN_ID = dicionario_parametros.get('PARAM_VALUE_PAN_ID')
            if key == 'PARAM_VALUE_DEST_ADDRESS_H':
                self.PARAM_VALUE_DEST_ADDRESS_H = dicionario_parametros.get('PARAM_VALUE_DEST_ADDRESS_H')
            if key == 'PARAM_VALUE_DEST_ADDRESS_L':
                self.PARAM_VALUE_DEST_ADDRESS_L = dicionario_parametros.get('PARAM_VALUE_DEST_ADDRESS_L')

        xbee.set_parameter(self.PARAM_NODE_ID, bytearray(self.PARAM_VALUE_NODE_ID, 'utf8'))
        xbee.set_parameter(self.PARAM_PAN_ID, self.PARAM_VALUE_PAN_ID)
        xbee.set_parameter(self.PARAM_DEST_ADDRESS_H, self.PARAM_VALUE_DEST_ADDRESS_H)
        xbee.set_parameter(self.PARAM_DEST_ADDRESS_L, self.PARAM_VALUE_DEST_ADDRESS_L)

    def close_connection(self):
        self.local_xbee.close()

    def reset_device(self, xbee):
        self.xbee.reset()

    def discover_network(self):
        xnet = self.local_xbee.get_network()
        xnet.set_discovery_options(
            {DiscoveryOptions.APPEND_DD, DiscoveryOptions.DISCOVERY_MYSELF, DiscoveryOptions.APEND_RSSI})
        xnet.set_discovery_timeout(15)
        xnet.start_discovery_process()
        while xnet.is_discovery_running():
            time.sleep(0.5)
        devices = xnet.get_devices()
        iterator = iter(devices)
        lista_nos
        while iterator.next() is not None:
            lista_nos.append(get_Device_Information(iterator.next()))
        return lista_nos

    def send_synchronous_data(self, remote_xbee, string):
        self.local_xbee.send_data(remote_xbee, string)

    # timeout está em segundos.
    def set_timeout_synchronous_data(self, timeout):
        self.local_xbee.set_sync_ops_timeout(timeout)

    def get_timeout_synchronous_data(self):
        return self.local_xbee.get_sync_ops_timeout()

    def send_broadcast_data(self, string):
        self.local_xbee.send_data_broadcast(string)

    # Definição do callback para recepção de mensagem.
    def my_data_received_callback(self, xbee_message, remote_xbee):
        address = xbee_message.remote_xbee.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        print("Received data from %s: %s" % (address, data))

    # recebe mensagens por <timer> segundos
    def receive_data(self, timer):
        for y in range(0, timer - 1):
            self.local_xbee.add_data_received_callback(my_data_received_callback)
        self.local_xbee.del_data_received_callback(my_data_recived_callback)

    # Precisa de testes para ver como é a saída dos dados e como isso será passado para interface.
    # Há uma maneira alternativa de se fazer, ver documentação.
    def log(self):
        # enable log
        dev_logger = enable_logger(digi.xbee.devices.__name__, logging.INFO)
