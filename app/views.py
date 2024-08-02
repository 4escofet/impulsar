# En views.py

from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from . import db, bcrypt
from .models import User, KPI, KPIDescription
from .forms import RegistrationForm, LoginForm, EvaluationForm
from flask import Blueprint

# Definir el blueprint para las vistas
views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            organization_name=form.organization_name.data,
            cuit=form.cuit.data,
            username=form.username.data,
            position=form.position.data,
            email=form.email.data,
            phone=form.phone.data,
            importance=form.importance.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('views.login'))
    return render_template('register.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # Verificar si el usuario es administrador
            if user.is_admin:
                return redirect(next_page) if next_page else redirect(url_for('views.admin_dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)



@views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@views.route('/user/<int:cuit>')
@login_required
def user(cuit):
    user = User.query.get_or_404(cuit)
    kpis = KPI.query.filter_by(cuit=user.cuit).all()
    descriptions = {desc.question_number: {} for desc in KPIDescription.query.all()}
    for desc in KPIDescription.query.all():
        descriptions[desc.question_number][desc.value] = desc.description
    return render_template('user.html', user=user, kpis=kpis, descriptions=descriptions)


@views.route('/user/<cuit>/evaluate', methods=['GET', 'POST'])
@login_required
def evaluate(cuit):
    user = User.query.get_or_404(cuit)
    form = EvaluationForm()
    if form.validate_on_submit():
        kpi = KPI(
            cuit=user.cuit,
            reduc_consumo_electrico=form.reduc_consumo_electrico.data,
            gestion_ambiental=form.gestion_ambiental.data,
            reduc_consumo_agua=form.reduc_consumo_agua.data,
            reduc_residuos=form.reduc_residuos.data,
            impacto_ambiental=form.impacto_ambiental.data,
            asp_laborales=form.asp_laborales.data,
            div_inc_ddhh=form.div_inc_ddhh.data,
            acc_social=form.acc_social.data,
            ssma=form.ssma.data,
            formacion=form.formacion.data,
            codigo_conducta=form.codigo_conducta.data,
            linea_etica=form.linea_etica.data,
            area_compliance=form.area_compliance.data,
            due_dilligence=form.due_dilligence.data,
            riesgos=form.riesgos.data,
            huella_co2=form.huella_co2.data,
            date=datetime.utcnow()
        )
        db.session.add(kpi)
        db.session.commit()
        flash('Auto-evaluation submitted successfully!', 'success')
        return redirect(url_for('views.user', cuit=user.cuit))
    return render_template('evaluate.html', user=user, form=form)

@views.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('views.home'))
    users = User.query.filter_by(is_admin=False).all()
    kpi_averages = {
        'reduc_consumo_electrico': round(db.session.query(db.func.avg(KPI.reduc_consumo_electrico)).scalar(), 2),
        'gestion_ambiental': round(db.session.query(db.func.avg(KPI.gestion_ambiental)).scalar(), 2),
        'reduc_consumo_agua': round(db.session.query(db.func.avg(KPI.reduc_consumo_agua)).scalar(), 2),
        'reduc_residuos': round(db.session.query(db.func.avg(KPI.reduc_residuos)).scalar(), 2),
        'impacto_ambiental': round(db.session.query(db.func.avg(KPI.impacto_ambiental)).scalar(), 2),
        'asp_laborales': round(db.session.query(db.func.avg(KPI.asp_laborales)).scalar(), 2),
        'div_inc_ddhh': round(db.session.query(db.func.avg(KPI.div_inc_ddhh)).scalar(), 2),
        'acc_social': round(db.session.query(db.func.avg(KPI.acc_social)).scalar(), 2),
        'ssma': round(db.session.query(db.func.avg(KPI.ssma)).scalar(), 2),
        'formacion': round(db.session.query(db.func.avg(KPI.formacion)).scalar(), 2),
        'codigo_conducta': round(db.session.query(db.func.avg(KPI.codigo_conducta)).scalar(), 2),
        'linea_etica': round(db.session.query(db.func.avg(KPI.linea_etica)).scalar(), 2),
        'area_compliance': round(db.session.query(db.func.avg(KPI.area_compliance)).scalar(), 2),
        'due_dilligence': round(db.session.query(db.func.avg(KPI.due_dilligence)).scalar(), 2),
        'riesgos': round(db.session.query(db.func.avg(KPI.riesgos)).scalar(), 2),
        'huella_co2': round(db.session.query(db.func.avg(KPI.huella_co2)).scalar(), 2)
    }
    descriptions = {desc.question_number: {} for desc in KPIDescription.query.all()}
    for desc in KPIDescription.query.all():
        descriptions[desc.question_number][desc.value] = desc.description
    return render_template('dashboard.html', users=users, kpi_averages=kpi_averages, descriptions=descriptions)


@views.route('/recursos')
def recursos():
    return render_template('recursos.html')

@views.route('/api/kpis/<cuit>')
@login_required
def get_kpis(cuit):
    if not current_user.is_admin:
        return jsonify({'error': 'Access Denied'}), 403

    if cuit == 'all':
        kpis = db.session.query(
            db.func.avg(KPI.reduc_consumo_electrico).label('reduc_consumo_electrico'),
            db.func.avg(KPI.gestion_ambiental).label('gestion_ambiental'),
            db.func.avg(KPI.reduc_consumo_agua).label('reduc_consumo_agua'),
            db.func.avg(KPI.reduc_residuos).label('reduc_residuos'),
            db.func.avg(KPI.impacto_ambiental).label('impacto_ambiental'),
            db.func.avg(KPI.asp_laborales).label('asp_laborales'),
            db.func.avg(KPI.div_inc_ddhh).label('div_inc_ddhh'),
            db.func.avg(KPI.acc_social).label('acc_social'),
            db.func.avg(KPI.ssma).label('ssma'),
            db.func.avg(KPI.formacion).label('formacion'),
            db.func.avg(KPI.codigo_conducta).label('codigo_conducta'),
            db.func.avg(KPI.linea_etica).label('linea_etica'),
            db.func.avg(KPI.area_compliance).label('area_compliance'),
            db.func.avg(KPI.due_dilligence).label('due_dilligence'),
            db.func.avg(KPI.riesgos).label('riesgos'),
            db.func.avg(KPI.huella_co2).label('huella_co2')
        ).one()
        kpis = [
            {'question': 'Reducción Consumo Eléctrico', 'value': kpis.reduc_consumo_electrico},
            {'question': 'Gestión Ambiental', 'value': kpis.gestion_ambiental},
            {'question': 'Reducción Consumo Agua', 'value': kpis.reduc_consumo_agua},
            {'question': 'Reducción Residuos', 'value': kpis.reduc_residuos},
            {'question': 'Análisis Impactos Ambientales', 'value': kpis.impacto_ambiental},
            {'question': 'Cumplimiento Aspectos Laborales', 'value': kpis.asp_laborales},
            {'question': 'Gestión Diversidad e Inclusión', 'value': kpis.div_inc_ddhh},
            {'question': 'Acciones Sociales', 'value': kpis.acc_social},
            {'question': 'Gestión Salud y Seguridad', 'value': kpis.ssma},
            {'question': 'Gestión Formación', 'value': kpis.formacion},
            {'question': 'Código de Conducta', 'value': kpis.codigo_conducta},
            {'question': 'Canal de Denuncias', 'value': kpis.linea_etica},
            {'question': 'Área de Compliance', 'value': kpis.area_compliance},
            {'question': 'Debida Diligencia', 'value': kpis.due_dilligence},
            {'question': 'Evaluación de Riesgos', 'value': kpis.riesgos},
            {'question': 'Huella de CO2', 'value': kpis.huella_co2}
        ]
    else:
        kpis = KPI.query.filter_by(cuit=cuit).all()
        kpis = [
            {'question': 'Reducción Consumo Eléctrico', 'value': kpi.reduc_consumo_electrico} for kpi in kpis
        ] + [
            {'question': 'Gestión Ambiental', 'value': kpi.gestion_ambiental} for kpi in kpis
        ] + [
            {'question': 'Reducción Consumo Agua', 'value': kpi.reduc_consumo_agua} for kpi in kpis
        ] + [
            {'question': 'Reducción Residuos', 'value': kpi.reduc_residuos} for kpi in kpis
        ] + [
            {'question': 'Análisis Impactos Ambientales', 'value': kpi.impacto_ambiental} for kpi in kpis
        ] + [
            {'question': 'Cumplimiento Aspectos Laborales', 'value': kpi.asp_laborales} for kpi in kpis
        ] + [
            {'question': 'Gestión Diversidad e Inclusión', 'value': kpi.div_inc_ddhh} for kpi in kpis
        ] + [
            {'question': 'Acciones Sociales', 'value': kpi.acc_social} for kpi in kpis
        ] + [
            {'question': 'Gestión Salud y Seguridad', 'value': kpi.ssma} for kpi in kpis
        ] + [
            {'question': 'Gestión Formación', 'value': kpi.formacion} for kpi in kpis
        ] + [
            {'question': 'Código de Conducta', 'value': kpi.codigo_conducta} for kpi in kpis
        ] + [
            {'question': 'Canal de Denuncias', 'value': kpi.linea_etica} for kpi in kpis
        ] + [
            {'question': 'Área de Compliance', 'value': kpi.area_compliance} for kpi in kpis
        ] + [
            {'question': 'Debida Diligencia', 'value': kpi.due_dilligence} for kpi in kpis
        ] + [
            {'question': 'Evaluación de Riesgos', 'value': kpi.riesgos} for kpi in kpis
        ] + [
            {'question': 'Huella de CO2', 'value': kpi.huella_co2} for kpi in kpis
        ]

    return jsonify({'kpis': kpis})
