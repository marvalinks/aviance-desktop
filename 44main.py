from kivy.app import App
from kivy.core import text
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.core.window import Window




Window.clearcolor = (1,1,1,1)
Window.size = (1720, 1080)

class MainApp(App):
    def build(self):
        layout = GridLayout(cols=1, row_force_default=True, row_default_height=40, spacing=10, padding=80)
        logo = Image(source='./images/aviance.png')
        self.email = TextInput(text="Enter email here", size_hint=(None, None), width=500, height=40)
        self.password = TextInput(text="Enter password here", size_hint=(None, None), width=500, height=40)
        submit = Button(text='Login', size_hint=(None, None), width=100, height=40)

        layout.add_widget(logo)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(submit)

        return layout
    
    def onSubmitPress(self, obj):
        pass


if __name__ == '__main__':
    MainApp().run()


    # Button:
    #             text: "Disconnect"
    #             font_size: 24
    #             on_press: root.disconnect()