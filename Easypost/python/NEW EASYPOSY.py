import easypost

try:
    with open('/home/devbox/Desktop/conf/conf.txt') as f:
        TESTKEY = str.splitlines(f.readline())
        PRODKEY = str.splitlines(f.readline())
        f.close()
        TESTKEY=TESTKEY[0]
        PRODJEY = PRODKEY[0]
except:
    print('failed to parse conf file for values')

OUTPUT = '/Users/madams/Desktop/CODE/EasyPost/python/output.txt'

easypost.api_key = TESTKEY

'''

'''