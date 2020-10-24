import sys
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon,QMenu
from PyQt5.QtGui import QIcon
from tuyapy import TuyaApi
import os
import time
from functools import partial
api = TuyaApi()

def turn_on(device):
    return device.turn_on()
def turn_off(device):
    return device.turn_off()

def main():
    api.init(os.getenv('TUYA_LOGIN'),os.getenv('TUYA_PASSWORD'),"44","tuya")
    device_id = api.get_all_devices()
    devices = dict((i.name(),i) for i in device_id if i.obj_type == 'light')

    app = QApplication(sys.argv)

    tray_icon = QSystemTrayIcon(QIcon('lightbulb.png'),parent=app)

    tray_icon.setToolTip('Tuya - Lights')
    tray_icon.show()
    menu = QMenu()

    menus = dict()
    buttons = dict()
    for j in (devices.keys()):
        menus[f"{j}_Action"] = menu.addMenu(j)
        menus[f"{j}_Action"].addAction('On')
        menus[f"{j}_Action"].addAction('Off')
        buttons = menus[f"{j}_Action"].actions()
        for i in buttons:
            if i.iconText() == 'On':
                i.triggered.connect(partial(turn_on,devices[j]))
            elif i.iconText() == 'Off':
                i.triggered.connect(partial(turn_off,devices[j]))

    exitaction = menu.addAction('Exit')
    exitaction.triggered.connect(app.quit)
    tray_icon.setContextMenu(menu)
    app.exec_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    while True:
        main()