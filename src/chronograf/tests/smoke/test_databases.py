
import pytest
import src.util.login_util as lu
import src.util.database_util as du
from src.chronograf.lib import rest_lib

@pytest.mark.usefixtures('delete_created_sources', 'default_sources',
                         'chronograf')
class TestDefaultDatabases():
    '''
    '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

    def header(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s START --------------->' % test_name)
        self.mylog.info('#######################################################')

    def footer(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s END --------------->' % test_name)
        self.mylog.info('#######################################################')
        self.mylog.info('')

    def test_get_default_databases(self):
        '''
        TODO TEST STEPS
        '''
        self.header('test_get_default_databases')
        self.mylog.info('test_get_default_databases - STEP 1: GET DBS LINKS')
        dbs_links=du.get_default_databases_links(self, default_sources=self.default_sources)
        for db in dbs_links:
            self.rl.get_databases_for_source(self.chronograf, db)
        

