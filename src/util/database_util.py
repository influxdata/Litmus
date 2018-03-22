
import src.util.sources_util as su

def get_default_databases_links(test_class_instance, default_sources):
    '''
    :param test_class_instance: instance of test class
    :param default_sources: dictionary of default sources, i.e. sources that
                 were created when chronograf was added to the cluster
    :return: list of links to the dbs, .i.e.[u'/chronograf/v1/sources/1/dbs',
                  u'/chronograf/v1/sources/2/dbs']
    '''
    test_class_instance.mylog.info('database_util.get_default_databases_links() functions is called')
    dbs_link_list=[]
    for source in default_sources.keys():
        dbs_link_list.append(su.get_source_dbs_link(test_class_instance,
                                        source_id=source, sources_dictionary=default_sources))
        test_class_instance.mylog.info('database_util.get_default_databases_links()'
                                       ' - dbs links =' + str(dbs_link_list))
    return dbs_link_list
