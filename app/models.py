from datetime import datetime
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    cuit = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    importance = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  
    kpis = db.relationship('KPI', backref='user', lazy=True)

    def get_id(self):
        return str(self.cuit)

class KPI(db.Model):
    kpi_id = db.Column(db.Integer, primary_key=True)
    cuit = db.Column(db.Integer, db.ForeignKey('user.cuit'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    reduc_consumo_electrico = db.Column(db.Integer, nullable=False)
    gestion_ambiental = db.Column(db.Integer, nullable=False)
    reduc_consumo_agua = db.Column(db.Integer, nullable=False)
    reduc_residuos = db.Column(db.Integer, nullable=False)
    impacto_ambiental = db.Column(db.Integer, nullable=False)
    asp_laborales = db.Column(db.Integer, nullable=False)
    div_inc_ddhh = db.Column(db.Integer, nullable=False)
    acc_social = db.Column(db.Integer, nullable=False)
    ssma = db.Column(db.Integer, nullable=False)
    formacion = db.Column(db.Integer, nullable=False)
    codigo_conducta = db.Column(db.Integer, nullable=False)
    linea_etica = db.Column(db.Integer, nullable=False)
    area_compliance = db.Column(db.Integer, nullable=False)
    due_dilligence = db.Column(db.Integer, nullable=False)
    riesgos = db.Column(db.Integer, nullable=False)
    huella_co2 = db.Column(db.Integer, nullable=False)

class KPIDescription(db.Model):
    __tablename__ = 'kpi_descriptions'
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<KPIDescription {self.question_number}-{self.value}>'
