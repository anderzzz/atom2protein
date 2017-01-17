'''Bla bla

'''
from proteininfo.rawretrievers import PDBData
from proteininfo.parsers import Parser
from proteininfo.summaries import create_summarizer_for
from proteininfo.presenter import Presenter
from proteininfo.database import DBHandler

from collections import namedtuple
import json
import os

class Launcher:
    '''Bla bla

    '''
    def launch(self):
        '''Bla bla

        '''
        for search_method, kwargs in self.rawretriever_methods:
            func = getattr(self.rawretriever, search_method)
            func(**kwargs)
        self.rawretriever.search()

        summary_collection = []
        parser = Parser(self.rawretriever)
        for data in self.rawretriever:
            container = parser(data)
            summarizer = create_summarizer_for(container) 
            for summary_method in self.summarize_stream:
                func = getattr(summarizer, summary_method)
                func(container)
            summary_collection.append(summarizer)
            presenter = Presenter(summarizer, self.db_handler,
                                  search_id=self.id_of_search)
            presenter.produce_visualization(output_format='javascript')

    def __init__(self, method_chain):
        '''Bla bla

        '''
        inconf = json.loads(method_chain)

        search_terms = []
        for key, value in inconf.items():
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
                #TODO Ensure this value is associated with the visualization db
                #entry
                self.id_of_search = value

            else:
                raise AttributeError('Undefined search key %s' %(key))

        self.rawretriever_methods = search_terms
        self.rawretriever = PDBData()

        self.summarize_stream = ['populate_nresidues', 'populate_rresidues_polarity']

        path = os.getcwd() 
        self.db_handler = DBHandler('django', path + '/server/viz_out/', path + '/server/vizout.db') 
