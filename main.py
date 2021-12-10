from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from kivy.core.window import Window

from kivy.storage.jsonstore import JsonStore

from connected import Connected
import requests

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

Window.clearcolor = (1,1,1,1)

class Login(Screen):
    store = JsonStore('auth.json')
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = SlideTransition(direction="left")
        # self.manager.current = 'connected'

        dataReq = {
            'email': self.ids.login.text,
            'password': self.ids.password.text,
        }

        for key in dataReq:
            if dataReq[key] and dataReq[key].strip():
                pass
            else:
                self.onPopPress("Missing field: " + key)
                return

        url = 'https://seyclock.com/api/v1/login'
        response = requests.post(url, data = dataReq)
        resData = response.json()['success']

        print(resData)

        if resData['passed'] == 1:
            self.store.put('user',
                name=resData['user']['name'], email=resData['user']['email'],
                gender=resData['user']['gender'], userid=resData['user']['userid']
            )
            self.resetForm()
            self.manager.current = 'connected'
        else:
            self.onPopPress(resData['message'])
            self.resetForm()

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

    def onPopPress(self, message):
          
        layout = GridLayout(cols = 1, padding = 5)
  
        popupLabel = Label(text = message)
        closeButton = Button(text = "Close", size_hint=(None, None), width=100, height=40)
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
  
        # Instantiate the modal popup and display
        popup = Popup(title ='Alert',
                      content = layout,
                      size_hint =(None, None), size =(400, 200))  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))

        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    LoginApp().run()