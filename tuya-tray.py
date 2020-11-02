import sys
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon,QMenu,QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from tuyapy import TuyaApi
import os
import time
from functools import partial
import json

api = TuyaApi()

class SystemTrayIcon(QSystemTrayIcon):
    
    def __init__(self,parent=None):
        super().__init__()
        QSystemTrayIcon.__init__(self,parent)
        self.setIcon(QIcon('lightbulb.png'))
        self.setToolTip('Tray - Lights')
        self.menu = QMenu()
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

    def change_colour(self,device):
        colors = QColorDialog.getColor()
        h,s,v,t = colors.getHsv()
        s = int((s/255 * 100))
        if s < 60:
            s = 60
        is_list = isinstance(device,list)
        if is_list == False:
            return device.set_color([h,s,100])
        else:
            return [i.set_color([h,s,100]) for i in device]

    def initUI(self):
        
        with open('config.json') as config:
            data = json.load(config)
            
        username,password,country_code,application = data['username'],data['password'],data['country_code'],data['application']
        api.init(username,password,country_code,application)
        self.device_ids = api.get_all_devices()
        self.switch = dict(sorted(dict((i.name(),i) for i in self.device_ids if i.obj_type == 'switch').items()))
        self.switch['All Switches'] = list(self.switch.values())
        self.lights = dict(sorted(dict((i.name(),i) for i in self.device_ids if i.obj_type == 'light').items()))
        self.lights['All Lights'] = list(self.lights.values())
        self.devices = {**self.switch,**self.lights}
        self.menus = dict()
        self.counter = 0
        
        for j in self.devices.keys():
            if isinstance(self.devices[j],list) == False and self.devices[j].obj_type == 'light':
                if self.counter == 0:
                    self.menu.addSeparator()
                    self.counter += 1
            self.menus[f"{j}_Action"] = self.menu.addMenu(j)
            if j in self.lights.keys():
                on_menu = self.menus[f"{j}_Action"].addMenu('On')
                on = on_menu.addAction('On')
                colour_wheel = on_menu.addAction('Light Colour')
                colour_wheel.triggered.connect(partial(self.change_colour,self.devices[j]))
            else:
                on = self.menus[f"{j}_Action"].addAction('On')
                
            off = self.menus[f"{j}_Action"].addAction('Off')
            on.triggered.connect(partial(self.turn_on,self.devices[j]))
            off.triggered.connect(partial(self.turn_off,self.devices[j]))

        exitaction = self.menu.addAction('Exit')
        exitaction.triggered.connect(QCoreApplication.quit)
        self.setContextMenu(self.menu)
        self.show()

if __name__ == "__main__":
    app= QApplication.instance() # checks if QApplication already exists 
    if not app: # create QApplication if it doesnt exist 
        app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray = SystemTrayIcon()
    sys.exit(app.exec_())