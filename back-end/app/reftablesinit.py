import math
import pandas as pd
from flask import Blueprint, jsonify
from flask import request

from .models import db, AreaTypeCode, MapCode, ResolutionCode , ProdutionType ,AllocatedEICDetail

bp = Blueprint("reftablesinit", __name__, url_prefix="/energy/api")


@bp.route('/init/<file_name>', methods=['POST'])
def importcsvInit(file_name):
    # if not current_user.is_admin:
    #     return jsonify({'message': 'cant complete that,not an admin'})

    file = request.files['file']
    reader = pd.read_csv(file, ';')
    if file_name == 'AreaTypeCode':
        for row in reader.itertuples():
            id = getattr(row, 'Id')
            entity_created_at = getattr(row, 'EntityCreatedAt')
            entity_modified_at = getattr(row, 'EntityModifiedAt')
            area_type_code_text = getattr(row, 'AreaTypeCodeText')
            area_type_code_note = getattr(row, 'AreaTypeCodeNote')
            query = AreaTypeCode(id=id, entity_created_at=entity_created_at, entity_modified_at=entity_modified_at,
                                 area_type_code_text=area_type_code_text, area_type_code_note=area_type_code_note)
            db.session.add(query)
        db.session.commit()

        return jsonify({"message": 'Table AreaType imported '})
    if file_name == 'MapCode':
        for row in reader.itertuples():
            id = getattr(row, 'Id')
            entity_created_at = getattr(row, 'EntityCreatedAt')
            entity_modified_at = getattr(row, 'EntityModifiedAt')
            map_code_text = getattr(row, 'MapCodeText')
            map_code_note = getattr(row, 'MapCodeNote')
            query = MapCode(id=id, entity_created_at=entity_created_at, entity_modified_at=entity_modified_at,
                            map_code_text=map_code_text, map_code_note=map_code_note)
            db.session.add(query)
        db.session.commit()

        return jsonify({"message": 'Table MapCode imported '})
    if file_name == 'ResolutionCode':
        for row in reader.itertuples():
            id = getattr(row, 'Id')
            entity_created_at = getattr(row, 'EntityCreatedAt')
            entity_modified_at = getattr(row, 'EntityModifiedAt')
            resolution_code_text = getattr(row, 'ResolutionCodeText')
            resolution_code_note = getattr(row, 'ResolutionCodeNote')
            query = ResolutionCode(id=id, entity_created_at=entity_created_at, entity_modified_at=entity_modified_at,
                                   resolution_code_text=resolution_code_text, resolution_code_note=resolution_code_note)
            db.session.add(query)
        db.session.commit()

        return jsonify({"message": 'Table ResolutionCode imported '})

    if file_name == 'ProductionType':
        for row in reader.itertuples():
            id = getattr(row, 'Id')
            entity_created_at = getattr(row, 'EntityCreatedAt')
            entity_modified_at = getattr(row, 'EntityModifiedAt')
            production_type_text = getattr(row, 'ProductionTypeText')
            production_type_note = getattr(row, 'ProductionTypeNote')
            query = ProdutionType(id=id, entity_created_at=entity_created_at, entity_modified_at=entity_modified_at,
                                   production_type_text=production_type_text, production_type_note=production_type_note)
            db.session.add(query)
        db.session.commit()

        return jsonify({"message": 'Table Production imported '})

    if file_name == 'AllocatedEICDetail':
        for row in reader.itertuples():
            id = getattr(row, 'Id')
            # print(id)
            entity_created_at = getattr(row, 'EntityCreatedAt')
            entity_modified_at = getattr(row, 'EntityModifiedAt')
            mrid = getattr(row, 'MRID')
            doc_status_value = getattr(row, 'DocStatusValue')
            attribute_instance_component = getattr(row, 'AttributeInstanceComponent')
            long_names = getattr(row, 'LongNames')
            display_names = getattr(row, 'DisplayNames')
            last_request_date_and_or_time = getattr(row, 'LastRequestDateAndOrTime')
            if type(last_request_date_and_or_time) is float:
                if math.isnan(last_request_date_and_or_time):
                    last_request_date_and_or_time = None
            deactivate_request_date_and_or_time = getattr(row, 'DeactivateRequestDateAndOrTime')
            if type(deactivate_request_date_and_or_time) is float:
                if math.isnan(deactivate_request_date_and_or_time):
                    deactivate_request_date_and_or_time = None
            market_participant_street_address_country = getattr(row, 'MarketParticipantStreetAddressCountry')
            # market_participant_acer_code = getattr(row, 'MarketParticipantACERCode')
            market_participant_vat_code = getattr(row, 'MarketParticipantVATcode')
            description = getattr(row, 'Description')
            eic_parent_market_document_mrid = getattr(row, 'EICParentMarketDocumentMRID')
            eic_responsible_market_participant_mrid = getattr(row, 'ELCResponsibleMarketParticipantMRID')
            is_deleted = getattr(row, 'IsDeleted')
            query = AllocatedEICDetail(id=id, entity_created_at=entity_created_at,
                                       entity_modified_at=entity_modified_at,
                                       mrid=mrid, doc_status_value=doc_status_value,
                                       attribute_instance_component=attribute_instance_component, long_names=long_names,
                                       display_names=display_names,
                                       last_request_date_and_or_time=last_request_date_and_or_time,
                                       deactivate_request_date_and_or_time=deactivate_request_date_and_or_time,
                                       market_participant_street_address_country=market_participant_street_address_country,
                                       market_participant_vat_code=market_participant_vat_code, description=description,
                                       eic_parent_market_document_mrid=eic_parent_market_document_mrid,
                                       eic_responsible_market_participant_mrid=eic_responsible_market_participant_mrid,
                                       is_deleted=is_deleted)
            db.session.add(query)
            db.session.commit()

        return jsonify({"message": 'Table AllocatedEICDetail imported '})


