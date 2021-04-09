from flask import Blueprint, jsonify, Response, request,json
from .models import AggregatedGenerationPerType, ResolutionCode, AreaTypeCode, MapCode, ProdutionType
import datetime
from .auth import requires_auth
from .jsontocsv import json2csv
from flask import make_response

bp = Blueprint("aggregatedGenerationPerType", __name__, url_prefix="/energy/api/AggregatedGenerationPerType")

base_csv_first_row = ["Source", "Dataset", "AreaName", "AreaTypeCode", "MapCode", "ResolutionCode", "Year", "Month"]


@bp.route('/<AreaName>/<production_type>/<Resolution>/date/<date_str>', methods=['GET'])
@requires_auth
def aggregated_generation_per_type_date(_, AreaName, production_type, Resolution, date_str):
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

    if not production_type == 'AllTypes':
        prod = ProdutionType.query.filter_by(production_type_text=production_type).first()

        if not prod:
            return make_response('The Production Type is invalid', 403)

        st = AggregatedGenerationPerType.query.filter_by(area_name=AreaName, production_type_id=prod.id,
                                                         resolution_code_id=res_id, day=day, month=month,
                                                         year=year).order_by(
            AggregatedGenerationPerType.date_time).all()
        if not st:
            return make_response('There is no data with these attributes', 403)
        records = []
        first = True
        for record in st:
            if first:
                area_type_code = AreaTypeCode.query.filter_by(id=record.area_type_code_id).first()
                if not area_type_code:
                    return make_response('The Area Type Code is invalid', 403)

                map_code = MapCode.query.filter_by(id=record.map_code_id).first()
                if not map_code:
                    return make_response('The Map Code is invalid', 403)
                first = False

            extra = {"Source": "entso-e", "Dataset": "AggregatedGenerationPerType", "AreaName": str(AreaName),
                     "AreaTypeCode": str(area_type_code.area_type_code_text), "MapCode": str(map_code.map_code_text),
                     "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month), "Day": str(day),
                     "DateTimeUTC": str(record.date_time), "ProductionType": str(production_type),
                     "ActualGenerationOutputValue": str(record.actual_generation_output),
                     "UpdateTimeUTC": str(record.update_time)}
            records.append(extra)

        if csvbool:
            csv_response = json2csv(records,
                                    base_csv_first_row + ["Day", "DateTimeUTC", "ProductionType",
                                                          "ActualGenerationOutputValue",
                                                          "UpdateTimeUTC"])
            return Response(csv_response, mimetype='text/csv')
        else:
            return Response(json.dumps(records, sort_keys=False), mimetype='application/json')

    elif production_type == 'AllTypes':
        typesofproduction = ProdutionType.query.with_entities(ProdutionType.id,
                                                              ProdutionType.production_type_text).all()

        records = []
        for prod in typesofproduction:

            st = AggregatedGenerationPerType.query.filter_by(area_name=AreaName, production_type_id=prod.id,
                                                             resolution_code_id=res_id, day=day, month=month,
                                                             year=year).order_by(
                AggregatedGenerationPerType.date_time).all()

            first = True
            for record in st:
                if first:
                    area_type_code = AreaTypeCode.query.filter_by(id=record.area_type_code_id).first()
                    if not area_type_code:
                        return make_response('The Area Type Code is invalid', 403)

                    map_code = MapCode.query.filter_by(id=record.map_code_id).first()
                    if not map_code:
                        return make_response('The Map Code is invalid', 403)
                    first = False

                extra = {"Source": "entso-e", "Dataset": "AggregatedGenerationPerType", "AreaName": str(AreaName),
                         "AreaTypeCode": str(area_type_code.area_type_code_text),
                         "MapCode": str(map_code.map_code_text),
                         "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month), "Day": str(day),
                         "DateTimeUTC": str(record.date_time), "ProductionType": str(prod.production_type_text),
                         "ActualGenerationOutputValue": str(record.actual_generation_output),
                         "UpdateTimeUTC": str(record.update_time)}
                records.append(extra)
        if not records:
            return make_response('There is no data with these attributes', 403)
        if csvbool:
            csv_response = json2csv(records,
                                    base_csv_first_row + ["Day", "DateTimeUTC", "ProductionType",
                                                          "ActualGenerationOutputValue",
                                                          "UpdateTimeUTC"])
            return Response(csv_response, mimetype='text/csv')
        else:
            return Response(json.dumps(records, sort_keys=False), mimetype='application/json')


@bp.route('/<AreaName>/<production_type>/<Resolution>/month/<date_str>', methods=['GET'])
@requires_auth
def aggregated_generation_per_type_month(_, AreaName, production_type, Resolution, date_str):
    format = request.args.get('format')
    csvbool = False
    if format == 'csv':
        csvbool = True

    try:
        date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m')
    except:
        return make_response('Not valid date format (YYYY-MM)', 400)
    month = date_time_obj.month
    year = date_time_obj.year
    res = ResolutionCode.query.filter_by(resolution_code_text=Resolution).first()
    if not res:
        return make_response('The Resolution Code is invalid', 403)
    res_id = res.id

    if not production_type == 'AllTypes':
        prod = ProdutionType.query.filter_by(production_type_text=production_type).first()

        if not prod:
            return make_response('The Production Type is invalid', 403)

        st = AggregatedGenerationPerType.query.filter_by(area_name=AreaName, production_type_id=prod.id,
                                                         resolution_code_id=res_id, month=month,
                                                         year=year).order_by(
            AggregatedGenerationPerType.date_time).all()
        if not st:
            return make_response('There is no data with these attributes', 403)
        days = [0] * 31

        first = True
        for record in st:
            for day in range(1, 32):
                if record.day == day:
                    days[day - 1] = days[day - 1] + record.actual_generation_output
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
                extra = {"Source": "entso-e", "Dataset": "AggregatedGenerationPerType",
                         "AreaName": str(record.area_name),
                         "AreaTypeCode": str(area_type_code.area_type_code_text),
                         "MapCode": str(map_code.map_code_text),
                         "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month), "Day": str(day + 1),
                         "ProductionType": str(prod.production_type_text),
                         "ActualGenerationOutputByDayValue": str(days[day])}
                records.append(extra)
        if csvbool:
            csv_response = json2csv(records,
                                    base_csv_first_row + ["Day", "ProductionType",
                                                          "ActualGenerationOutputByDayValue"])
            return Response(csv_response, mimetype='text/csv')
        else:
            return Response(json.dumps(records, sort_keys=False), mimetype='application/json')

    elif production_type == 'AllTypes':

        typesofproduction = ProdutionType.query.with_entities(ProdutionType.id,
                                                              ProdutionType.production_type_text).all()

        records = []
        for prod in typesofproduction:

            st = AggregatedGenerationPerType.query.filter_by(area_name=AreaName, production_type_id=prod.id,
                                                             resolution_code_id=res_id, month=month,
                                                             year=year).order_by(
                AggregatedGenerationPerType.date_time).all()
            days = [0] * 31

            first = True
            for record in st:
                for day in range(1, 32):
                    if record.day == day:
                        days[day - 1] = days[day - 1] + record.actual_generation_output
                        break
                if first:
                    area_type_code = AreaTypeCode.query.filter_by(id=record.area_type_code_id).first()
                    if not area_type_code:
                        return make_response('The Area Type Code is invalid', 403)
                    map_code = MapCode.query.filter_by(id=record.map_code_id).first()
                    if not map_code:
                        return make_response('The Map Code is invalid', 403)
                    first = False

            for day in range(0, 31):
                if not days[day] == 0:
                    extra = {"Source": "entso-e", "Dataset": "AggregatedGenerationPerType",
                             "AreaName": str(record.area_name),
                             "AreaTypeCode": str(area_type_code.area_type_code_text),
                             "MapCode": str(map_code.map_code_text),
                             "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month),
                             "Day": str(day + 1), "ProductionType": str(prod.production_type_text),
                             "ActualGenerationOutputByDayValue": str(days[day])}
                    records.append(extra)
        if not records:
            return make_response('There is no data with these attributes', 403)
        if csvbool:
            csv_response = json2csv(records,
                                    base_csv_first_row + ["Day", "ProductionType",
                                                          "ActualGenerationOutputByDayValue"])
            return Response(csv_response, mimetype='text/csv')
        else:
            return Response(json.dumps(records, sort_keys=False), mimetype='application/json')


@bp.route('/<AreaName>/<production_type>/<Resolution>/year/<date_str>', methods=['GET'])
@requires_auth
def aggregated_generation_per_type_year(_, AreaName, production_type, Resolution, date_str):
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
        # return jsonify({'message': 'The Resolution Code is invalid'}), 403
    res_id = res.id

    if not production_type == 'AllTypes':
        prod = ProdutionType.query.filter_by(production_type_text=production_type).first()
        if not prod:
            return make_response('The Production Type is invalid', 403)
            # return jsonify({'message': 'The Production type is invalid'}), 403

        st = AggregatedGenerationPerType.query.filter_by(area_name=AreaName, production_type_id=prod.id,
                                                         resolution_code_id=res_id, year=year).order_by(
            AggregatedGenerationPerType.date_time).all()
        if not st:
            return make_response('There is no data with these attributes', 403)

        months = [0] * 12

        first = True
        for record in st:
            for month in range(1, 13):
                if record.month == month:
                    months[month - 1] = months[month - 1] + record.actual_generation_output
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
                extra = {"Source": "entso-e", "Dataset": "AggregatedGenerationPerType",
                         "AreaName": str(record.area_name),
                         "AreaTypeCode": str(area_type_code.area_type_code_text),
                         "MapCode": str(map_code.map_code_text),
                         "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month + 1),
                         "ProductionType": str(prod.production_type_text),
                         "ActualGenerationOutputByMonthValue": str(months[month])}
                records.append(extra)
        if csvbool:
            csv_response = json2csv(records,
                                    base_csv_first_row + ["ProductionType", "ActualGenerationOutputByMonthValue"])
            return Response(csv_response, mimetype='text/csv')
        else:
            return Response(json.dumps(records, sort_keys=False), mimetype='application/json')

    elif production_type == 'AllTypes':

        typesofproduction = ProdutionType.query.with_entities(ProdutionType.id,
                                                              ProdutionType.production_type_text).all()
        records = []
        for prod in typesofproduction:
            st = AggregatedGenerationPerType.query.filter_by(area_name=AreaName, production_type_id=prod.id,
                                                             resolution_code_id=res_id, year=year).order_by(
                                                            AggregatedGenerationPerType.date_time).all()
            months = [0] * 12

            first = True
            for record in st:
                for month in range(1, 13):
                    if record.month == month:
                        months[month - 1] = months[month - 1] + record.actual_generation_output
                        break
                if first:
                    area_type_code = AreaTypeCode.query.filter_by(id=record.area_type_code_id).first()
                    if not area_type_code:
                        return make_response('The Area Type Code is invalid', 403)
                    map_code = MapCode.query.filter_by(id=record.map_code_id).first()
                    if not map_code:
                        return make_response('The Map Code is invalid', 403)
                    first = False

            for month in range(0, 12):
                if not months[month] == 0:
                    extra = {"Source": "entso-e", "Dataset": "AggregatedGenerationPerType",
                             "AreaName": str(record.area_name),
                             "AreaTypeCode": str(area_type_code.area_type_code_text),
                             "MapCode": str(map_code.map_code_text),
                             "ResolutionCode": str(Resolution), "Year": str(year), "Month": str(month + 1),
                             "ProductionType": str(prod.production_type_text),
                             "ActualGenerationOutputByMonthValue": str(months[month])}
                    records.append(extra)
        if not records:
            return make_response('There is no data with these attributes', 403)
        if csvbool:
            csv_response = json2csv(records,
                                    base_csv_first_row + ["ProductionType", "ActualGenerationOutputByMonthValue"])
            return Response(csv_response, mimetype='text/csv')
        else:
            return Response(json.dumps(records, sort_keys=False), mimetype='application/json')
