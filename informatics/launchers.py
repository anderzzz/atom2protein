'''Bla bla

'''
from informatics.rawretrievers import PDBData
from informatics.parsers import Parser
from informatics.summaries import create_summarizer_for
from informatics.presenter import Presenter
from informatics.database import DBHandler

from collections import namedtuple
import json
import os

class Launcher:
    '''Bla bla

    '''
    EXPECTED_KEYS = set(['rawdata_type', 'search_instructions',
                         'summary_instructions',
                         'presentation_instructions'])

    def launch(self):
        '''Bla bla

        '''
        self._launch_search()
        collection = self._launch_summarize()
        self._launch_present(collection)

    def _launch_search(self):
        '''Bla bla

        '''
        for search_method, kwargs in self.rawretriever_methods:
            func = getattr(self.rawretriever, search_method)
            func(**kwargs)
        self.rawretriever.search()

    def _launch_summarize(self):
        '''Bla bla

        '''
        summary_collection = []
        parser = Parser(self.rawretriever)
        for data in self.rawretriever:
            container = parser(data)
            summarizer = create_summarizer_for(container) 
            for summary_method in self.summarize_stream:
                func = getattr(summarizer, summary_method)
                func(container)
            summary_collection.append(summarizer)

        return summary_collection

    def _launch_present(self, collection):
        '''Bla bla

        '''
        if self.collective_presentation:
            presenter = Presenter(collection, self.db_handler,
                                  search_id=self.id_of_search)
            presenter.produce_visualization(output_format='javascript')

        else:
            for summa in collection:
                presenter = Presenter(summa, self.db_handler,
                                      search_id=self.id_of_search)
                presenter.produce_visualization(output_format='javascript')

    def _validate_json(self, json_dict):
        '''Bla bla

        '''
        keys = set(json_dict.keys())
        test1 = keys - self.EXPECTED_KEYS
        test2 = self.EXPECTED_KEYS - keys

        if len(test1) > 0:
            raise LookupError('JSON contains more attributes that expected. ' + \
                              'Offending attributes: ' + ','.join(test1))
        if len(test2) > 0:
            raise LookupError('JSON is missing expected attributes. ' + \
                              'Missing attributes: ' + ','.join(test2))

        return True

    def __init__(self, method_chain):
        '''Bla bla

        '''
        path = os.getcwd() 
        self.db_handler = DBHandler('django', path + '/server/viz_out/', path + '/server/vizout.db') 

        inconf = json.loads(method_chain)
        self._validate_json(inconf)

        # Set the rawdata retriever class
        rawdata_value = inconf['rawdata_type']
        if rawdata_value == 'protein_structure':
            self.rawretriever = PDBData()
        else:
            raise NotImplementedError('Launcher for rawdata_type ' + \
                                      '%s not implemented' %(rawdata_value))

        # Parse search instructions
        search_input = inconf['search_instructions']

        search_terms = []
        for key, value in search_input.items():
            if value == '' or value is None:
                continue

            if key == 'title':
                vals = value.split(',')
                for v in vals:
                    to_add = ('set_search_title', {'val' : v})
                    search_terms.append(to_add)

            elif key == 'resolution_min':
                to_add = ('set_search_resolution' , {'res_min' : value,
                                                     'res_max' : '1e50'})
                search_terms.append(to_add)

            elif key == 'resolution_max':
                to_add = ('set_search_resolution' , {'res_min' : '0.0',
                                                     'res_max' : value})
                search_terms.append(to_add)

            elif key in ['id']:
                self.id_of_search = value

            else:
                raise LookupError('Undefined search value %s' %(key))
        self.rawretriever_methods = search_terms

        # Parse summarization instructions
        summarize_input = inconf['summary_instructions']

        summary_terms = []
        for key, value in summarize_input.items():

            if not isinstance(value, bool):
                raise TypeError('Not Boolean value for %s attribute' %(key))

            if key == 'nresidues':
                if value == True:
                    summary_terms.append('populate_nresidues')

            elif key == 'rresidues_polarity':
                if value == True:
                    summary_terms.append('populate_rresidues_polarity')

            elif key == 'bb_torsions':
                if value == True:
                    summary_terms.append('populate_bb_torsions')

            else:
                raise LookupError('Undefined summarization value %s' %(key))
        self.summarize_stream = summary_terms

        # Parse collective versus individual presentation
        presentation_input = inconf['presentation_instructions']

        for key, value in presentation_input.items():
            if key == 'collective_viz':
                if isinstance(value, bool):
                    self.collective_presentation = value 
                else:
                    raise TypeError('Not Boolean value for ' + \
                          'collective_viz attribute')

            else:
                raise LookupError('Undefined presentation value %s' %(key))

