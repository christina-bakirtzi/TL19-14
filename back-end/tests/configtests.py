import pytest
from app.models import db, User, ActualTotalLoad
from app import create_app
from app.auth import reset


@pytest.fixture(scope="class")
def new_user():
    user = User(username='foo', password_hash='bar', email='foo@gmail.com', quotas=7)
    return user


@pytest.fixture(scope="class")
def new_actual_total_load():
    load = ActualTotalLoad(entity_created_at='2019-10-01 13:46:36.761013', entity_modified_at='2019-10-01 '
                                                                                              '13:46:36.761013',
                           action_task_id=312126, status= 'NaN', year= 2018, month= 1, day= 4, date_time='2018-01-04 '
                                                                                                         '05:30:00',
                           area_name='DE-AT-LU', update_time='2018-04-01 04:01:28', total_load_value=67928.13,
                           area_type_code_id=2, map_code_id=7, area_code_id=55448, resolution_code_id=1,
                           row_hash='B82C7EFD-60F2F573-C96FC45E-D1C6BDCF-90931B6E-F597F424-ED2AB8DC-417B2132-1DCDCEFE'
                                    '-7AA96D2A-994E7E4A-48B611ED-148827AF-B30EF809-95994DB3-033F3720')
    return load


@pytest.fixture(scope="class", params=['postgresql+psycopg2://postgres:evanescence.@localhost/testing'], autouse=True)
def client(request):
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = request.param
    app.config['SECRET_KEY'] = '35236712dsgajg1365sg125'
    app.config['SQLALCHEMY_ECHO'] = False
    with app.app_context():
        db.create_all()
        yield app.test_client()
        reset()
        db.session.remove()
