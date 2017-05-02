#!/usr/bin/python
import urllib2
from urllib2 import urlopen
import re
import time

yahoo_search_url_prefix = '''https://search.yahoo.com/search?q='''
#bing_search_url_prefix = '''https://www.bing.com/search?q='''
get_total_results = re.compile('<span[^>]*> *([0-9,]+) results *</span>')
webscore_dict = {}

def replace_spaces_with_plus (term):
    return(term.replace(' ','+'))

def do_provider_search(term):
    url = yahoo_search_url_prefix + '"'+replace_spaces_with_plus(term)+'"'
    url_stream = urlopen(url)
    data = str(url_stream.read())
    url_stream.close()
    return(data)

def do_provider_search_with_pause(term,timing=1,reps=0):
    ## without this function, the system will halt every time
    ## the internet connection is interupted
    if reps>0:
        print('Internet search failure')
        output = False
        total = -1
    else:
        try:
            output = do_provider_search(term)
            total = str(get_total_results.search(output).group(1).replace(',',''))
        except:
            print('Temporary internet search failure. Trying again')
            time.sleep(timing)
            total = do_provider_search_with_pause(term,timing=timing,reps=reps+1)
    return(total)
