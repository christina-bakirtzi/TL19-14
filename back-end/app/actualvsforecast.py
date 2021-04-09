from flask import Blueprint, Response, json
from flask import request
from .models import ActualTotalLoad, DayAheadTotalLoadForecast, ResolutionCode, AreaTypeCode, MapCode
import datetime
from .auth import requires_auth
from .jsontocsv import json2csv
from flask import make_response

base_csv_first_row = ["Source", "Dataset", "AreaName", "AreaTypeCode", "MapCode", "ResolutionCode", "Year", "Month"]

bp = Blueprint("actualvsforecast", __name__, url_prefix="/energy/api/ActualvsForecast")


@bp.route('/<AreaName>/<Resolution>/date/<date_str>', methods=['GET'])
@requires_auth
def actual_vs_forecast_date(_, AreaName, Resolution, date_str):
    format = request.args.get('format')
    csvbool = False
    if format == 'csv':
        csvbool = True
    try:
        date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except:
        return make_response('Not valid date format (YYYY-MM-DD)', 400)
    day = date_time_obj.day
    month = date_time_obj.month
    year = date_time_obj.year

    res = ResolutionCode.query.filter_by(resolution_code_text=Resolution).first()
    if not res:
        return make_response('The Resolution Code is invalid', 403)
    res_id = res.id
    st1 = ActualTotalLoad.query.filter_by(area_name=AreaName, resolution_code_id=res_id, day=day, month=month,
                                          year=year).order_by(ActualTotalLoad.date_time).all()
    if not st1:
        return make_response('There is no data with these attributes', 403)
    st2 = DayAheadTotalLoadForecast.query.filter_by(area_name=AreaName, resolution_code_id=res_id, day=day, month=month,
                                                    year=year).order_by(DayAheadTotalLoadForecast.date_time).all()
    if not st2:
        return make_response('There is no data with these attributes', 403)
    records = []
    first = True
    for record1 in st1:
        for record2 in st2:
            if first:
                area_type_code = AreaTypeCode.query.filter_by(id=record1.area_type_code_id).first()
                if not area_type_code:
                    return make_response('The Area Type Code is invalid', 403)
                map_code = MapCode.query.filter_by(id=record1.map_code_id).first()
                if not map_code:
                    return make_response('The Map Code is invalid', 403)
                first = False
            if record1.date_time == record2.date_time and record1.area_name == record2.area_name and record1.resolution_code_id == record2.resolution_code_id and record1.day == record2.day and record1.month == record2.month and record1.year == record2.year:
                extra = {"Source": "entso-e", "Dataset": "ActualvsForecastedTotalLoad",
                         "AreaName": str(record1.area_name),
                         "AreaTypeCode": str(area_type_code.area_type_code_text),
                         "MapCode": str(map_code.map_code_text),
                         "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month), "Day": str(day),
                         "DateTimeUTC": str(record1.date_time),
                         "DayAheadTotalLoadForecastValue": str(record2.total_load_value),
                         "ActualTotalLoadValue": str(record1.total_load_value)}
                records.append(extra)
                break
    if csvbool:
        csv_response = json2csv(records,
                                base_csv_first_row + ["Day", "DateTimeUTC", "DayAheadTotalLoadForecastValue",
                                                      "ActualTotalLoadValue"])
        return Response(csv_response, mimetype='text/csv')
    else:
        return Response(json.dumps(records, sort_keys=False), mimetype='application/json')


@bp.route('/<AreaName>/<Resolution>/month/<date_str>', methods=['GET'])
@requires_auth
def actual_vs_forecast_month(_, AreaName, Resolution, date_str):
    format = request.args.get('format')
    csvbool = False
    if format == 'csv':
        csvbool = True
    try:
        date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m')
    except:
        return make_response('Not valid date format (YYYY-MM)', 400)
    year = date_time_obj.year
    month = date_time_obj.month
    res = ResolutionCode.query.filter_by(resolution_code_text=Resolution).first()
    if not res:
        return make_response('The Resolution Code is invalid', 403)
    res_id = res.id
    st1 = ActualTotalLoad.query.filter_by(area_name=AreaName, resolution_code_id=res_id, year=year,
                                          month=month).order_by(ActualTotalLoad.date_time).all()
    if not st1:
        return make_response('There is no data with these attributes', 403)
    st2 = DayAheadTotalLoadForecast.query.filter_by(area_name=AreaName, resolution_code_id=res_id, year=year,
                                                    month=month).order_by(DayAheadTotalLoadForecast.date_time).all()
    if not st2:
        return make_response('There is no data with these attributes', 403)
    days1 = [0] * 31
    days2 = [0] * 31
    first = True
    for record1 in st1:
        for day in range(1, 32):
            if record1.day == day:
                days1[day - 1] = days1[day - 1] + record1.total_load_value
                break
        if first:
            area_type_code = AreaTypeCode.query.filter_by(id=record1.area_type_code_id).first()
            if not area_type_code:
                return make_response('The Area Type Code is invalid', 403)
            map_code = MapCode.query.filter_by(id=record1.map_code_id).first()
            if not map_code:
                return make_response('The Map Code is invalid', 403)
            first = False
    for record2 in st2:
        for day in range(1, 32):
            if record2.day == day:
                days2[day - 1] = days2[day - 1] + record2.total_load_value
                break

    records = []
    for day in range(0, 31):
        if not days1[day] == 0 and not days2[day] == 0:
            extra = {"Source": "entso-e", "Dataset": "ActualvsForecastedTotalLoad", "AreaName": str(AreaName),
                     "AreaTypeCode": str(area_type_code.area_type_code_text), "MapCode": str(map_code.map_code_text),
                     "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month), "Day": str(day + 1),
                     "DayAheadTotalLoadForecastByDayValue": str(days2[day]),
                     "ActualTotalLoadByDayValue": str(days1[day])}
            records.append(extra)
    if csvbool:
        csv_response = json2csv(records,
                                base_csv_first_row + ["Day", "DayAheadTotalLoadForecastByDayValue",
                                                      "ActualTotalLoadByDayValue"])
        return Response(csv_response, mimetype='text/csv')
    else:
        return Response(json.dumps(records, sort_keys=False), mimetype='application/json')


@bp.route('/<AreaName>/<Resolution>/year/<date_str>', methods=['GET'])
@requires_auth
def actual_vs_forecast_year(_, AreaName, Resolution, date_str):
    format = request.args.get('format')
    csvbool = False
    if format == 'csv':
        csvbool = True

    try:
        date_time_obj = datetime.datetime.strptime(date_str, '%Y')
    except:
        return make_response('Not valid date format (YYYY)', 400)
    year = date_time_obj.year
    res = ResolutionCode.query.filter_by(resolution_code_text=Resolution).first()
    if not res:
        return make_response('The Resolution Code is invalid', 403)
    res_id = res.id
    st1 = ActualTotalLoad.query.filter_by(area_name=AreaName, resolution_code_id=res_id, year=year).order_by(
        ActualTotalLoad.date_time).all()
    if not st1:
        return make_response('There is no data with these attributes', 403)
    st2 = DayAheadTotalLoadForecast.query.filter_by(area_name=AreaName, resolution_code_id=res_id, year=year).order_by(
        DayAheadTotalLoadForecast.date_time).all()
    if not st2:
        return make_response('There is no data with these attributes', 403)
    months1 = [0] * 12
    months2 = [0] * 12
    first = True
    for record1 in st1:
        for month in range(1, 13):
            if record1.month == month:
                months1[month - 1] = months1[month - 1] + record1.total_load_value
                break
        if first:
            area_type_code = AreaTypeCode.query.filter_by(id=record1.area_type_code_id).first()
            if not area_type_code:
                return make_response('The Area Type Code is invalid', 403)
            map_code = MapCode.query.filter_by(id=record1.map_code_id).first()
            if not map_code:
                return make_response('The Map Code is invalid', 403)
            first = False
    for record2 in st2:
        for month in range(1, 13):
            if record2.month == month:
                months2[month - 1] = months2[month - 1] + record2.total_load_value
                break

    records = []
    for month in range(0, 12):
        if not months1[month] == 0 and not months2[month] == 0:
            extra = {"Source": "entso-e", "Dataset": "ActualvsForecastedTotalLoad", "AreaName": str(AreaName),
                     "AreaTypeCode": str(area_type_code.area_type_code_text), "MapCode": str(map_code.map_code_text),
                     "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month + 1),
                     "DayAheadTotalLoadForecastByMonthValue": str(months2[month]),
                     "ActualTotalLoadByMonthValue": str(months1[month])}
            records.append(extra)

    if csvbool:
        csv_response = json2csv(records,
                                base_csv_first_row + ["DayAheadTotalLoadForecastByMonthValue",
                                                      "ActualTotalLoadByMonthValue"])
        return Response(csv_response, mimetype='text/csv')
    else:
        return Response(json.dumps(records, sort_keys=False), mimetype='application/json')
