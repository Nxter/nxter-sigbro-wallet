# -*- coding: UTF-8 -*-

# Global modules
import json
import requests

class testNxt():
  def get_json(self, url):
    """GET request and return JSON response"""
    try:
      r = requests.get(url=url, timeout=3)
    except requests.exceptions.RequestException as e:
      tmp = """{"error" : "Connection timeout: %s " }""" % (url)
      data = json.loads(tmp)
      return data

    if r.status_code == 200:
      data = json.loads(r.text)
      return data
    else:
      tmp = """{"error" : "Error while try to get information from %s " }""" % (url)
      data = json.loads(tmp)
      return data

  def test_get_tx_info(self):
    url = """http://localhost:8000/api/v2/explorer/nxt/tx/124083191368220338261/"""
    res = self.get_json(url)

    #print (res)

    assert (res['error'] is None) , 'Have an error while run get_tx_info'  
    assert (res['data'] is not  None) , 'Have not data section  while run get_tx_info'  

 
test = testNxt()
test.test_get_tx_info()



