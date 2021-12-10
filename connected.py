from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty
import os
import requests

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from kivy.storage.jsonstore import JsonStore

import serial
import serial.tools.list_ports


class MyStack(StackLayout):
    pass


class Connected(Screen):
    dialog = None
    store = JsonStore('auth.json')
    port_value = ""
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        if self.store.exists('user'):
            self.store.delete('user')
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def submitData(self):
        uld_number = self.ids.uld_number.text
        station_code = self.ids.station_code.text
        destination_code = self.ids.destination_code.text
        carrier_code = self.ids.carrier_code.text
        transport_number = self.ids.transport_number.text
        weight = self.ids.weight.text
        print(self.store.get('user')['userid'])
        dataReq = {
            'uld_number': uld_number,
            'station_code': station_code,
            'destination_code': destination_code,
            'carrier_code': carrier_code,
            'transport_number': transport_number,
            'weight': weight,
            # 'userid': self.store.get('user')['userid']
        }
        for key in dataReq:
            if dataReq[key] and dataReq[key].strip():
                pass
            else:
                self.onPopPress("Missing field: " + key)
                return

        url = 'https://seyclock.com/api/v1/submit-weight'
        response = requests.post(url, data = dataReq)
        resData = response.json()['success']

        print(resData)

        if resData['passed'] == 1:
            self.onPopPress("Data successfully sent!")
            self.resetForm()
        else:
            self.onPopPress("Error processing data!")
            self.resetForm()


    def onPopPress(self, message):
          
        layout = GridLayout(cols = 1, padding = 5)
  
        popupLabel = Label(text = message)
        closeButton = Button(text = "Close")
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
  
        # Instantiate the modal popup and display
        popup = Popup(title ='Alert',
                      content = layout,
                      size_hint =(None, None), size =(400, 400))  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)


    def resetForm(self):
        self.ids.uld_number.text = ""
        self.ids.station_code.text = ""
        self.ids.destination_code.text = ""
        self.ids.carrier_code.text = ""
        self.ids.transport_number.text = ""
        self.ids.weight.text = ""

    def readWeight(self):
        port_number = self.ids.port_number.text
        ports = serial.tools.list_ports.comports()
        self.port_value = ""
        port_list = []

        if(len(port_list) < 1):
            self.onPopPress("No ports opened or available!")
            return

        for sel_port in ports:
            port_list.append(str(sel_port))

        for x in range(0, len(port_list)):
            if port_list[x].startswith(port_number):
                self.port_value = port_number
        
        if self.port_value and self.port_value.strip():
            pass
        else:
            self.onPopPress("Port Selected not available!")
            return
        

        serialBout = serial.Serial()
        serialBout.port = port_number
        serialBout.open()

        packet = serialBout.readline()
        self.ids.weight.text = packet.decode("utf").rstrip("\n")
