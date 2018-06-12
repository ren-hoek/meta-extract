import requests
import os
import json
import re
import pymongo as py


def remove_non_ascii(s): return "".join(i for i in s if ord(i)<128)


def get_resp(g, a, s=False):
    """Get Mayan with requests"""
    resp = requests.get(g, auth=a, stream=s)
    if s == False:
        return json.loads(resp.text)
    else:
        return resp


def get_page_num(p):
    """Extract page number from page URL."""
    return p['url'][p['url'].rfind("/")+1:]


def get_next_page(p):
    """Extract p."""
    return p['next'][p['next'].rfind("?")+6:]


def get_tika_content(d, a):
    """Call TIKA api for rmeta content.

    Calls the rmeta api from TIKA whihc extracts file metadata
    and content.
    Input:
        d: Mayan document API output
        a: Mayan authorization
    Output:
        c: Dictionary of document metadata and content
    """
    down_url = d['latest_version']['download_url']
    pages = get_resp(d['latest_version']['pages_url'], a)['results']
    try:
        page_no = get_page_num(pages[0])
    except:
        page_no = 0
    file_stream = get_resp(down_url, a, True)
    resp = requests.put('http://tika:9998/rmeta/text', file_stream)
    if resp.status_code == 200:
        c = json.loads(resp.text)[0]
        print(c['Content-Type'])
        if 'X-TIKA:content' in c:
            c['content'] = remove_non_ascii(c['X-TIKA:content'])
            c['page_no'] = page_no
        else:
            c['content'] = 'No X-TIKA:content'
            c['page_no'] = page_no
    else:
        c = {'page_no': 0, 'content': str(resp.status_code) + ": "+ resp.reason}
    for k in c:
        if k.find(".") > -1:
            c[k.replace(".", ":")] = c.pop(k)
    """
    try:
        c = unpack.from_buffer(file_stream)
    except:
        c = []
    """
    return c


def insert_aug_metadata(d, a):
    """Insert TIKA extracted metadata and coient."""
    client = py.MongoClient('mongo')
    db = client['docs']
    col = db['aug_meta']
    d = get_tika_content(d, a)
    col.insert_one(d)
    return True

