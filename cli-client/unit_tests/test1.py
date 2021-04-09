import pytest
import energy_group14
import urllib3

def test_CheckC():
    urllib3.disable_warnings()
    res = energy_group14.check('giannis@gmail.com')
    assert res == True

def test_CheckW():
    urllib3.disable_warnings()
    res =energy_group14.check('giannisgmail.com')
    assert res == False

def test_Check_cred():
    urllib3.disable_warnings()
    res = energy_group14.check_cred('giannis', '123', 'giannis@gmail.com')
    assert res == True

def test_Check_credw1():
    urllib3.disable_warnings()
    res = energy_group14.check_cred('gian#%@nis', '123', 'giannis@gmail.com')
    assert res == False

def test_Check_credw2():
    urllib3.disable_warnings()
    res = energy_group14.check_cred('giannis', '12 3', 'giannis@gmail.com')
    assert res == False

def test_Check_credw3():
    urllib3.disable_warnings()
    res = energy_group14.check_cred('giannis', '123', 'giannisgmail.com')
    assert res == False
