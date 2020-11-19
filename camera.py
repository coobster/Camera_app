from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.image import Image
from io import BytesIO
import socket
from _thread import start_new_thread

HOST = '10.0.0.224'
#HOST = '127.0.0.1'
PORT = 5455

	
class MyCamera(App):
	def build(self):
		layout = BoxLayout(orientation='vertical')

		self.cameraObject = Camera(play=True)
		self.cameraObject.resolution = (500,500)

		self.cameraClick = Button(text='Take Photo')
		self.cameraClick.size_hint = (.5,.2)
		self.cameraClick.pos_hint = {'x':.25,'y':.75}
		self.cameraClick.bind(on_press=self.onCameraClick)
		layout.add_widget(self.cameraObject)
		layout.add_widget(self.cameraClick)
		return layout
	def onCameraClick(self,*args):
		texture = self.cameraObject.export_as_image()
		b_io = BytesIO()
		texture.save(b_io,fmt='png')
		#im = Image(texture,fmt='png')
		start_new_thread(sendImage,(b_io.getvalue(),))

def sendImage(tmp):
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as soc:
		soc.connect((HOST,PORT))
		soc.send(tmp)

if __name__ == '__main__':
	app = MyCamera()
	app.run()
