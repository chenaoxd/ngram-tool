#coding=utf-8
import urllib2, urllib
import gzip
import json

CONFIG = {
    'WORD_SEGMENT':{
        'STANFORD_URL': 'http://localhost:8080/segment'
    }
}

def http_request_real(url, data, referer=None, method='get', headers=None):
    if headers == None:
        user_agent = 'Mozilla/5.0'
        headers = {
            'User-Agent': user_agent
        }
        if referer != None:
            headers['Referer'] = referer
    else:
        headers = headers

    if method == 'get':
        req = urllib2.Request(url + '?' + urllib.urlencode(data), headers=headers)
    elif method == 'post':
        req = urllib2.Request(url, urllib.urlencode(data), headers=headers)
    conn = urllib2.urlopen(req)
    content = conn.read()
    if conn.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(content)
        f = gzip.GzipFile(fileobj=buf)
        return f.read()
    return content

def stanford_seg(sentence):
    try:
        res = json.loads(http_request_real(CONFIG['WORD_SEGMENT']['STANFORD_URL'], {'sentence': sentence}, method='post'))['content']
    except UnicodeEncodeError:
        res = json.loads(http_request_real(CONFIG['WORD_SEGMENT']['STANFORD_URL'], {'sentence': sentence.encode('utf-8')}, method='post'))['content']

    return res

def seg_file(file_path, output_path):
    output_file = open(output_path, 'w')
    with open(file_path) as input_file:
        for line in input_file:
            line = line.strip()
            seged_line = stanford_seg(line)
            output_file.write(seged_line.encode('utf-8') + '\n')
