'''Model definitions, which corresponds to how the data is structured and
defined, as it is exposed to the API.

'''
from django.db import models
from django.core import validators

class PresenterDataViz(models.Model):
    '''Django model for the data visualization

    '''
    WHO_ENTERED = (
        ('H1', 'Human One'),
        ('H2', 'Human Second'),
        ('S1', 'Presenter.produce_visualization'))

    created_by = models.CharField(max_length=200, blank=True, default='',
                                  choices=WHO_ENTERED)
    created_by_version = models.CharField(max_length=200, blank=False)
    created_by_version.validators = [validators.int_list_validator(sep='.')]
    created_time = models.DateTimeField(auto_now_add=True)
    id_label = models.CharField(max_length=200, blank=False)
    entry_data_type = models.CharField(max_length=200, blank=False)
    viz_method = models.CharField(max_length=200, blank=False)
    id_text = models.CharField(max_length=200, blank=False)
    entry_data_text = models.CharField(max_length=200, blank=False)
    viz_text = models.CharField(max_length=200, blank=False)
    file_path = models.CharField(max_length=500, blank=False, default='')
    file_namespace = models.CharField(max_length=20, blank=False, default='')

    class Meta:
        '''Meta class to define attribute to order'''
        ordering = ('created_time',)

class RetrieverStructure(models.Model):
    '''Bla bla

    '''
    pubmedid = models.CharField(max_length=501, blank=True, default='')
    pubmedid.validators = [validators.int_list_validator(sep=',')]
    description = models.CharField(max_length=500, blank=True, default='')
    resolution_min = models.FloatField(blank=True, null=True)
    resolution_max = models.FloatField(blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, default='')
    depositdate_min = models.CharField(max_length=10, blank=True, default='')
    depositdate_max = models.CharField(max_length=10, blank=True, default='')
    molweight_min = models.FloatField(blank=True, null=True)
    molweight_max = models.FloatField(blank=True, null=True)

