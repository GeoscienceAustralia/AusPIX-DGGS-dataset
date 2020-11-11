from os.path import dirname, realpath, join, abspath
import os
import psycopg2
from psycopg2 import extras
import yaml


APP_DIR = dirname(dirname(realpath(__file__)))
TEMPLATES_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'templates')
STATIC_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'static')

LOGFILE = APP_DIR + '/flask.log'
DEBUG = True

# get db conn settings from yaml file
directory = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(directory, "secrets.yml")
DB_CON_DICT = yaml.safe_load(open(file))
# Prefix for DGGS PID

#DGGS_PID_PREFIX = 'http://pid.geoscience.gov.au/dggs/ausPIX/'
DGGS_PID_PREFIX = 'http://ec2-13-238-161-97.ap-southeast-2.compute.amazonaws.com/AusPIX-DGGS-dataset/'

if DB_CON_DICT is None:
    print('You must set up a secrets.yml file containing the DB login credentials')
    exit()


def db_select(q):
    try:
        conn = psycopg2.connect(**DB_CON_DICT['db_con'])

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(q)
        return cur.fetchall()
    except Exception as e:
        print(e)





#ORININAL
from os.path import dirname, realpath, join, abspath
import os
##import psycopg2
from psycopg2 import extras
import yaml

#
#
APP_DIR = dirname(dirname(realpath(__file__)))
TEMPLATES_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'templates')
STATIC_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'static')
#
LOGFILE = APP_DIR + '/flask.log'
DEBUG = True

# Prefix for DGGS PID
DGGS_PID_PREFIX = 'http://pid.geoscience.gov.au/dggs/ausPIX/'
#DGGS_PID_PREFIX = 'http://ec2-52-63-73-113.ap-southeast-2.compute.amazonaws.com/AusPIX-DGGS-dataset/'

