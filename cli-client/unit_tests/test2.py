import unittest
import requests
from mock import Mock, patch, MagicMock
from energy_group14_test import HealthCheck, Reset, Login, Logout, ActualTotalLoad, AggregatedGenerationPerType, DayAheadTotalLoadForecast, ActualvsForecast, Admin
import subprocess
import json
import datetime
import os
import os.path
from os import path
from os.path import expanduser
import urllib3
urllib3.disable_warnings()
st= {}
st['status'] = 'OK'

token = {}
token['token'] = '123'

import time

def test_HealthCheck():
    urllib3.disable_warnings()
    with patch.object(requests, 'get') as get_mock:
            
        get_mock.return_value = Mock(status_code = 200)
        get_mock.return_value.json.return_value = st
        assert HealthCheck() == 200
            
def test_Login():
    urllib3.disable_warnings()
    with patch.object(requests, 'post') as post_mock:
            
        post_mock.return_value = Mock(status_code =200)
        post_mock.return_value.json.return_value = token
        assert Login('giannis', '111') == 200
            
# def test_ActualTotalLoad():
#     urllib3.disable_warnings()
#     with patch.object(requests, 'get') as get_mock:
#
#         get_mock.return_value = Mock(status_code =200)
#         get_mock.return_value.json.return_value = token
#
#         assert ActualTotalLoad('Greece', 'PT60M', datetime.date(2018,1,1) , None , None , 'json') == 200
#
#
# def test_AggregatedGenerationPerType():
#     urllib3.disable_warnings()
#     with patch.object(requests, 'get') as get_mock:
#
#         get_mock.return_value = Mock(status_code =200)
#         get_mock.return_value.json.return_value = token
#
#         assert AggregatedGenerationPerType('Greece', 'PT60M','Fossil Oil',  datetime.date(2018,1,1) , None , None , 'json') == 200
#
#
# def test_DayAheadTotalLoadForecast():
#     urllib3.disable_warnings()
#     with patch.object(requests, 'get') as get_mock:
#
#         get_mock.return_value = Mock(status_code =200)
#         get_mock.return_value.json.return_value = token
#
#         assert DayAheadTotalLoadForecast('Greece', 'PT60M', datetime.date(2018,1,1) , None , None , 'json') == 200
#
# def test_ActualvsForecast():
#     urllib3.disable_warnings()
#     with patch.object(requests, 'get') as get_mock:
#
#         get_mock.return_value = Mock(status_code =200)
#         get_mock.return_value.json.return_value = token
#
#         assert ActualvsForecast('Greece', 'PT60M', datetime.date(2018,1,1) , None , None , 'json') == 200

def test_Admin_newuser():
    urllib3.disable_warnings()
    with patch.object(requests, 'post') as post_mock:
            
        post_mock.return_value = Mock(status_code =200)
        post_mock.return_value.json.return_value = token
            
        assert Admin('giannis', None, None, None, '123', 'giannis@gmail.com', 10, 'C:/Users/user') == 200
# def test_Admin_moduser():
#     urllib3.disable_warnings()
#     with patch.object(requests, 'put') as put_mock:
#
#         put_mock.return_value = Mock(status_code =200)
#         put_mock.return_value.json.return_value = token
#
#         assert Admin(None, 'giannis', None, None, '123', 'giannis@gmail.com', 10, 'C:/Users/user') == 200
def test_Admin_userstatus():
    urllib3.disable_warnings()
    with patch.object(requests, 'get') as get_mock:

        get_mock.return_value = Mock(status_code =200)
        get_mock.return_value.json.return_value = token

        assert Admin(None, None , 'giannis', None, None, None , None , None) == 200
# def test_Admin_newdata():
#     urllib3.disable_warnings()
#     home = expanduser("~")
#     tokenpath = "%s/softeng19bAPI.token" % home
#     with patch.object(requests, 'post') as post_mock:
#
#         post_mock.return_value = Mock(status_code =200)
#         post_mock.return_value.json.return_value = token
#
#         assert Admin(None, None , None , 'ActualTotalLoad', None, None , None , tokenpath) == 200


def test_Logout():
    urllib3.disable_warnings()
    with patch.object(requests, 'post') as post_mock:
            
        post_mock.return_value = Mock(status_code = 200)
        post_mock.return_value.json.return_value = st
        assert Logout() == 200
            
              
              
    