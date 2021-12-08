from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty
import os
import requests

class MyStack(StackLayout):
    pass


class Connected(Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def submitData(self):
        uld_number = self.ids.uld_number.text
        station_code = self.ids.station_code.text
        destination_code = self.ids.destination_code.text
        carrier_code = self.ids.carrier_code.text
        transport_number = self.ids.transport_number.text
        weight = self.ids.weight.text
        dataReq = {
            'uld_number': uld_number,
            'station_code': station_code,
            'destination_code': destination_code,
            'carrier_code': carrier_code,
            'transport_number': transport_number,
            'weight': weight
        }
        url = 'http://localhost:8000/api/v1/submit-weight'
        response = requests.post(url, data = dataReq)
        resData = response.json()['success']
        print(resData['passed'])