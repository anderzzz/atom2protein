'''Django forms that define content of webpages from which user input is
obtained.

'''
from django import forms
from django.utils.translation import ugettext_lazy as _
from server.presenter_webapp.models import RetrieverStructure

class SearchStructureForm(forms.ModelForm):
    '''Class that defines the form for searching for a structure.

    Notes
    -----
    The items of the form are taken from a Django model, but only the items
    related to the search query are kept in the ``Meta`` subclass.

    '''
    class Meta:
        '''Define fields of the form. A subset from a Django model

        '''
        model = RetrieverStructure
        fields = ('pubmedid', 'description', 
                  'resolution_min', 'resolution_max', 'title', 
                  'depositdate_min', 'depositdate_max',
                  'molweight_min', 'molweight_max')
        labels = {'pubmedid' : _('Pubmed IDs of structure'),
                  'description' : _('Text in structure description'),
                  'resolution_min' : _('Minimum X-ray resolution'),
                  'resolution_max' : _('Maximum X-ray resolution'),
                  'title' : _('Text in structure title'),
                  'depositdate_min' : _('Earliest deposit date'),
                  'depositdate_max' : _('Latest deposit date'),
                  'molweight_min' : _('Minimum molecular weight'),
                  'molweight_max' : _('maximum molecular weight')}
        help_texts = {'depositdate_min' : _('Format YYYY-MM-DD'),
                      'depositdate_max' : _('Format YYYY-MM-DD'),
                      'description' : _('Comma-separated terms'),
                      'title' : _('Comma-separated terms')}

class SummaryPropertyForm(forms.ModelForm):
    '''Class that defines the form for how to summarize a set of structures.

    Notes
    -----
    The items of the form are taken from a Django model, but only the items
    related to the summarization are kept in the ``Meta`` subclass.

    '''
    class Meta:
        '''Define fields of the form. A subset from a Django model

        '''
        model = RetrieverStructure
        fields = ('nresidues', 'rresidues_polarity', 'bb_torsions')

class PresentationVizForm(forms.ModelForm):
 
    class Meta:
        model = RetrieverStructure
        fields = ('collective_viz', )
