# -*- coding: utf-8 -*-

'''
Created on Sep 28, 2013

@author: kamushadenes
'''

import requests
import cookielib as cookiejar
from bs4 import BeautifulSoup as bs

class Browser():
    '''
    classdocs
    '''
    
    def set_headers(self,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'}):
        self.headers=headers
    
    def get_bs(self,element):
        return bs(element)
    
    def get_response(self,url):
        return self.session.get(url, headers=self.headers)

    def set_cookies(self,jar):
        self.cookies = jar
        
    def download(self,url,localfile=''):
        if localfile == '':
            localfile = url.split('/')[-1]
        r = self.session.get(url, headers=self.headers, stream = True) # here we need to set stream = True parameter
        with open(localfile, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return localfile
    
    def post_response(self,url,pdata):
        return self.session.post(url, pdata, headers=self.headers)
    
    
    def __init__(self):
        self.session = requests.Session()
        jar = cookiejar.CookieJar()
        self.set_cookies(jar)
        self.set_headers()
        
        

        
        
        
