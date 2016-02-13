from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
import base64

def index(request):
	context = dict()
	return render(request, "index.html", context)

def email(request):
	name = request.POST['name']
	recipientEmail = request.POST['recipientEmail']
	base64Image = request.POST['canvasBase64']
	saveImageToFile(base64Image)
	email = EmailMessage('Picto Message from %s' % name, '', 
			'shouvik.mani@gmail.com', [recipientEmail], [], [], headers={})
	email.attach_file('picto_message.png')
	email.send()
	return redirect('/')

def saveImageToFile(base64Image):
	#Parses base64 data out of base64Image
	base64String = base64Image.replace('data:image/png;base64,', '')
	image = base64.b64decode(base64String)
	with open('picto_message.png', 'wb') as f:
		f.write(image)
