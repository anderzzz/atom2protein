from django import forms
from .models import RetrieverStructure

class RetrieverForm(forms.ModelForm):

    class Meta:
        model = RetrieverStructure
        fields = '__all__'
