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
	#saveImage(base64Image)
	email = EmailMessage('Picto Message from %s' % name, '', 
			'shouvik.mani@gmail.com', [recipientEmail], [], [], headers={})
	email.send()
	return redirect('/')

def saveImage(base64Image):
	fh = open("picto_message.jpg", "wb")
	fh.write(base64Image.decode('base64'))
	fh.close()