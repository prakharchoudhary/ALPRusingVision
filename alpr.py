import io
import os
import re
from google.cloud import vision
from google.cloud.vision import types

class GoogleVision:

	def __init__(self, camera_port=0):
		# Instantiates a client
		self.client = vision.ImageAnnotatorClient()
		self.numplate = None
		self.CAMERA_PORT = camera_port

	def getResponse(self, img):
		'''
		Request the vision api for a given image or frame(when using webcam)
		'''
		if img is not None:
			with io.open(img, 'rb') as image_file:
				content = image_file.read()

		image = types.Image(content=content)

		# Performs label detection on the image file
		self.response = self.client.text_detection(image=image)
		self.text = [i.description for i in self.response.text_annotations]

	def readLicenseNumber(self):
		'''
		Finds out the number plate among all the detected text text_annotations
		'''

		# Indian Number plate regex pattern
		licenseNum = re.compile(r'[A-Z]{2,3}[\s\.-]?[0-9]{2}[\s\.-]?[A-Z]{2,3}[\s\.-]?[a-zA-Z0-9]{4}')
		# print(self.text)
		for word in self.text:
			if self.numplate is None:
				self.numplate = licenseNum.match(word)
				if self.numplate:
					self.numplate = self.numplate.group(0)
					self.numplate = ''.join(self.numplate.split(' '))
					self.numplate = ''.join(self.numplate.split('.'))
					break
		if self.numplate is None:
			print("No number plate found!")

	def call(self, img=None, webcam=False):
		'''
		if an input is image then simple call _getResponse on it and read the
		license number; however; if the the input is a live video stream from webcam
		then use frames until number plate is detected.
		'''
		if img and webcam:
			print("Both image and webcam input can't be True")
			return

		if img:
			self.getResponse(img)
			self.readLicenseNumber()
			return(self.numplate)
		else:
			print("No image!")
			return None	

if __name__ == '__main__':
	gv = GoogleVision()
	img_path = "./images/toyCar.jpg"
	# img_path = "./testData/3.jpg"	
	print(gv.call(img_path))