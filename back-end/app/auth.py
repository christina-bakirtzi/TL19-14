import pandas as pd
from flask import make_response, Response
from flask import Blueprint, jsonify
from flask import request
from werkzeug.security import check_password_hash
import jwt
from functools import wraps
from .models import User, db, ActualTotalLoad, AggregatedGenerationPerType, DayAheadTotalLoadForecast
from .config import Config
import datetime

bp = Blueprint("auth", __name__, url_prefix="/energy/api")


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-OBSERVATORY-AUTH' in request.headers:
            token = request.headers['X-OBSERVATORY-AUTH']

        if not token:
            return make_response('Not authorized', 401)
        try:
        # if True:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
            current_user = User.query.filter_by(id=data['id']).first()
            if current_user.token == token:
                if current_user.quotas >= 1 and (current_user.is_admin is False):
                    current_user.quotas = current_user.quotas - 1
                    db.session.commit()
                    return f(current_user, *args, **kwargs)
                else:
                    if current_user.is_admin is True:
                        return f(current_user, *args, **kwargs)
                    else:
                        return make_response('Out of quota', 402)
            else:
                if current_user.token is None:
                    return make_response('User has been logged out (Not authorized)', 401)
                else:
                    return make_response('Token is invalid (Not authorized)', 401)
        except:
            return make_response('Not authorized', 401)

    return decorated


@bp.route('/Admin/users', methods=['POST'])
@requires_auth
def register(current_user):
    data = request.form
    if not current_user.is_admin:
        return make_response('User is not an admin (Not authorized)', 401)
        # return jsonify({'message': 'Can\'t complete that,not an admin!'}), 401

    if not data['username'] or not data['email'] or not data['quota'] or not data['password']:
        return make_response('A field is missing', 400)
    else:
        unique = User.query.filter_by(username=data['username']).first()
        if not unique is None:
            return make_response('Username already exists', 400)
        unique = User.query.filter_by(email=data['email']).first()
        if not unique is None:
            return make_response('E-mail already exists', 400)
        new_user = User(is_admin=False, username=data['username'], email=data['email'], quotas=data['quota'])
        new_user.hash_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'new user created'})


@bp.route('/Admin/users/<user_username>', methods=['GET', 'PUT'])
@requires_auth
def show(current_user, user_username):
    if not current_user.is_admin:
        return make_response('User is not an admin (Not authorized)', 401)
        # return jsonify({'message': 'cant complete that,not an admin'})
    if request.method == 'GET':
        user = User.query.filter_by(username=user_username).first()
        if not user:
            return make_response('There is no user with this username', 400)
        result = {'username': user.username, 'email': user.email, 'quota': user.quotas}
        return jsonify({"message": result})
    if request.method == 'PUT':
        data = request.form
        user = User.query.filter_by(username=user_username).first()
        if not user:
            return make_response('There is no user with this username', 400)
        if 'email' in data:
            unique = User.query.filter_by(email=data['email']).first()
            if not unique is None:
                return make_response('E-mail already exists', 400)
            user.email = data['email']
        if 'quota' in data:
            user.quotas = data['quota']
        if 'password' in data:
            user.hash_password(data['password'])
        db.session.commit()
        return jsonify({"message": 'Fields have been changed'})


@bp.route('/Login', methods=['POST'])
def login():
    auth = request.form.to_dict()
    if not auth or not auth['username'] or not auth['password']:
        return make_response('Could not verify', 401)
    user = User.query.filter_by(username=auth['username']).first()
    if not user:
        return make_response('Could not verify', 401)
    if check_password_hash(user.password_hash, auth['password']):
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)},
            Config.SECRET_KEY)
        user.update_token(token.decode('UTF-8'))
        db.session.commit()
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401)


@bp.route('/Logout', methods=['POST'])
@requires_auth
def logout(current_user):
    current_user.token = None
    db.session.commit()
    return make_response('', 200)


@bp.route('/Admin/<table>', methods=['POST'])
@requires_auth
def importcsv(current_user, table):
    if not current_user.is_admin:
        return make_response('User is not an admin (Not authorized)', 401)
        # return jsonify({'message': 'cant complete that,not an admin'})
    file = request.files['file']
    if file is None:
        return make_response('There is no file', 400)
        # return jsonify({"error": "Bad request"}), 400
    try:
        reader = pd.read_csv(file, ';')
    except:
        return make_response('Couldn\'t read file', 400)
        # return jsonify({"error": "Bad request"}), 400
    counter = 0
    totalRecordsInFile = reader.shape[0]
    if table == 'ActualTotalLoad':
        recordsindatabase = ActualTotalLoad.query.count()
    elif table == 'DayAheadTotalLoadForecast':
        recordsindatabase = DayAheadTotalLoadForecast.query.count()
    elif table == 'AggregatedGenerationPerType':
        recordsindatabase = AggregatedGenerationPerType.query.count()
    else:
        return make_response('There is no table with this name', 400)
    for row in reader.itertuples():
        try:
            id = getattr(row, 'Id')
            entity_created_at = getattr(row, 'EntityCreatedAt')
            entity_modified_at = getattr(row, 'EntityModifiedAt')
            action_task_id = getattr(row, 'ActionTaskID')
            status = getattr(row, 'Status')
            year = getattr(row, 'Year')
            month = getattr(row, 'Month')
            day = getattr(row, 'Day')
            date_time = getattr(row, 'DateTime')
            area_name = getattr(row, 'AreaName')
            update_time = getattr(row, 'UpdateTime')
            row_hash = getattr(row, 'RowHash')

            if table == 'ActualTotalLoad':
                unique = ActualTotalLoad.query.filter_by(id=id).first()
                if not unique is None:
                    continue
                total_load_value = getattr(row, 'TotalLoadValue')
                area_type_code_id = getattr(row, 'AreaTypeCodeId')
                map_code_id = getattr(row, 'MapCodeId')
                area_code_id = getattr(row, 'AreaCodeId')
                resolution_code_id = getattr(row, 'ResolutionCodeId')
                query = ActualTotalLoad(id=id, entity_created_at=entity_created_at,
                                        entity_modified_at=entity_modified_at,
                                        action_task_id=action_task_id, status=status, year=year, month=month,
                                        day=day,
                                        date_time=date_time, area_name=area_name, update_time=update_time,
                                        total_load_value=total_load_value, area_type_code_id=area_type_code_id,
                                        map_code_id=map_code_id, resolution_code_id=resolution_code_id,
                                        row_hash=row_hash, area_code_id=area_code_id)
                db.session.add(query)
                db.session.commit()

            if table == 'DayAheadTotalLoadForecast':
                unique = DayAheadTotalLoadForecast.query.filter_by(id=id).first()
                if not unique is None:
                    continue
                total_load_value = getattr(row, 'TotalLoadValue')
                area_type_code_id = getattr(row, 'AreaTypeCodeId')
                resolution_code_id = getattr(row, 'ResolutionCodeId')
                map_code_id = getattr(row, 'MapCodeId')
                area_code_id = getattr(row, 'AreaCodeId')
                query = DayAheadTotalLoadForecast(id=id, entity_created_at=entity_created_at,
                                                  entity_modified_at=entity_modified_at,
                                                  action_task_id=action_task_id, status=status, year=year,
                                                  month=month,
                                                  day=day,
                                                  date_time=date_time, area_name=area_name, update_time=update_time,
                                                  total_load_value=total_load_value,
                                                  area_type_code_id=area_type_code_id,
                                                  map_code_id=map_code_id, resolution_code_id=resolution_code_id,
                                                  row_hash=row_hash, area_code_id=area_code_id)
                db.session.add(query)
                db.session.commit()

            if table == 'AggregatedGenerationPerType':
                unique = AggregatedGenerationPerType.query.filter_by(id=id).first()
                if not unique is None:
                    continue
                actual_generation_output = getattr(row, 'ActualGenerationOutput')
                actual_consuption = getattr(row, 'ActualConsuption')
                area_type_code_id = getattr(row, 'AreaTypeCodeId')
                production_type_id = getattr(row, 'ProductionTypeId')
                resolution_code_id = getattr(row, 'ResolutionCodeId')
                map_code_id = getattr(row, 'MapCodeId')
                area_code_id = getattr(row, 'AreaCodeId')
                query = AggregatedGenerationPerType(id=id, entity_created_at=entity_created_at,
                                                    entity_modified_at=entity_modified_at,
                                                    action_task_id=action_task_id, status=status, year=year,
                                                    month=month,
                                                    day=day,
                                                    date_time=date_time, area_name=area_name,
                                                    update_time=update_time,
                                                    actual_generation_output=actual_generation_output,
                                                    actual_consuption=actual_consuption,
                                                    area_type_code_id=area_type_code_id,
                                                    production_type_id=production_type_id,
                                                    map_code_id=map_code_id, resolution_code_id=resolution_code_id,
                                                    row_hash=row_hash, area_code_id=area_code_id)
                db.session.add(query)
                db.session.commit()
            counter = counter + 1
        except:
            continue
    return jsonify({"totalRecordsInFile": totalRecordsInFile, "totalRecordsImported": counter,
                    "totalRecordsInDatabase": recordsindatabase + counter})


@bp.route('/HealthCheck', methods=['GET'])
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'OK'})
    except:
        return make_response('There is no connection with database', 400)
        # return jsonify({'status': 'no connection with database'})


@bp.route('/Reset', methods=['POST'])
def reset():
    try:
        db.session.query(User).delete()
        db.session.query(AggregatedGenerationPerType).delete()
        db.session.query(ActualTotalLoad).delete()
        db.session.query(DayAheadTotalLoadForecast).delete()
        db.session.commit()
        admin = User(username='admin', is_admin=True, email='admin@gmail.com', quotas=-1)
        admin.hash_password('321nimda')
        db.session.add(admin)
        db.session.commit()
        return jsonify({'status': 'OK'})
    except:
        db.session.rollback()
        return make_response('Couldn\'t clear database', 400)
        # return jsonify({'status': 'couldn\'t clear database'})
