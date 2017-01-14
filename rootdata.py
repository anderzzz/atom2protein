'''The raw data to analyze can be retrieved via open Web APIs. The classes in
this module contain the logic to do so for a set number of third-party Web REST APIs. The
intent of these classes is to remove the need for the user to know the details
of each API and in what format requests and responses are defined. Instead each
class contains a number of methods to define search criteria with a clear
semantic. 

Each class is designed such that upon calling the `search` method the class
instance is populated with the raw data returned by the Web API. Each element
of raw data is retrieved in no particular order by iterating over the
particular instance. Any further analysis is done by passing the raw data into
an instance of the `Parser` class.

'''
from urllib.request import urlopen
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

class DownloadError(Exception):
    pass

class WebService:
    '''General purpose class for accessing data from and posting data to web
    servers, particularly through REST APIs. The class methods are not
    concerned with the nature of the data. Typically this class is used as a
    parent to other classes.

    '''
    def set_id(self, ids):
        '''Set ids of items to extract

        Args:
            ids (iterable): Iterable of strings of IDs

        Returns: None

        Raises:
            TypeError: If one or more elements of ids iterable is not a string

        '''
        if not all([isinstance(val, str) for val in ids]):
            raise TypeError('Not all ids are strings')
        else:
            self.item_ids = [val.lower() for val in ids]

    def get_id(self):
        '''Return ids of items set so far.

        Args: None

        Returns:
            ids (list): List of string identifiers

        '''
        return self.item_ids

    def get(self, http_string):
        '''Wrapper to execute the HTTP GET command and to check response and
        convert any output to a string.

        Args:
            http_string (string): The HTTP Request-URI

        Returns:
            content_str (string): The returned item following the request
                                  operation.

        Raises:
            DownloadError: In case the HTTP status suggests an error

        '''
        response = urlopen(http_string)
        if self._check_response(response):
            content_str = response.read().decode('utf-8')
        else:
            raise DownloadError('Failed GET of: %s' %(http_string))

        return content_str

    def post(self, http_string, data):
        '''Wrapper to execute the HTTP POST command and to check response and
        convery any uotput to a string.

        Args:
            http_string (string): The HTTP Request-URI
            data (string): The data to post

        Returns:
            content_str (string): The returned item following the request
                                  operation.

        Raises:
            DownloadError: In case the HTTP status suggests an error

        '''
        response = urlopen(http_string, data=data)
        if self._check_response(response):
            content_str = response.read().decode('utf-8')
        else:
            raise DownloadError('Failed POST of: %s' %(http_string))

        return content_str

    def save(self, id_name, data):
        '''Save string of data to disk with file naming as configured during
        initialization.

        Args:
            id_name (string): Unique data identifier to be used in file name
            data (string): Data to be saved to disk

        Returns: None

        '''
        name_out = self.out_prefix + id_name
        if len(self.out_suffix) > 0:
            if not id_name[-4:] == self.out_suffix:
                name_out += self.out_suffix

        with open(name_out, 'w') as f_out:
            f_out.write(data)

    def _check_response(self, resp):
        '''Tests the HTTP return status in a reponse

        Args:
            resp (dict): Dictionary returned by the httplib2 after a GET call
                         to a web server

        Returns:
            status200 (bool): True if return status is 200, False otherwise.

        '''
        if resp.status == 200:
            ret = True
        else:
            ret = False

        return ret 

    def __init__(self, out_prefix='', out_suffix=''):
        '''Bla bla

        '''
        self.item_ids = []
        self.out_prefix = out_prefix
        self.out_suffix = out_suffix

class PDBData(WebService):
    '''Class to query the PDB databank available at http://www.rcsb.org/pdb
    using advanced search queries. The class also retrieves the data associated
    with the queried structure identifiers, in other words, entire PDB files
    can be obtained. The XML format is preferred. 

    Helpful documentation on the PDB Databank REST API is found at
    http://www.rcsb.org/pdb/software/rest.do

    '''
    def set_search_pubmedid(self, idlist):
        '''Define pubmed identifiers to be associated with structures.

        Args:
            idlist (list): List of integer PubMed identifiers.

        Returns: None

        '''
        params = {}
        params['queryType'] = 'org.pdb.query.simple.PubmedIdQuery'
        params['description'] = 'PubMed Identifiers'
        params['pubMedIdList'] = ','.join([str(x) for x in idlist])
        self.xml_parameters.append(params)

    def set_search_description(self, val):
        '''Define string part of structure description in a search query.

        Args:
            val (string): Text to be part of structure description

        Returns: None

        '''
        params = {}
        params['queryType'] = 'org.pdb.query.simple.StructDescQuery'
        params['description'] = 'Structure Description'
        params['entity.pdbx_description.comparator'] = 'contains'
        params['entity.pdbx_description.value'] = val
        self.xml_parameters.append(params)

    def set_search_resolution(self, res_min, res_max):
        '''Define lower and upper bound of X-ray resolution in a search query.

        Args:
            res_min (float): Lower bound of resolution in units of AA
            res_max (float): Upper bound of resolution in units of AA

        Returns: None

        '''
        params = {}
        params['queryType'] = 'org.pdb.query.simple.ResolutionQuery'
        params['description'] = 'Resolution Query'
        params['refine.ls_d_res_high.comparator'] = 'between'
        params['refine.ls_d_res_high.min'] = str(res_min)
        params['refine.ls_d_res_high.max'] = str(res_max)
        self.xml_parameters.append(params)

    def set_search_title(self, val):
        '''Define string part of structure title in a search query.

        Args:
            val (string): Text to be part of structure title

        Returns: None

        '''
        params = {}
        params['queryType'] = 'org.pdb.query.simple.StructTitleQuery'
        params['description'] = 'Structure Title Query'
        params['struct.title.comparator'] = 'contains'
        params['struct.title.value'] = val
        self.xml_parameters.append(params)

    def set_search_depositdate(self, date_min, date_max):
        '''Define lower and upper bound for deposit date in a search query.

        Args:
            date_min (string): Earliest despoit date in format YYYY-MM-DD
            date_max (string): Latest deposit date in format YYYY-MM-DD

        Returns: None

        '''
        params = {}
        params['queryType'] = 'org.pdb.query.simple.DepositDateQuery'
        params['description'] = 'Structure Deposit Date Query'
        params['database_PDB_rev.date_original.comparator'] = 'between'
        params['database_PDB_rev.date_original.min'] = date_min
        params['database_PDB_rev.date_original.max'] = date_max
        params['database_PDB_rev.mod_type.value'] = '1'
        self.xml_parameters.append(params)

    def set_search_molweight(self, weight_min, weight_max):
        '''Define lower and upper bound for molecular weight in a search query.

        Args:
            weight_min (float): Lowest molecular weight
            weight_max (float): Highest molecular weight

        Returns: None

        '''
        params = {}
        params['queryType'] = 'org.pdb.query.simple.MolecularWeightQuery'
        params['description'] = 'Structure Molecular Weight Query'
        params['entity.formula_weight.min'] = str(weight_min)
        params['entity.formula_weight.max'] = str(weight_max)
        self.xml_parameters.append(params)

    def search(self):
        '''Function to execute a configured search and retrieve the PDB IDs of
        the structures that satisfies search query.

        Args: None

        Returns: None

        '''
        # Construct a nested XML string that denotes a many criteria advanced
        # search
        top = Element('orgPdbCompositeQuery')
        for level, params in enumerate(self.xml_parameters):
            child_query_refinement = SubElement(top, 'queryRefinement')
            child_query_level = SubElement(child_query_refinement, 'queryRefinementLevel')
            child_query_level.text = str(level)
            child_query_root = SubElement(child_query_refinement, 'orgPdbQuery')
            for title, value in params.items():
                child_p = SubElement(child_query_root, title)
                child_p.text = value

        # Post the XML string to the PDB server and retrieve data
        search_query = tostring(top)
        http_string = self.url_base + self.url_search
        content = self.post(http_string, search_query)
        ids = self._extract_pdb_id(content)
        self.set_id(ids)

    def _extract_pdb_id(self, data):
        '''Extract PDB IDs from the search output

        Args:
            data (string): String of data obtained from the PDB search.

        Returns:
            ids (list): List of strings of PDB IDs.

        '''
        return data.split('\n')[:-1]

    def __iter__(self):
        '''Iterator for the class object which returns at each iteration a
        string in memory of the protein structure data in the PDB file format

        Args: None

        Returns: 
            content_str (string): String of structure data formatted in the PDB
                                  file format.

        '''
        for item_name in self.item_ids:
            http_string = self.url_filebase + item_name + '.xml'
            content_str = self.get(http_string)

            if self.save_to_disk:
                self.save(item_name, content_str)

            yield content_str

    def __init__(self, save_to_disk=False, print_list_only=False):
        '''Initialize the class object that retrieves structure data given a
        search query

        Args: 
            save_to_disk (bool): Parameter that sets if structure data should be saved
                                 to disk in addition to being a string in
                                 memory.
            print_list_only (bool): Parameter that sets if any structure data should be
                                    read or only the set of PDB IDs reported.

        Returns: None

        '''
        # Initialize parent class
        super().__init__(out_prefix='protein_', out_suffix='.xml')

        # Parameters relevant to a query to define a set of PDB IDs
        self.url_base = 'http://www.rcsb.org/pdb/rest/'
        self.url_search = 'search'
        self.xml_parameters = []

        # Parameters relevant to retrieving the structure data
        self.url_filebase = 'https://files.rcsb.org/download/'
        self.save_to_disk = save_to_disk 
        self.print_list_only = print_list_only

class PubMedData(WebService):
    '''Class to query the PubMed database available at
    http://www.ncbi.nlm.nih.gov/pubmed/
    using advanced search queries. The class also retrieves the data associated
    with the queried publication identifiers in the JSON format.

    Helpful documentation on the PubMed REST API is found at
    http://www.ncbi.nlm.nih.gov/books/NBK25501/

    '''
    def set_search_journal(self, journal_name):
        '''Set the name of the journal for query.

        Args:
            journal_name (string): Name of journal. Whitespace allowed.

        Returns: None

        '''
        params = {}
        params['[Journal]'] = (self._plus_adjust(journal_name),)
        self.uri_parameters.append(params)

    def set_search_abstract(self, title_and_abstract):
        '''Set condition on text in title or abstract for query.

        Args:
            title_and_abstract (string): Text to be present in title or
                                         abstract. Whitespace allowed.

        Returns: None

        '''
        params = {}
        params['[Title/Abstract]'] = (self._plus_adjust(title_and_abstract),)
        self.uri_parameters.append(params)

    def set_search_publishdate(self, date_min, date_max):
        '''Set condition on publication date for query.

        Args:
            date_min (string): Earliest publication date, format YYYYMMDD
            date_max (string): Most recent publication date, format YYYYMMDD

        Returns: None

        '''
        params = {}
        date_tuple = ('/'.join([date_min[0:4], date_min[4:6], date_min[6:8]]),
                      '/'.join([date_max[0:4], date_max[4:6], date_max[6:8]]))
        params['[PDAT]'] = date_tuple
        self.uri_parameters.append(params)

    def set_retmax(self, retmax):
        '''Bla bla

        '''
        self.retmax = str(retmax)

    def search(self):
        '''Perform the query of the PubMed database as set above. The function
        constructs the parametes to the GET call and sets the list of PMIDs.

        Args: None

        Returns: None

        '''
        # Set required constant parameters
        uri_params_root = ['tool=' + self.tool, 
                           'email=' + self.email, 
                           'retmax=' + str(self.retmax),
                           'db=pubmed']

        ids = []
        for retstart in range(0, self.max_ids, self.retmax):
            uri_params = uri_params_root + ['retstart=' + str(retstart)]

            # Build the query term based on specifications
            query = []
            for term_part in self.uri_parameters:
                for key, values in term_part.items():
                    out = ':'.join(values)
                    out += key
                    query.append(out)
            term_parameters = '+AND+'.join(query)
            uri_params += ['term=' + term_parameters]

            # Construct HTTP string and get data
            search_params = '&'.join(uri_params)
            http_string = self.url_base + self.search_prefix + '?' + search_params
            content = self.get(http_string)
            ids_iteration = self._extract_pubmed_id(content)
            ids += ids_iteration

            # In case end of list reached before maximum allowed ids obtained,
            # break the loop
            if len(ids_iteration) < int(self.retmax):
                break

        self.set_id(ids)

    def _plus_adjust(self, string2adjust):
        '''Replace intermediate white space in search terms with '+' signs.

        Args:
            string2adjust (string): string that can contain whitespace

        Returns:
            plus_string (string): string that contains no whitespace and with
                                  intermediate whitespace replaced with '+'. 

        '''
        compact_string = string2adjust.strip()
        plus_string = compact_string.replace(' ','+')
        
        return plus_string

    def _extract_pubmed_id(self, xml_string):
        '''From the returned XML string of an advanced search of the PubMed,
        the PMIDs are retrieved.

        Args:
            xml_string (string): The XML string obtained from the PubMed query.

        Returns:
            ret_ids (list): List of strings of the PMIDs.

        '''
        root = etree.fromstring(xml_string)

        ret_ids = []
        for idlist in root.findall('IdList'):
            for id_entry in idlist.findall('Id'):
                ret_ids.append(id_entry.text)

        return ret_ids 

    def __iter__(self):
        '''Iterator for the class object which returns at each iteration a
        string in memory of the detailed pubmed output 

        Args: None

        Returns: 
            content_str (string): String of pubmed data.

        '''
        for item_id in self.item_ids:
            fetch_terms = ['tool=' + self.tool, 'email=' + self.email]
            fetch_terms += ['db=pubmed', 'retmode=xml', 'rettype=xml']
            fetch_terms += ['id=' + item_id]
            fetch_params = '&'.join(fetch_terms)
            http_string = self.url_base + self.fetch_prefix + '?' + fetch_params

            content_str = self.get(http_string)
            if self.save_to_disk:
                self.save(item_id, content_str)

            yield content_str

    def __init__(self, save_to_disk=False, print_list_only=False):
        '''Initialize the class object that retrieves pubmed data given a
        search query

        Args: 
            save_to_disk (bool): Parameter that sets if raw pubmed search 
                                 data should be saved to disk in addition to being 
                                 a string in memory.
            print_list_only (bool): Parameter that sets if any pubmed data should be
                                    read or only the set of pubmed IDs reported.

        Returns: None

        '''
        # Initialize parent class
        super().__init__(out_prefix='pubmed_', out_suffix='.xml')

        # Search related constants
        self.url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.search_prefix = 'esearch.fcgi'
        self.fetch_prefix = 'efetch.fcgi'
        self.tool = 'kenting_beach'
        self.email = 'atyro123@gmail.com'
        self.uri_parameters = []

        # Search related parameters
        self.pubmed_search_term = ''
        self.retmax = 100
        self.max_ids = 10000

        # Runtime related parameters
        self.save_to_disk = save_to_disk

