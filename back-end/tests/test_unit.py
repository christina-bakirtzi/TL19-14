# import pytest
# from app.models import User
from .configtests import new_user,new_actual_total_load
from app.jsontocsv import json2csv


class TestUnit(object):
    def test_new_user(self, new_user):
        assert new_user.username == 'foo'
        assert new_user.password_hash == 'bar'
        assert new_user.email == 'foo@gmail.com'
        assert not new_user.is_admin
        assert not new_user.token
        assert new_user.quotas == 7

    def test_hash_password(self, new_user):
        new_user.hash_password('new_password')
        assert new_user.hash_password != 'new_password'
        assert new_user.verify_password('new_password')
        assert not new_user.verify_password('wrong_password')
        assert not new_user.verify_password('bar')

    def test_actual_total_load(self, new_actual_total_load):
        assert new_actual_total_load.entity_created_at == '2019-10-01 13:46:36.761013'
        assert new_actual_total_load.entity_modified_at == '2019-10-01 13:46:36.761013'
        assert new_actual_total_load.action_task_id == 312126
        assert new_actual_total_load.status == 'NaN'
        assert new_actual_total_load.year == 2018
        assert new_actual_total_load.month == 1
        assert new_actual_total_load.day == 4
        assert new_actual_total_load.date_time == '2018-01-04 05:30:00'
        assert new_actual_total_load.area_name == 'DE-AT-LU'
        assert new_actual_total_load.update_time == '2018-04-01 04:01:28'
        assert new_actual_total_load.total_load_value == 67928.13
        assert new_actual_total_load.area_type_code_id == 2
        assert new_actual_total_load.map_code_id == 7
        assert new_actual_total_load.area_code_id == 55448
        assert new_actual_total_load.resolution_code_id == 1
        assert new_actual_total_load.row_hash == 'B82C7EFD-60F2F573-C96FC45E-D1C6BDCF-90931B6E-F597F424-ED2AB8DC' \
                                                 '-417B2132-1DCDCEFE-7AA96D2A-994E7E4A-48B611ED-148827AF-B30EF809' \
                                                 '-95994DB3-033F3720'

    def test_json2csv(self):
        csv_response = json2csv([{'country': 'Greece', 'city': 'Athens'}, {'country': 'Italy', 'city': 'Rome'}], ["country", "city"])
        response = str('country,city\r\nGreece,Athens\r\nItaly,Rome\n\r').strip('\r\n')
        assert csv_response == response
