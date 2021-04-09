from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_marshmallow import Marshmallow

db = SQLAlchemy()


# ma = Marshmallow()


class User(db.Model):
    # __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    token = db.Column(db.String(256), default=None, unique=True)
    quotas = db.Column(db.Integer, nullable=False)

    def update_token(self, newToken):
        self.token = newToken

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# class UserSchema(ma.Schema):
#     class Meta:
#         model = User

class AreaTypeCode(db.Model):
    __tablename__ = 'areatypecode'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    area_type_code_text = db.Column(db.VARCHAR(length=255), nullable=True)
    area_type_code_note = db.Column(db.VARCHAR(length=255), nullable=True)


class MapCode(db.Model):
    __tablename__ = 'mapcode'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    map_code_text = db.Column(db.VARCHAR(length=255), nullable=False)
    map_code_note = db.Column(db.VARCHAR(length=255), nullable=True)


class ProdutionType(db.Model):
    __tablename__ = 'productiontype'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    production_type_text = db.Column(db.VARCHAR(length=255), nullable=False)
    production_type_note = db.Column(db.VARCHAR(length=255), nullable=True)


class AllocatedEICDetail(db.Model):
    __tablename__ = 'allocatedeicdetail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    mrid = db.Column(db.VARCHAR(length=255), nullable=True)
    doc_status_value = db.Column(db.VARCHAR(length=255), nullable=True)
    attribute_instance_component = db.Column(db.VARCHAR(length=255), nullable=True)
    long_names = db.Column(db.VARCHAR(length=255), nullable=True)
    display_names = db.Column(db.VARCHAR(length=255), nullable=True)
    last_request_date_and_or_time = db.Column(db.DateTime, nullable=True)
    deactivate_request_date_and_or_time = db.Column(db.DateTime, nullable=True)
    market_participant_street_address_country = db.Column(db.VARCHAR(length=255), nullable=True)
    # market_participant_acer_code = db.Column(db.VARCHAR(length=255), nullable=True)
    market_participant_vat_code = db.Column(db.VARCHAR(length=255), nullable=True)
    description = db.Column(db.VARCHAR(length=1000), nullable=True)
    eic_parent_market_document_mrid = db.Column(db.VARCHAR(length=255), nullable=True)
    eic_responsible_market_participant_mrid = db.Column(db.VARCHAR(length=255), nullable=True)
    is_deleted = db.Column(db.VARCHAR(length=4))


class ResolutionCode(db.Model):
    __tablename__ = 'resolutioncode'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    resolution_code_text = db.Column(db.VARCHAR(length=255), nullable=False)
    resolution_code_note = db.Column(db.VARCHAR(length=255), nullable=True)


class ActualTotalLoad(db.Model):
    __tablename__ = 'actualtotalload'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    action_task_id = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.VARCHAR(length=4), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    area_name = db.Column(db.VARCHAR(length=200), nullable=True)
    update_time = db.Column(db.DateTime, nullable=False)
    total_load_value = db.Column(db.Numeric(24, 2), nullable=False)
    area_type_code_id = db.Column(db.Integer, db.ForeignKey('areatypecode.id', ondelete="CASCADE"), nullable=True)
    map_code_id = db.Column(db.Integer, db.ForeignKey('mapcode.id', ondelete="CASCADE"), nullable=True)
    area_code_id = db.Column(db.Integer, db.ForeignKey('allocatedeicdetail.id', ondelete="CASCADE"), nullable=False)
    resolution_code_id = db.Column(db.Integer, db.ForeignKey('resolutioncode.id', ondelete="CASCADE"), nullable=True)
    row_hash = db.Column(db.VARCHAR(length=255), nullable=True)


class AggregatedGenerationPerType(db.Model):
    __tablename__ = 'aggregatedgenerationpertype'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    action_task_id = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.VARCHAR(length=4), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    area_name = db.Column(db.VARCHAR(length=200), nullable=True)
    update_time = db.Column(db.DateTime, nullable=False)
    actual_generation_output = db.Column(db.Numeric(24, 2), nullable=False)
    actual_consuption = db.Column(db.Numeric(24, 2), nullable=False)  # consuption without M on purpose
    area_type_code_id = db.Column(db.Integer, db.ForeignKey('areatypecode.id', ondelete="CASCADE"), nullable=True)
    production_type_id = db.Column(db.Integer, db.ForeignKey('productiontype.id', ondelete="CASCADE"),
                                   nullable=True)
    resolution_code_id = db.Column(db.Integer, db.ForeignKey('resolutioncode.id', ondelete="CASCADE"),
                                   nullable=True)
    map_code_id = db.Column(db.Integer, db.ForeignKey('mapcode.id', ondelete="CASCADE"), nullable=True)

    area_code_id = db.Column(db.Integer, db.ForeignKey('allocatedeicdetail.id', ondelete="CASCADE"), nullable=False)
    row_hash = db.Column(db.VARCHAR(length=255), nullable=True)


class DayAheadTotalLoadForecast(db.Model):
    __tablename__ = 'dayaheadtotalloadforecast'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entity_created_at = db.Column(db.DateTime, nullable=False)
    entity_modified_at = db.Column(db.DateTime, nullable=False)
    action_task_id = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.VARCHAR(length=4), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    area_name = db.Column(db.VARCHAR(length=200), nullable=True)
    update_time = db.Column(db.DateTime, nullable=False)
    total_load_value = db.Column(db.Numeric(24, 2), nullable=False)
    area_type_code_id = db.Column(db.Integer, db.ForeignKey('areatypecode.id', ondelete="CASCADE"), nullable=True)
    map_code_id = db.Column(db.Integer, db.ForeignKey('mapcode.id', ondelete="CASCADE"), nullable=True)
    resolution_code_id = db.Column(db.Integer, db.ForeignKey('resolutioncode.id', ondelete="CASCADE"), nullable=True)
    area_code_id = db.Column(db.Integer, db.ForeignKey('allocatedeicdetail.id', ondelete="CASCADE"), nullable=False)
    row_hash = db.Column(db.VARCHAR(length=255), nullable=True)
