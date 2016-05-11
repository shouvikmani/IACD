from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^classifier/(?P<classifier_name>[a-zA-Z]+)/$', views.classifier, name='classifier'),
    url(r'^addClassifier/$', views.addClassifier, name='addClassifier'),
]
