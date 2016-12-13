'''Bla bla

'''
from urllib.request import urlopen
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

class DownloadError(Exception):
    pass

class WebService:

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
    '''Bla bla

    '''
    def search(self):
        '''Bla bla

        '''
        top = Element('orgPdbQuery')
        child_query = SubElement(top, 'queryType')
        child_query.text = 'org.pdb.query.simple.ResolutionQuery'
        child_descr = SubElement(top, 'description')
        child_descr.text = 'Automated query of PDB'
        child_comparator = SubElement(top, 'refine.ls_d_res_high.comparator')
        child_comparator.text = 'between'
        child_min = SubElement(top, 'refine.ls_d_res_high.min')
        child_min.text = '0.3'
        child_max = SubElement(top, 'refine.ls_d_res_high.max')
        child_max.text = '1.0'

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
            http_string = self.url_filebase + item_name + '.pdb'
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
        super().__init__(out_suffix='.pdb')

        # Parameters relevant to a query to define a set of PDB IDs
        self.url_base = 'http://www.rcsb.org/pdb/rest/'
        self.url_search = 'search'

        # Parameters relevant to retrieving the structure data
        self.url_filebase = 'https://files.rcsb.org/download/'
        self.save_to_disk = save_to_disk 
        self.print_list_only = print_list_only

class PMCData(WebService):
    '''Bla bla

    '''
    def set_search_term(self, search_term):
        '''Bla bla

        '''
        self.pubmed_search_term = search_term

    def set_retmax(self, retmax):
        '''Bla bla

        '''
        self.retmax = str(retmax)

    def search(self):
        '''Bla bla

        '''
        search_terms = ['tool=' + self.tool, 'email=' + self.email]
        search_terms += ['db=pubmed']
        search_terms += ['term=' + self.pubmed_search_term]
        search_params = '&'.join(search_terms)
        http_string = self.url_base + self.search_prefix + '?' + search_params

        content = self.get(http_string)
        ids = self._extract_pubmed_id(content)
        self.set_id(ids)

    def _extract_pubmed_id(self, xml_string):
        '''Bla bla

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
            fetch_terms += ['db=pubmed']
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
        super().__init__(out_prefix='pubmed_', out_suffix='.json')

        # Search related constants
        self.url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.search_prefix = 'esearch.fcgi'
        self.fetch_prefix = 'efetch.fcgi'
        self.tool = 'kenting_beach'
        self.email = 'atyro123@gmail.com'

        # Search related parameters
        self.pubmed_search_term = ''
        self.retmax = '2'

        # Runtime related parameters
        self.save_to_disk = save_to_disk

