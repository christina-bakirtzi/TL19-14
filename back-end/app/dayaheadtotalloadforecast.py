from flask import Blueprint, jsonify, Response, request,json
from .models import DayAheadTotalLoadForecast, ResolutionCode, AreaTypeCode, MapCode
import datetime
from .auth import requires_auth
from .jsontocsv import json2csv
from flask import make_response
bp = Blueprint("dayaheadtotalloadforecast", __name__, url_prefix="/energy/api/DayAheadTotalLoadForecast")

base_csv_first_row = ["Source", "Dataset", "AreaName", "AreaTypeCode", "MapCode", "ResolutionCode", "Year", "Month"]


@bp.route('/<AreaName>/<Resolution>/date/<date_str>', methods=['GET'])
@requires_auth
def day_ahead_total_load_forecast_date(_, AreaName, Resolution, date_str):
    format = request.args.get('format')
    csvbool = False
    if format == 'csv':
        csvbool = True
    try:
        date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        day = date_time_obj.day
        month = date_time_obj.month
        year = date_time_obj.year
    except:
        return make_response('Not valid date format (YYYY-MM-DD)', 400)
    res = ResolutionCode.query.filter_by(resolution_code_text=Resolution).first()
    if not res:
        return make_response('The Resolution Code is invalid', 403)
    res_id = res.id

    st = DayAheadTotalLoadForecast.query.filter_by(area_name=AreaName, resolution_code_id=res_id, day=day, month=month,
                                                   year=year).order_by(DayAheadTotalLoadForecast.date_time).all()
    if not st:
        return make_response('There is no data with these attributes', 403)
    records = []
    for record in st:
        area_type_code = AreaTypeCode.query.filter_by(id=record.area_type_code_id).first()
        if not area_type_code:
            return make_response('The Area Type Code is invalid', 403)
        map_code = MapCode.query.filter_by(id=record.map_code_id).first()
        if not map_code:
            return make_response('The Map Code is invalid', 403)
        extra = {"Source": "entso-e", "Dataset": "DayAheadTotalLoadForecast", "AreaName": str(record.area_name),
                 "AreaTypeCode": str(area_type_code.area_type_code_text), "MapCode": str(map_code.map_code_text),
                 "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month), "Day": str(day),
                 "DateTimeUTC": str(record.date_time), "DayAheadTotalLoadForecastValue": str(record.total_load_value),
                 "UpdateTimeUTC": str(record.update_time)}
        records.append(extra)

    if csvbool:
        csv_response = json2csv(records,
                                base_csv_first_row + ["Day", "DateTimeUTC", "DayAheadTotalLoadForecastValue",
                                                      "UpdateTimeUTC"])
        return Response(csv_response, mimetype='text/csv')
    else:
        return Response(json.dumps(records, sort_keys=False), mimetype='application/json')


@bp.route('/<AreaName>/<Resolution>/month/<date_str>', methods=['GET'])
@requires_auth
def day_ahead_total_load_forecast_month(_, AreaName, Resolution, date_str):
    format = request.args.get('format')
    csvbool = False
    if format == 'csv':
        csvbool = True
    try:
        date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m')
        month = date_time_obj.month
        year = date_time_obj.year
    except:
        return make_response('Not valid date format (YYYY-MM)', 400)
    res = ResolutionCode.query.filter_by(resolution_code_text=Resolution).first()
    if not res:
        return make_response('The Resolution Code is invalid', 403)
    res_id = res.id
    st = DayAheadTotalLoadForecast.query.filter_by(area_name=AreaName, resolution_code_id=res_id, month=month,
                                                   year=year).order_by(DayAheadTotalLoadForecast.date_time).all()
    if not st:
        return make_response('There is no data with these attributes', 403)
    days = [0] * 31

    first = True
    for record in st:
        for day in range(1, 32):
            if record.day == day:
                days[day - 1] = days[day - 1] + record.total_load_value
                break
        if first:
            area_type_code = AreaTypeCode.query.filter_by(id=record.area_type_code_id).first()
            if not area_type_code:
                return make_response('The Area Type Code is invalid', 403)
            map_code = MapCode.query.filter_by(id=record.map_code_id).first()
            if not map_code:
                return make_response('The Map Code is invalid', 403)
            first = False

    records = []
    for day in range(0, 31):
        if not days[day] == 0:
            extra = {"Source": "entso-e", "Dataset": "DayAheadTotalLoadForecast", "AreaName": str(record.area_name),
                     "AreaTypeCode": str(area_type_code.area_type_code_text), "MapCode": str(map_code.map_code_text),
                     "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month), "Day": str(day + 1),
                     "DayAheadTotalLoadForecastByDayValue": str(days[day])}
            records.append(extra)
    if csvbool:
        csv_response = json2csv(records,
                                base_csv_first_row + ["Day", "DayAheadTotalLoadForecastByDayValue"])
        return Response(csv_response, mimetype='text/csv')
    else:
        return Response(json.dumps(records, sort_keys=False), mimetype='application/json')


@bp.route('/<AreaName>/<Resolution>/year/<date_str>', methods=['GET'])
@requires_auth
def day_ahead_total_load_forecast_year(_, AreaName, Resolution, date_str):
    format = request.args.get('format')
    csvbool = False
    if format == 'csv':
        csvbool = True
    try:
        date_time_obj = datetime.datetime.strptime(date_str, '%Y')
        year = date_time_obj.year
    except:
        return make_response('Not valid date format (YYYY)', 400)
    res = ResolutionCode.query.filter_by(resolution_code_text=Resolution).first()
    if not res:
        return make_response('The Resolution Code is invalid', 403)
    res_id = res.id
    st = DayAheadTotalLoadForecast.query.filter_by(area_name=AreaName, resolution_code_id=res_id, year=year).order_by(
        DayAheadTotalLoadForecast.date_time).all()
    if not st:
        return make_response('There is no data with these attributes', 403)
    months = [0] * 12
    first = True
    for record in st:
        for month in range(1, 13):
            if record.month == month:
                months[month - 1] = months[month - 1] + record.total_load_value
                break
        if first:
            area_type_code = AreaTypeCode.query.filter_by(id=record.area_type_code_id).first()
            if not area_type_code:
                return make_response('The Area Type Code is invalid', 403)
            map_code = MapCode.query.filter_by(id=record.map_code_id).first()
            if not map_code:
                return make_response('The Map Code is invalid', 403)
            first = False
    records = []
    for month in range(0, 12):
        if not months[month] == 0:
            extra = {"Source": "entso-e", "Dataset": "DayAheadTotalLoadForecast", "AreaName": str(record.area_name),
                     "AreaTypeCode": str(area_type_code.area_type_code_text), "MapCode": str(map_code.map_code_text),
                     "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month + 1),
                     "DayAheadTotalLoadForecastByMonthValue": str(months[month])}
            records.append(extra)
    if csvbool:
        csv_response = json2csv(records,
                                base_csv_first_row + ["DayAheadTotalLoadForecastByMonthValue"])
        return Response(csv_response, mimetype='text/csv')
    else:
        return Response(json.dumps(records, sort_keys=False), mimetype='application/json')
