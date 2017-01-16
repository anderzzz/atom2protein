from rest_framework import serializers
from server.presenter_webapp.models import PresenterDataViz, RetrieverStructure

class PresenterDataVizSerializer(serializers.ModelSerializer):
    '''Serializer to translate between data in database and the format sent
    over the HTTP request

    '''
    class Meta:
        model = PresenterDataViz
        fields = ('id', 'created_by', 'created_by_version', 'created_time',
                  'id_label', 'entry_data_type', 'viz_method', 'id_text',
                  'entry_data_text', 'viz_text', 'file_path', 'file_namespace')

class RetrieverStructureSerializer(serializers.ModelSerializer):
    '''Bla bla

    '''
    class Meta:
        model = RetrieverStructure
        fields = '__all__'
