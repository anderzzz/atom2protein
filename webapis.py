'''Bla bla

'''
import httplib2
import xml.etree.ElementTree as etree

class PDBDownloadError(Exception):
    pass

class PDBIDError(Exception):
    pass

class PubMedDownloadError(Exception):
    pass

class WebService:

    def _check_response(self, resp):
        '''Tests the HTTP return status in a reponse

        Args:
            resp (dict): Dictionary returned by the httplib2 after a GET call
                         to a web server

        Returns:
            status200 (bool): True if return status is 200, False otherwise.

        '''
        if resp['status'] == '200':
            ret = True
        else:
            ret = False

        return ret 

    def _init_websocket(self):
        '''Bla bla

        '''
        return httplib2.Http(".cache")

class PDBData(WebService):
    '''Bla bla

    '''
    def set_pdbid(self, ids):
        '''Manually set the PDB IDs of the structure data to retrieve from the
        Protein Structure Databank.

        Args:
            ids (list): List of strings, each four characters long, defining
                        the four character PDB code.

        Returns: None

        Raises: 
            PDBIDError: If given PDB codes include invalid formatted strings

        '''
        if any([len(given_id) != 4 for given_id in ids]):
            raise PDBIDError('At least one PDB ID is not four' + \
                             'characters long')
        self.pdb_files = [root.lower() + '.pdb' for root in ids]

    def _save_pdb(self, data, name):
        '''Save string of structure data as a file.

        Args:
            data (string): The structure data as a string
            name (string): Name of the file

        Returns: None

        '''
        with open(name, 'w') as f_out:
            f_out.write(data)

    def __iter__(self):
        '''Iterator for the class object which returns at each iteration a
        string in memory of the protein structure data in the PDB file format

        Args: None

        Returns: 
            content_str (string): String of structure data formatted in the PDB
                                  file format.

        Raises:
            PDBDownloadError: Return status of the HTTP request signals
                              failed operation.

        '''
        for file_name in self.pdb_files:
            resp, content = self.http.request(self.url_filebase + file_name, 'GET')
            if self._check_response(resp):
                content_str = content.decode('utf-8')
            else:
                raise PDBDownloadError('Failed to download PDB file %s' %(file_name))

            if self.save_to_disk:
                self._save_pdb(content_str, file_name)

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
        # Parameters relevant to a query to define a set of PDB IDs
        self.url_base = 'http://www.rcsb.org/pdb/rest/'
        self.pdb_files = []

        # Parameters relevant to retrieving the structure data
        self.url_filebase = 'https://files.rcsb.org/download/'
        self.save_to_disk = save_to_disk 
        self.print_list_only = print_list_only

        # Initialize the Web connection
        self.http = self._init_websocket()

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

    def search_pubmed(self):
        '''Bla bla

        '''
        search_terms = ['tool=' + self.tool, 'email=' + self.email]
        search_terms += ['db=pubmed']
        search_terms += ['term=' + self.pubmed_search_term]
        search_params = '&'.join(search_terms)
        http_string = self.url_base + self.search_prefix + '?' + search_params

        resp, content = self.http.request(http_string, 'GET')
        if self._check_response(resp):
            self.pmids = self._extract_pubmed_id(content.decode('utf-8'))
        else:
            raise PubMedDownloadError('Failed to download PubMed data with ' + \
                                      'search parameters: %s' %(search_params))

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
        '''Bla bla

        '''
        for pm_id in self.pmids:
            fetch_terms = ['tool=' + self.tool, 'email=' + self.email]
            fetch_terms += ['db=pubmed']
            fetch_terms += ['id=' + pm_id]
            fetch_params = '&'.join(fetch_terms)
            http_string = self.url_base + self.fetch_prefix + '?' + fetch_params

            resp, content = self.http.request(http_string, 'GET')
            if self._check_response(resp):
                content_str = content.decode('utf-8')
            else:
                raise PubMedDownloadError('Failed to download detailed ' + \
                                          'article metadata with fetch ' + \
                                          'parameters: %s' %(fetch_params))

            yield content_str

    def __init__(self):
        '''Bla bla

        '''
        # Search related constants
        self.url_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.search_prefix = 'esearch.fcgi'
        self.fetch_prefix = 'efetch.fcgi'
        self.tool = 'kenting_beach'
        self.email = 'atyro123@gmail.com'
        self.pmids = []

        # Search related parameters
        self.pubmed_search_term = ''
        self.retmax = '20'

        # Initialize the Web connection
        self.http = self._init_websocket() 

