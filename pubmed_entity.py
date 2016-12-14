'''Bla bla

'''
import json

class PubMedEntry:
    '''Bla bla

    '''
    def _parse_json(self, json_rawdata):
        '''Bla bla

        '''
        raw_decode = json.loads(json_rawdata)
        print (raw_decode)

    def __init__(self, json_rawdata):
        '''Bla bla

        '''

        self._parse_json(json_rawdata) 
