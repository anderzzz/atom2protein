from django import forms
from .models import RetrieverStructure

class RetrieverForm(forms.ModelForm):

    class Meta:
        model = RetrieverStructure
        fields = ('pubmedid', 'description', 'resolution_min',
        'resolution_max', 'title', 'depositdate_min', 'depositdate_max',
        'molweight_min', 'molweight_max')

class RetrieverForm2(forms.ModelForm):
 
    class Meta:
        model = RetrieverStructure
        fields = ('nresidues', 'rresidues_polarity', 'bb_torsions')

class RetrieverForm3(forms.ModelForm):
 
    class Meta:
        model = RetrieverStructure
        fields = ('collective_viz', )
