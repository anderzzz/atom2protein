'''Bla bla

'''
from informatics.visualizers import Visualizer
from informatics.summaries import StructureSummarizer
from informatics.ensemble_makers import EnsembleMaker
from informatics._version import __version__

import inspect
import sqlite3
import datetime
import random
import string

class HowToViz:
    '''Class that defines how to associate type of data with type of
    visualization. This removes the concern of the data semantics from the
    visualizer, which thus handles the data as numbers of given shapes and
    operations applied to it. 
    
    Default associations are encoded if a named default category is given
    during initialization. Additional associations can be dynamically added.

    '''
    def add(self, data_entry_type, viz_method_name, kwargs_dict):
        '''Method to dynamically add an association of data entry type and
        visualization method and its associated arguments. Note that each data
        entry type can be associated with multiple visualization methods.
        Hence, associations are not overwritten.

        Args:
            data_entry_type (string): Name of data entry type to associate with
                                      a visualization method.
            viz_method_name (string): Name of visualization method.
            kwargs_dict (dict): Dictionary that associates values with
                                arguments of given visualization method.

        Returns: None

        Raises:
            KeyError: If a non-existant visualization method is requested.
                      Note that data entry types are dynamic and a similar
                      check can only be done for this argument once the
                      visualization is executed.

        '''
        if not viz_method_name in self._available_viz_methods:
            raise KeyError('The Visualizer class does not contain a method ' + \
                           'called %s' %(viz_method_name))

        list_of_viz = self._container.setdefault(data_entry_type, []) 
        list_of_viz.append((viz_method_name, kwargs_dict))
        self._container[data_entry_type] = list_of_viz

    def __getitem__(self, key):
        '''Return association between the given data entry type and a
        visualization method.

        Args:
            key (string): Name of data entry type.

        Returns:
            viz_association (list): List of 2-member tuples, which encode an
                                    associated visualization, where first
                                    element of tuple is name of visualization
                                    method, and second element of tuple the
                                    kwargs.

        '''
        try:
            ret = self._container[key]
        except KeyError:
            raise KeyError('No visualization associated with property %s' %(key))

        return ret

    def __init__(self, default=None):
        '''Initialize class that handles the concern of which visualization
        method or methods to employ for a given data entry type. 

        Args:
            default (string, optional): If given, the string denotes a
                                        particular default of associations to
                                        use. Observe that additional
                                        associations can be dynamically added
                                        after a default has been given. The
                                        available defaults are:
                                        * 'single structure': suitable where
                                        data from one structure is to be
                                        presented.
                                        * 'summary structure': suitable where
                                        data from a plurality of structures is
                                        to be presented.

        Raises:
            KeyError: In case invalid default name given.

        '''
        self._container = {}
        self._available_viz_methods = set([name for name, method in
                                     inspect.getmembers(Visualizer,
                                     predicate=inspect.isfunction)])

        if default == 'single structure':
            self.add('bb_torsions', 'scatter_plot', 
                     {'x_axis' : 'phi', 'y_axis' : 'psi',
                      'level_name' : 'property',
                      'y_range' : (-180.0, 180.0),
                      'x_range' : (-180.0, 180.0),
                      'alpha' : 0.5})
            self.add('nresidues', 'stacked_bars',
                     {'x_axis' : 'chain', 'y_axis' : 'residue count',
                      'stack' : 'property'})
            self.add('nresidues_polarity', 'stacked_bars',
                     {'x_axis' : 'chain', 'y_axis' : 'residue count',
                      'stack' : 'property'})
            self.add('rresidues_polarity', 'stacked_bars',
                     {'x_axis' : 'chain', 'y_axis' : 'residue count',
                      'stack' : 'property'})

        elif default == 'summary structure':
            self.add('bb_torsions', 'scatter_plot',
                     {'x_axis' : 'phi', 'y_axis' : 'psi',
                      'level_name' : 'property',
                      'y_range' : (-180.0, 180.0),
                      'x_range' : (-180.0, 180.0),
                      'alpha' : 0.5})
            self.add('rresidues_polarity', 'spider_plot',
                     {'dims' : 'property', 'common_range' : (0.0, 1.0)})

        elif default == 'single pubmed':
            pass
        elif default == 'summary pubmed':
            pass
        elif default is None:
            pass
        else:
            raise KeyError("Undefined default given: %s" %(default))
        
class Presenter:
    '''Bla bla

    '''
    def _randomword(self, length):
        '''Bla bla

        '''
        return ''.join(random.choice(string.ascii_lowercase +
                                     string.digits) for i in range(length))

    def produce_visualization(self, output_format='html', name_length=15):
        '''Produce visualization files and database entry for the specified
        visualization method and data.

        Args: 
            output_format (string, optional): Which format to output visualization 
                                    files in. Must match what is available in the
                                    Visualizer class.
            name_length (int, optional): How long the namespace should be of
                                         visualization files. The longer the
                                         lower probability of identical
                                         namespace for distinct visualizations.

        Returns: None

        '''
        # Loop over all specified data entry types
        for entry_type in self.type_subset:
            entry = self.summary_object[entry_type]

            # Initialize the Visualizer
            viz = Visualizer(write_output_format=output_format)

            # Loop over all visualization methods associated with current data
            # entry type.
            for viz_method, viz_kwargs in self.howtoviz[entry_type]:

                # Execute the visualization
                getattr(viz, viz_method)(entry.value, **viz_kwargs)

                # Generate file of visualization and insert entry into database
                namespace = self._randomword(name_length)
                viz.write_output(self.file_path, namespace)

                data = (self.summary_object.label, entry_type, viz_method,
                        '', entry.verbose, viz.get_descr(viz_method),
                        self.file_path, namespace)
                self.db_entry(data, 'Presenter.produce_visualization',
                                    self.search_id)

    def _validate_subset(self, summary_obj, id_subset, type_subset):
        '''Validate that any specifically enumerated summary IDs or entry types
        are present in the summary object. If not an exception is raised. If
        validation successful, return the sets of summary IDs and entry types
        defined by the subset selection. Note that if the specific selections
        are set to None, the entire range of summary IDs and entry types are
        returned.

        Args:
            summary_obj: The summary object to be presented. The object can be
                         a single Summary object, or an iterable of Summary
                         objects.
            id_subset (list or set): List or set of strings of the summary IDs
                                     to present. If None, all available
                                     summaries will be presented.
            type_subset (list or set): List or set of strings of the entry
                                       types to present. If None, all available
                                       entry types will be presented.

        Returns:
            ret_1 (set): Set of validated summary IDs implied by the input.
            ret_2 (set): Set of validated entry types implied by the input.

        Raises:
            KeyError: At least one of the given subsets of IDs or types is
                      missing from the given Summary object.
       
        '''
        ids = set([])
        types = set([])
        if isinstance(summary_obj, (list, set, tuple)):
            for s in summary_obj:
                ids.add(s.label)
                types = types.union(set(s.__iter__()))
        else:
            ids.add(summary_obj.label)
            types = types.union(set(summary_obj.__iter__()))

        if id_subset is None:
            ret_1 = ids
        else:
            ret_1 = set(id_subset)
        if type_subset is None:
            ret_2 = types
        else:
            ret_2 = set(type_subset)

        if not ret_1.issubset(ids):
            raise KeyError("Summary ID subset not subset of IDs of given summary")
        if not ret_2.issubset(types):
            raise KeyError("Summary data types subset not subset of data types of given summary")
            
        return ret_1, ret_2

    def __init__(self, summary_object, db_handler,
                 howtoviz=None, ensemble_operation='join',
                 id_subset=None, data_type_subset=None,
                 search_id=None):
        '''Bla bla

        '''
        self.file_path = db_handler.static_file_path
        self.howtoviz = howtoviz 
        self.id_subset, self.type_subset = self._validate_subset(summary_object, 
                                                     id_subset, data_type_subset)

        if isinstance(summary_object, (list, set, tuple)):
            self.ensemble_summary = True
            self.ensemble_maker = EnsembleMaker(ensemble_operation,
                                                self.id_subset)
            if self.howtoviz is None:
                if all(isinstance(s, StructureSummarizer) for s in summary_object):
                    self.howtoviz = HowToViz(default='summary structure')
                #elif all(isinstance(s, PubMedSummarizer) for s in summary_object):
                #    self.howtoviz = HowToViz(default='summary pubmed')
                else:
                    raise TypeError("Summary contains objects without a presenter class")
        else:
            self.ensemble_summary = False
            self.ensemble_maker = EnsembleMaker('unity', None)
            if self.howtoviz is None:
                if isinstance(summary_object, StructureSummarizer):
                    self.howtoviz = HowToViz(default='single structure')
                #elif isinstance(summary_object, PubMedSummarizer):
                #    self.howtoviz = HowToViz(default='single pubmed')
                else:
                    raise TypeError("Summary is of type without a presenter class")

        self.summary_object = self.ensemble_maker(summary_object)

        self.db_entry = db_handler.make_db_entry
        self.search_id = search_id

