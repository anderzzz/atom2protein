'''The summarizer contains the classes and methods to obtain numerical
properties to a given data container. The set of properties to obtain is
defined dynamically as methods of the classes are called. The summarizer is
expected to be initialized by the user, directly in code, or indirectly through
calling code. The actual numerical evaluations are done in other classes 
instantiated as part of the summarizer initialization.

'''
from informatics.datacontainers import Structure
from informatics.calculators import StructureCalculator

import inspect
import pandas as pd
from collections import namedtuple

class ConsistencyError(Exception):
    '''In case set of properties does not match the hard-coded associations
    with calculator functions. Should only be raised in case implementation of
    class is wrong, not by any user error.

    '''
    pass

Entry = namedtuple('Entry', 'brief, value, verbose')
'''namedtuple: Any property value is stored in a named tuple, which in addition
to storing the numeric data also dresses it with data semantics, both in a
brief and verbose form.

'''

class StructureSummarizer:
    '''Defining what properties of a structure to summarize, and their value.
    
    Class to define which properties of a structure to obtain and their
    associated semantics. The class also encodes methods to perform operations
    on groups of class instances, which enables a class instance to be
    associated with collective properties of a set of structures. This is one
    of the key classes that a user, or a calling program, is expected to
    initialize.

    Parameters
    ----------
    label, string
        Label to associate with the summary. For a single structure, the
        structure label is recommended.
    nresidues, namedtuple, optional
        Number of residues in the summarized object.
    nresidues_polarity, namedtuple, optional
        Number of residues of a certain polarity class in the summarized
        object.
    rresidues_polarity, namedtuple, optional
        Percentage of residues of a certain polarity class in the summarized
        object.
    bfactor_chain_stat, namedtuple, optional
        B-factor statistics per chain in the summarized object.
    bb_torsions, namedtuple, optional
        Backbone torsion angles for all chains in the summarized object.
    kwargs_to_calc, dict, optional
        Dictionary of named arguments to be passed to the calculator class,
        which does all the numeric evaluations of the properties.

    Raises
    ------
    ConsistencyError
        In case the set of properties defined in the initialization arguments
        are not identical to the set of properties in the association
        dictionary between property and calculation method. This should only be
        raised if the class has been incorrectly implemented, never due to user
        input error.

    Notes
    -----
    The initialization dynamically generates methods that once called with a
    particular data container instance evaluates the property, dress it with
    the relevant data semantics, and store it in a class attribute. The methods
    are named based on the name of the input parameters, defined above. For
    example, if the number of residues to a structure should be evaluated, the
    code should include

    ``summarizer.populate_nresidues(structure)``

    where ``summarizer`` is an instance of the current class and ``structure``
    is an instance of a Structure class, typically obtained as output from a
    parser.

    If this class is to be expanded, the set of input arguments must be
    expanded, along with the ``SUMMARY_KEY`` dictionary. All other associations
    and methods are dynamically created.

    '''
    SUMMARY_KEY = {'nresidues' : {'func' : 'cmp_nresidues', 
        'brief' : 'number of residues',
        'verbose' : 'Total number of residues per chain, including ' + \
                     'residues comprised of heteroatoms, such as water.'},

                   'bb_torsions' : {'func' : 'cmp_bb_torsions',
        'brief' : 'backbone torsion angles',
        'verbose' : ''},

                   'nresidues_polarity' : {'func' : 'cmp_nresidues_polarity',
        'brief' : 'number of residues in polarity classes',
        'verbose' : ''},

                   'bfactor_chain_stat' : {'func' : 'cmp_bfactor_chain_stat',
        'brief' : 'B-factor chain statistics',
        'verbose' : ''},

                   'rresidues_polarity' : {'func' : 'cmp_rresidues_polarity',
        'brief' : 'percentage of residues in polarity classes',
        'verbose' : ''}
        }
    '''dict: Dictionary that defines how to associate a property name with a
    property calculator function, and property semantics, both brief and
    verbose. This dictionary, and only this dictionary, encodes all relations
    between a summary property and the calculator machinery.

    '''
    def items(self):
        '''Iterator over live properties, their name and value.

        Yields
        ------
        key_value, tuple
            Tuple with two elements, the name of the property and its value,
            where the latter is described as a named tuple.

        '''
        for x in self:
            yield (x, self[x])

    def groupby(self, index_reduce, agg_func, entry_subset=None):
        '''Bla bla

        '''
        if entry_subset is None:
            entry_subset = list(self.__iter__())

        new_summary = StructureSummarizer(self.label)

        for entry_type in self:

            if entry_type in entry_subset:
                serie = self[entry_type].value
                levels = [x for x in serie.index.names if not x in index_reduce]
                group_by_pd = serie.groupby(level=levels, axis=0)
                serie_agg = group_by_pd.agg(agg_func)

                entry_brief = self[entry_type].brief + ' with grouping and aggregation'
                entry_verbose = self[entry_type].verbose + ' with grouping on ' + \
                '%s and aggregation by %s' %(str(levels), str(agg_func))
                new_entry = Entry('grouped on', serie_agg, entry_verbose)

            else:
                new_entry = self[entry_type]

            new_summary[entry_type] = new_entry

        return new_summary

    def _make_populate_func(self, name, cmp_func, brief, verbose):
        '''Generator function to produce the methods that calls the functions
        to numerically evaluate the property and to subsequently dress the data
        with data semantics. The function is called dynamically to translate
        property definitions into methods. 

        Parameters
        ----------
        name, string
            Name of property to construct a populate-function for.
        cmp_func, function
            Function object that is used to numerically evaluate the property.
        brief, string
            Short string of text that describes the property. This can be used
            in subsequent presentation to end-users.
        verbose, string
            Long string of text that described the property. This can be used
            in subsequent presentation to end-users. 

        Returns
        -------
        populate_x, function
            Function that accepts a structure object to evaluate the specified
            property.

        Notes
        -----
        The function is added to better satisfy the DRY principle. The list of
        properties are defined explicitly in the class initialization, and
        their associations to calculator functions and data semantics in a
        hard-coded dictionary. The population functions are derived, rather
        than explicitly coded.

        '''
        def _populate_x(structure):
            value = self._add_id_to(cmp_func(structure))
            self[name] = Entry(brief, value, verbose)

        return _populate_x

    def _add_id_to(self, df):
        '''Extends the Pandas Series with another column with the summary
        label. The calculator, that produces the raw data in the Pandas Series,
        is not concerned with the summary label, hence it is added after raw
        data is returned.

        '''
        names = ['id'] + df.index.names
        extended_index = [(self.label, ) + ind for ind in df.index]
        df.index = pd.MultiIndex.from_tuples(extended_index, names=names)

        return df

    def __add__(self, other):
        '''Append two summary objects.

        Defines the union (addition) of two summary objects and returns a new summed
        object, also of the summary object type. The addition matches
        properties in the two objects, and appends the content, in case
        identical properties exists in the two objects. In case there are
        properties present in one, but not the other, the sum contains
        identical data for these properties as either of the two objects.

        '''
        # Initialize the sum Summarizer
        new_summary = StructureSummarizer(self.label + '+' + other.label)

        # Loop over the union of Entry types and perform the Pandas algebra
        a_entries = set(self.__iter__())
        b_entries = set(other.__iter__())
        all_entry_types = a_entries | b_entries
        for entry_type in all_entry_types:
            if (entry_type in a_entries) and (entry_type in b_entries):
                a_entry = self[entry_type]
                b_entry = other[entry_type]
                value = a_entry.value.append(b_entry.value)
                entry_brief = a_entry.brief 
                entry_verbose = a_entry.verbose 
            elif entry_type in a_entries:
                a_entry = self[entry_type]
                value = a_entry.value
                entry_brief = a_entry.brief 
                entry_verbose = a_entry.verbose 
            elif entry_type in b_entries:
                b_entry = other[entry_type]
                value = b_entry.value
                entry_brief = b_entry.brief 
                entry_verbose = b_entry.verbose 

            new_entry = Entry(entry_brief, value, entry_verbose)
            new_summary[entry_type] = new_entry
            
        return new_summary

    def __getitem__(self, key):
        '''Return the value associated with a property key.

        Parameters
        ----------
        key, string
            Property name

        Returns
        -------
        entry, namedtuple
            The named tuple with property data and associated semantics

        Raises
        ------
        KeyError
            If the property key is either undefined or without associated
            value.

        '''
        try:
            ret = self.entry_collector[key] 
        except KeyError:
            raise KeyError('An entry for  %s not found in Summary' %(key))

        if ret is None:
            raise KeyError('A live entry of name %s not found in Summary' %(key))

        return ret

    def __setitem__(self, key, value):
        '''Set a property attribute.

        Parameters
        ----------
        key, string
            Property to set
        value, namedtuple
            Value and data semantics to set property attribute to.

        Raises
        ------
        TypeError
            If the value is not of the correct type

        '''
        if not isinstance(value, Entry):
            raise TypeError('The value a summarizer is set to must be an ' + \
                            'instance of the named tuple Entry')

        self.entry_collector[key] = value 

    def __iter__(self):
        '''Iterate over all populated summarized data. 
        
        Any items that have been left undefined, that is their associated 
        attribute equals ``None``, are not included.

        Yields
        ------
        entry, namedtuple
            Named tuple with value of property and associated data semantics.

        '''
        live_entries = []
        for member, value in self.entry_collector.items():
            if isinstance(value, Entry):
                live_entries.append(member)
        
        return iter(live_entries)

    def __init__(self, label, nresidues=None, nresidues_polarity=None,
                 rresidues_polarity=None, bfactor_chain_stat=None,
                 bb_torsions=None, kwargs_to_calc={}):

        self.label = label 
        self.calculator = StructureCalculator(**kwargs_to_calc)

        # Obtain the property input arguments and their name. They define the
        # properties to store values for and associate calculator methods with.
        frame = inspect.currentframe()
        args_to_init = inspect.getargvalues(frame).args
        vals_to_init = inspect.getargvalues(frame).locals
        prop_args = [v for v in args_to_init if not v in ['self', 'label',
                                                          'kwargs_to_calc']]

        self.entry_collector = dict([(key, value) for key, value in
                                                      vals_to_init.items() 
                                                  if key in prop_args]) 

        # Verify that no properties are defined without calculator method, or
        # vice versa.
        test_set1 = set(self.entry_collector) - set(self.SUMMARY_KEY.keys())
        test_set2 = set(self.SUMMARY_KEY.keys()) - set(self.entry_collector)
        if not test_set1 == set([]):
            raise ConsistencyError('More summary properties defined than ' + \
                                   'associated with calculator method. ' + \
                                   'Excess properties are: ' + ','.join(test_set1))
        if not test_set2 == set([]):
            raise ConsistencyError('Fewer summary properties defined than ' + \
                                   'associations with calculator methods. ' + \
                                   'Missing properties are: ' + ','.join(test_set2))

        # Dynamically create population methods for each property.
        for prop, prop_cmp in self.SUMMARY_KEY.items():
            brief = prop_cmp['brief']
            verbose = prop_cmp['verbose']
            cmp_func = getattr(self.calculator, prop_cmp['func'])
            pop_func = self._make_populate_func(prop, cmp_func, brief, verbose)
            setattr(self, 'populate_' + prop, pop_func)


def create_summarizer_for(container, kwargs_to_sum={}):
    '''Factory method to produce the appropriate summarizer class for a given
    data container.

    Parameters
    ----------
    container, object
        The data container object to produce a summarizer class for. 
    kwargs_to_sum, dict, optional
        Dictionary of arguments to pass to the summarizer class initialization.

    Returns
    -------
    sum_obj, object
        Instance of class to summarize the given data container.

    Raises
    ------
    NotImplementedError
        If a data container is given that does not have an associated class for
        summarization.

    '''
    if isinstance(container, Structure):
        ret = StructureSummarizer(container.label, **kwargs_to_sum)
    else:
        raise NotImplementedError("Data container without summarizer class given")

    return ret
