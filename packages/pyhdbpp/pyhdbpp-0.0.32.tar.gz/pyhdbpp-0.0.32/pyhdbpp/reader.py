
import sys
import argparse
import yaml
import logging
import logging.handlers
import os
import datetime
import importlib
import collections.abc
import traceback


logger = logging.getLogger('hdbpp_reader')

###############################################################################

__usage__ = """
Usage:

:> reader : print this help

:> reader [options] list [pattern] :
    returns matching attributes from database

:> reader [options] <attribute> :
    print last value for attribute

:> reader [options] <attribute> <start> <stop> :
    returns values for attribute between given dates

Options (at least some is needed):
    --prompt
    --config=user:password@host:port/database
    --database=
    --host=
    --port=
    --user=
    --password=
    --log-level=

"""

def get_default_reader(tango_host=''):
    try:
        import tango
        if tango_host:
            tangodb = tango.Database(*tango_host.split(':'))
        else:
            tangodb = tango.Database()

        get_hdb_property = lambda p: tangodb.get_property('HDB++',p)[p]
        schema = get_hdb_property('DefaultSchema')
        try:
            logger.debug('DefaultSchema: {}'.format(schema))
            schema = schema[0] if not isinstance(schema,str) else schema
        except:
            logger.warning('get_default_reader: unable to get DefaultSchema',
                exc_info=logger.level==logging.DEBUG)
            
        data = dict(l.split('=') for l in get_hdb_property(schema) if '=' in l)
        return reader(apiclass=data['apiclass'],config=data['config'])
    
    except:
        logger.warning('get_default_reader: unable to get Tango DB',
                       exc_info=logger.level==logging.DEBUG)

    
def reader(apiclass='pyhdbpp.abstract.AbstractReader', config=None):
    """
    Initialize a reader object, based on the specified backend
    and a config dictionnary.
    """
    print('Creating pyhdbpp.reader(%s)' % config)
    if isinstance(config,(bytes,str)):
        
        if os.path.isfile(config):
            config = load_config_from_file(config)
        elif config.startswith('tango:'):
            config = load_config_from_tango(config)
        else:
            config = parse_config_string(config)
            
        if not validate_config(config):
            logger.error(config)
            raise Exception('InvalidConfig')

    apiclass = config.pop('apiclass',apiclass)
    mod_name, class_name = apiclass.rsplit('.', 1)
    module = importlib.import_module(mod_name)        

    return getattr(module, class_name)(**config)

def load_config_from_file(config_file):
    """
    Load the config file from the given path
    Arguments:
        config_file : str -- Path and name of the config file to load
    Returns:
        dict -- dictionary of values from the yaml config file.
    """

    try:
        logger.debug('load_config_from_file(%s)' % config_file)
        with open(config_file, 'r') as fp:
            try:
                config = yaml.safe_load(fp)

            except yaml.YAMLError as error:
                logger.error("Unable to load the config file: {}. Error: {}"
                            .format(config_file, error))
                return None

        # return the dictionary with the configuration in for the script to use
        return config

    except Exception as e:
        logger.error(str(e))
        return None
    
def load_config_from_tango(schema, root = 'HDB++', tango_host = ''):
    """
    Load config from TangoDB using tango://ObjectName.PropertyName
    Current version only accept Tango Free Properties
    """
    try:
        logger.debug('load_config_from_tango(%s)' % schema)
        schema = schema.replace('tango:','').strip('/')
        if '.' in schema:
            root,schema = schema.rsplit('.',1)
        if ':' in root:
            tango_host, root = schema.split('/')
            
        import tango
        if tango_host:
            tangodb = tango.Database(*tango_host.split(':'))
        else:
            tangodb = tango.Database()            
    
        get_hdb_property = lambda p: tangodb.get_property(root,p)[p]
        config = dict(l.split('=') for l in get_hdb_property(schema) 
                      if '=' in l)
        
        config['database'] = config.get('database',
                            config.get('db_name',
                           config.get('dbname','hdbpp')))
        config['password'] = config.get('password',
                            config.get('passwd',
                           config.get('token','')))
        return config
    
    except Exception as e:
        logger.error(str(e))
        return None

def parse_config_string(connect_str):
    """
    Parse a connect string into the various element to initiate a connection.
    Arguments:
        connect_str : str -- user:password@host:port/database
    Returns:
        dict -- dictionary of values from the connect string.
    """
    try:
        logger.debug('parse_config_str(%s)' % connect_str)
        
        config = {}
        config_split, config['database'] = connect_str.split('/')
        user_pass, host_port = config_split.split('@')
        config['user'], config['password'] = user_pass.split(':')
        config['host'], config['port'] = host_port.split(':')

        return config
    
    except Exception as e:
        logger.debug(traceback.print_exc())
        logger.error(str(e))
        return None    

def add_defaults_to_config(config):
    """
    Ensure the defaults for certain config params are part of the configuration
    Arguments:
        config : dict -- Configuration
    """
    if 'database' not in config:
        config['database'] = 'hdb'

    if 'host' not in config:
        config['host'] = 'localhost'

    if 'port' not in config:
        config['port'] = 3306

def validate_config(config):
    """
    Validate the config. Certain values will be checked for, and if not present
    the config is considered not valid and false is returned
    Arguments:
        config : dict -- dictionary of values that represent the config.
    Returns:
        bool -- True on success, False otherwise
    """
    
    if not isinstance(config,collections.abc.Mapping):
        logger.error("Configuration must be a dictionary")
        return False
    
    if len(config) == 0:
        logger.error("Invalid configuration, no values loaded.")
        return False

    if 'database' not in config:
        logger.error("Invalid configuration, no database provided.")
        return False

    if 'user' not in config:
        logger.error("Invalid configuration, no username provided to connect to the database.")
        return False

    if 'password' not in config:
        logger.error("Invalid configuration, no password provided to connect to the database.")
        return False

    return True



def read():
    parser = argparse.ArgumentParser(description="HDB++ reader")
    parser.add_argument("-v", "--version", action="store_true", help="version information")
    parser.add_argument("-D", "--debug", action="store_true", help="debug output for development")
    parser.add_argument("--syslog", action="store_true", help="send output to syslog")
    parser.add_argument("-b", "--backend", default="mariadb.MariadbReader", help="Reader backend.")
    parser.add_argument("-P", "--prompt", action="store_false", help="Prompt for connection details")
    parser.add_argument("-c", "--config", default=None, help="config file to use")
    parser.add_argument("-C", "--connect", help="connect string to connect to the database.")
    parser.add_argument("-d", "--database", help="database to connect to.")
    parser.add_argument("-H", "--host", help="host to connect to.")
    parser.add_argument("-u", "--user", help="User for the database connection.")
    parser.add_argument("-p", "--password", help="password for the database connection.")
    parser.add_argument("-t", "--timeformat", help="Time format expression.")

    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "list" command
    parser_list = subparsers.add_parser('list', help='List attributes matching the pattern from database')
    parser_list.add_argument("-P", '--pattern', type=str, nargs='?', default=None, help='SQL like type pattern')
    parser_list.set_defaults(func=list_attributes)

    parser_read = subparsers.add_parser('read', help='Read attribute value.')
    parser_read.add_argument('attribute', type=str, nargs='?', default=None, help="Name of the attribute to extract.")
    parser_read.add_argument('start', type=datetime.date.fromisoformat, nargs='?', default=None, help="Start date for the query.")
    parser_read.add_argument('stop', type=datetime.date.fromisoformat, nargs='?', default=None, help="End date for the query.")
    parser_read.set_defaults(func=read_attribute)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    stdout_formatter = logging.Formatter("%(asctime)s hdbpp_reader[%(process)d]: %(message)s", "%Y-%m-%d %H:%M:%S")
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(stdout_formatter)
    logger.addHandler(stdout_handler)

    if args.syslog:
        syslog_formatter = logging.Formatter("hdbpp_reader[%(process)d]: %(message)s")
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        syslog_handler.setFormatter(syslog_formatter)
        logger.addHandler(syslog_handler)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.version:
        from pyhdbpp import version_major, version_minor, version_patch
        print("Version {}.{}.{}".format(str(version_major), str(version_minor), str(version_patch)))

    # Build a config based on the provided information
    # A config file is preferred, then a single connect argument,
    # then the prompt.
    config = {}

    if args.config:
        config = load_config_from_file(args.config)
    elif args.connect:
        config = parse_config_string(args.connect)
    elif args.prompt:
        config['host'] = input('host (default localhost):') or 'localhost'
        config['port'] = input('port (default 3306):') or 3306
        config['database'] = input('database (default hdb):') or 'hdb'
        config['user'] = input('user:')
        config['password'] = input('password:')

    add_defaults_to_config(config)

    # Check the config.
    if not validate_config(config):
        return False

    # Build the reader object
    _reader = reader(args.backend, config)

    return args.func(_reader, args)


def list_attributes(_reader, args):
    pattern = args.pattern
    print('\n'.join(_reader.get_attributes(pattern=pattern)))

def read_attribute(_reader, args):
    start = args.start
    stop = args.stop
    attribute = args.attribute

    if start is None:
        print(_reader.get_last_attribute_value(attribute))
    else:
        datas = _reader.get_attribute_values(attribute, start, stop,
                                        decimate=True)
        for data in datas:
            data_str = '\t'.join(map(str,data))
            if args.timeformat:
                try:
                  timeformat = eval(args.timeformat)
                except:
                  timeformat = str

                print('%s\t%s' % (timeformat(data[0]), data_str))
            else:
                print(data_str)

if __name__ == '__main__':
    read()
