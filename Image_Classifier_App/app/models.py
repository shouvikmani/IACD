from django.db import models

def getImagePath(instance, filename):
		return 'images/%s' % (filename)

class Picture(models.Model):
	picture = models.ImageField(upload_to=getImagePath)

class Classifier(models.Model):
	name = models.CharField(max_length=200)
	class0 = models.CharField(max_length=200)
	class1 = models.CharField(max_length=200)
	algorithm = models.CharField(max_length=200)
	description = models.CharField(max_length=200)