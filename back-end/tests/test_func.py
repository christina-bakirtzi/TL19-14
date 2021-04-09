import os
import pytest
import urllib3
from app.models import User
from tests import data
from tests.utils import *
from .configtests import client
from werkzeug.datastructures import FileStorage
urllib3.disable_warnings()


class TestAdmin(object):
    token = None

    @staticmethod
    def admin_token():
        return User.query.filter(User.username == 'admin').first().token

    @staticmethod
    def user1_username():
        return data.users[0]['username']

    @staticmethod
    def user1_password():
        return data.users[0]['password']

    @staticmethod
    def user1_quota():
        return User.query.filter(User.username == data.users[0]['username']).first().quotas

    @staticmethod
    def user1_email():
        return User.query.filter(User.username == data.users[0]['username']).first().email

    @staticmethod
    def user1_token():
        return User.query.filter(User.username == data.users[0]['username']).first().token

    def test_T01_health_check(self, client):
        rv = client.get(url_for('/HealthCheck'))
        assert rv.status_code == 200

    def test_T02_reset(self, client):
        rv = client.post(url_for('/Reset'))
        assert rv.status_code == 200

    def test_T03_admin_login(self, client):
        rv = client.post(url_for('/Login'))
        assert rv.status_code == 401

        rv = client.post(url_for('/Login'), data={'username': 'admin', 'password': '321nimda'})
        assert rv.status_code == 200
        assert rv.json['token'] == User.query.filter(User.username == 'admin').first().token

    @pytest.mark.parametrize("user_data", data.users)
    def test_T04_register_new_user(self, client, user_data):
        rv = client.post(url_for('/Admin/users'))
        assert rv.status_code == 401

        rv = client.post(url_for('/Admin/users'), headers=auth_header(self.admin_token()), data=user_data)
        assert rv.status_code == 200

        assert User.query.filter(User.username == user_data['username']).first() is not None
        assert User.query.filter(User.username == user_data['username']).first().verify_password(user_data['password'])
        assert User.query.filter(User.username == user_data['username']).first().is_admin is False
        assert User.query.filter(User.username == user_data['username']).first().token is None

        rv = client.post(url_for('/Admin/users'), headers=auth_header(self.admin_token()), data=user_data)
        assert rv.status_code == 400

    def test_T05_user_login(self, client):
        rv = client.post(url_for('/Login'))
        assert rv.status_code == 401

        rv = client.post(url_for('/Login'),
                         data={'username': self.user1_username(), 'password': self.user1_password()})
        assert rv.status_code == 200
        assert rv.json['token'] == self.user1_token()

    def test_T06_importing_csv(self, client):
        file = os.path.join("C://Users//chris//Desktop//ActualTotalLoad.csv")
        my_file = FileStorage(
            stream=open(file, "rb"),
            filename="ActualTotalLoad.csv",
            content_type="text/csv",
        )
        rv = client.post(url_for('/Admin/ActualTotalLoad'),
                         headers=auth_header(User.query.filter(User.username == 'admin').first().token),
                         data={"file": my_file}, content_type="multipart/form-data")

    @pytest.mark.parametrize("date_data", data.date)
    def test_T07_user_get_actual_total_load(self, client, date_data):
        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/date/' + date_data['date']),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 200
        valid_response(rv.json, date_data['response'])

        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/month/' + date_data['date']),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 400

        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/year/' + date_data['date']),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 400

    def test_T08_user_out_of_quotas(self, client):
        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/month/2018-01-01'),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 402

    def test_T09_adming_updates_user_quota(self, client):
        rv = client.put(url_for('/Admin/users/foo'), headers=auth_header(self.admin_token()), data={'quota': 10})
        assert rv.status_code == 200


    @pytest.mark.parametrize("month_data", data.month)
    def test_T10_user_get_request_after_quotas_update(self, client, month_data):
        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/month/' + month_data['month']),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 200
        valid_response(rv.json, month_data['response'])

        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/year/' + month_data['month']),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 400

        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/date/' + month_data['month']),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 400

        rv = client.get(url_for('/ActualTotalLoad/Greece/PT60M/month/' + '2018-03'),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 403


    def test_T11_admin_get_user_status(self, client):
        rv = client.get(url_for('/Admin/users/foo'), headers=auth_header(self.admin_token()))
        assert rv.status_code == 200
        temp = rv.json['message']
        assert temp['username'] == self.user1_username()
        assert temp['email'] == self.user1_email()
        assert temp['quota'] == self.user1_quota()

    def test_T12_user_trying_admin_requests(self, client):
        rv = client.get(url_for('/Admin/users/admin'), headers=auth_header(self.user1_token()))
        assert rv.status_code == 401

        rv = client.post(url_for('/Admin/users'), headers=auth_header(self.user1_token()))
        assert rv.status_code == 401

        rv = client.get(url_for('/Admin/users/ActualTotalLoad'), headers=auth_header(self.user1_token()))
        assert rv.status_code == 401

        rv = client.get(url_for('/Admin/users/DayAheadTotalLoadForecast'), headers=auth_header(self.user1_token()))
        assert rv.status_code == 401

        rv = client.get(url_for('/Admin/users/AggregatedGenerationPerType'), headers=auth_header(self.user1_token()))
        assert rv.status_code == 401

    def test_T13_admin_logs_out(self, client):
        rv = client.post(url_for('/Logout'))
        assert rv.status_code == 401

        rv = client.post(url_for('/Logout'), headers=auth_header(self.admin_token()))

        assert rv.status_code == 200
        assert not self.admin_token()

    def test_T14_user_logs_out(self, client):
        rv = client.post(url_for('/Logout'))
        assert rv.status_code == 401

        rv = client.post(url_for('/Logout'), headers=auth_header(self.user1_token()))

        assert rv.status_code == 200
        assert not self.user1_token()

    def test_T15_user_request_after_loging_out(self, client):
        rv = client.get(url_for('/DayAheadTotalLoadForecast/Greece/PT60M/year/2018'),
                        headers=auth_header(self.user1_token()))
        assert rv.status_code == 401
