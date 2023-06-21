from rest_framework.authtoken import views

from rest_framework.renderers import BrowsableAPIRenderer


class CustomAuthToken(views.ObtainAuthToken):
    renderer_classes = (*views.ObtainAuthToken.renderer_classes, BrowsableAPIRenderer)
