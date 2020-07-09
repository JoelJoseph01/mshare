from .models import *
from django.forms import ModelForm


class ShareForm(ModelForm):
    class Meta:
        model=Share
        fields = ['title','content']

class Searching(ModelForm):
    class Meta:
        model = Share
        fields = ['title']