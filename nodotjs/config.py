from ConfigParser import SafeConfigParser
import sys
import uuid

if len(sys.argv) != 2:
    print """
Nodotjs must be invoked with a single argument, telling it
which mode from `config.ini` to use:

python nodotjs/server.py <MODE>

Look at `config.ini` for defined modes. Defaults are `production`,
`staging`, and `test`."""
    exit(1)

MODE = sys.argv[1]
PARSER = SafeConfigParser()

if not len(PARSER.read('config.ini')):
    print "No config.ini file found in this directory.  Writing a config..."

    modes = ['production', 'staging', 'test']
    for i in range(0, len(modes)): # ew redis dbs made me loop like this
        mode = modes[i]
        PARSER.add_section(mode)
        PARSER.set(mode, 'db', str(i))
        PARSER.set(mode, 'cookie_secret', str(uuid.uuid4()))
        PARSER.set(mode, 'timeout', '30')
        PARSER.set(mode, 'port', '7000')
        PARSER.set(mode, 'templates_dir', './templates')

    try:
        conf = open('config.ini', 'w')
        PARSER.write(conf)
        conf.close()
    except IOError:
        print "Could not write config file to `config.ini`, exiting..."
        exit(1)

DB = int(PARSER.get(MODE, 'db'))
COOKIE_SECRET = PARSER.get(MODE, 'cookie_secret')
TIMEOUT = int(PARSER.get(MODE, 'timeout'))
PORT = int(PARSER.get(MODE, 'port'))
TEMPLATES_DIR = PARSER.get(MODE, 'templates_dir')