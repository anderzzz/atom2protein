'''Bla bla

'''
from _version import __version__

import sqlite3
import datetime

class DBHandler:
    '''Bla bla

    '''
    def _entry_metadata(self, who_entered):
        '''Create metadata for any database entry.

        Args:
            who_entered (string): Name of function that made the entry into the
                                  database.

        Returns:
            meta (list): List of entry metadata, all strings. This includes in
                         order a string that describes who/what generated the
                         entry, the version of the who or what, and the time of
                         entry.

        '''
        version = __version__
        created_by = who_entered
        time_of_entry = datetime.datetime.now().ctime()

        return [created_by, version, time_of_entry]

    def _local_entry(self, dynamic_entry, who_entered):
        '''Bla bla

        '''
        c = self.conn.cursor()
        out_row_data = self._entry_metadata(who_entered)
        out_row_data += dynamic_entry
        out_row_data = ["'%s'" %(x) for x in out_row_data]
        out_row_str = ','.join(out_row_data)
        c.execute("INSERT INTO %s VALUES (%s)" %(self.table_name, out_row_str))
        self.conn.commit()

    def close(self):
        '''Bla bla

        '''
        self.conn.close()

    def __init__(self, db_method_name, static_file_path, db_file_path, 
                 table_name=None, headers=None):
        '''Bla bla

        '''
        self.db_path = db_file_path
        self.static_file_path = static_file_path

        if db_method_name == 'local':
            self.table_name = table_name
            self.conn = sqlite3.connect(self.db_path)
            c = self.conn.cursor()
            sql_cmd = "CREATE TABLE %s " %(self.table_name)
            sql_cmd += "(" + ','.join(headers) + ")"

            try:
                c.execute(sql_cmd)
                self.conn.commit()
            except sqlite3.OperationalError:
                pass

            self.make_db_entry = self._local_entry

        elif db_method_name == 'django':
            pass

        else:
            raise AttributeError("Database method %s does not exist" %(db_method_name))
