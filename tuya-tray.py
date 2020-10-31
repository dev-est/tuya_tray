import sys
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon,QMenu
from PyQt5.QtGui import QIcon
from tuyapy import TuyaApi
import os
import time
from functools import partial
import json

api = TuyaApi()

class tray():
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def turn_off(self,device):
        is_list = isinstance(device,list)
        if is_list == False:
            return device.turn_off()
        else:
            return [i.turn_off() for i in device]

    def turn_on(self,device):
        is_list = isinstance(device,list)
        if is_list == False:
            return device.turn_on()
        else:
            return [i.turn_on() for i in device] 
    
    def initUI(self):
        self.app = QApplication(sys.argv)
        with open('config.json') as config:
            data = json.load(config)
        username,password,country_code,application = data['username'],data['password'],data['country_code'],data['application']
        api.init(username,password,country_code,application)
        self.device_ids = api.get_all_devices()
        self.switch = dict(sorted(dict((i.name(),i) for i in self.device_ids if i.obj_type == 'switch').items()))
        self.switch['All Switches'] = list(self.switch.values())
        self.lights = dict(sorted(dict((i.name(),i) for i in self.device_ids if i.obj_type == 'light').items()))
        self.devices = {**self.switch,**self.lights}
        self.devices['All Lights'] = list(self.lights.values())
        self.tray_icon = QSystemTrayIcon(QIcon('lightbulb.png'),parent=self.app)
        self.tray_icon.setToolTip('Tray - Lights')
        self.menu = QMenu()
        self.menus = dict()
        self.buttons = dict()
        self.counter = 0
        for j in self.devices.keys():
            if isinstance(self.devices[j],list) == False and self.devices[j].obj_type == 'light':
                if self.counter == 0:
                    self.menu.addSeparator()
                    self.counter += 1
            self.menus[f"{j}_Action"] = self.menu.addMenu(j)
            self.menus[f"{j}_Action"].addAction('On')
            self.menus[f"{j}_Action"].addAction('Off')
            self.buttons = self.menus[f"{j}_Action"].actions()
            for i in self.buttons:
                if i.iconText() == 'On':
                    i.triggered.connect(partial(self.turn_on,self.devices[j]))
                elif i.iconText() == 'Off':
                    i.triggered.connect(partial(self.turn_off,self.devices[j]))

        self.exitaction = self.menu.addAction('Exit')
        self.exitaction.triggered.connect(self.app.quit)
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()
        self.app.exec_()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = tray()