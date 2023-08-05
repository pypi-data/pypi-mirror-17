from voluptuous import *

# Configuration file: client
def config_client():
    return {
        Optional('hosts', default='127.0.0.1'): Any(None, str, list),
        Optional('port', default=9200): Any(
            None, All(Coerce(int), Range(min=1, max=65535))
        ),
        Optional('url_prefix', default=''): Any(None, str),
        Optional('use_ssl', default=False): All(Any(int, bool), Coerce(bool)),
        Optional('certificate', default=None): Any(None, str),
        Optional('client_cert', default=None): Any(None, str),
        Optional('client_key', default=None): Any(None, str),
        Optional('aws_key', default=None): Any(None, str),
        Optional('aws_secret_key', default=None): Any(None, str),
        Optional('aws_region', default=None): Any(None, str),
        Optional('ssl_no_validate', default=False): All(
            Any(int, bool), Coerce(bool)),
        Optional('http_auth', default=None): Any(None, str),
        Optional('timeout', default=30): All(
            Coerce(int), Range(min=1, max=86400)),
        Optional('master_only', default=False): All(
            Any(int, bool), Coerce(bool)),
    }

# Configuration file: logging
def config_logging():
    return {
        Optional(
            'loglevel', default='INFO'): Any(None,
            'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
            All(Coerce(int), Any(0, 10, 20, 30, 40, 50))
        ),
        Optional('logfile', default=None): Any(None, str),
        Optional(
            'logformat', default='default'): Any(None, All(str,
            Any('default', 'json', 'logstash'))
        ),
        Optional(
            'blacklist', default=['elasticsearch', 'urllib3']): Any(None, list),
    }

def client():
    return Schema(
        {
            Optional('client'): config_client(),
            Optional('logging'): config_logging(),
        }
    )
