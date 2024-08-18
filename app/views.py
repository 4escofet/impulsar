from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from . import db, bcrypt
from .models import User, KPI, KPIDescription
from .forms import RegistrationForm, LoginForm, EvaluationForm
from flask import Blueprint
from sqlalchemy import text  

# Definir el blueprint para las vistas
views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')


@views.route('/recursos')
def recursos():
    return render_template('recursos.html')


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
                # Redirigir al nuevo endpoint de dashboard de admin
                return redirect(next_page) if next_page else redirect(url_for('views.get_admin_latest_kpis'))
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
    kpi_objects = KPI.query.filter_by(cuit=user.cuit).all()
    
    descriptions = {desc.question_number: {} for desc in KPIDescription.query.all()}
    for desc in KPIDescription.query.all():
        descriptions[desc.question_number][desc.value] = desc.description

    def get_color(value):
        if value >= 4:
            return "darkgreen"
        elif value >= 2:
            return "yellow"
        else:
            return "red"

    kpis = []
    for kpi in kpi_objects:
        kpis.append({
            'question': 'Reducción Consumo Eléctrico',
            'value': kpi.reduc_consumo_electrico,
            'description': descriptions[1][round(kpi.reduc_consumo_electrico, 0)],
            'color': get_color(kpi.reduc_consumo_electrico)
        })
        kpis.append({
            'question': 'Gestión Ambiental',
            'value': kpi.gestion_ambiental,
            'description': descriptions[2][round(kpi.gestion_ambiental, 0)],
            'color': get_color(kpi.gestion_ambiental)
        })
        kpis.append({
            'question': 'Reducción Consumo Agua',
            'value': kpi.reduc_consumo_agua,
            'description': descriptions[3][round(kpi.reduc_consumo_agua, 0)],
            'color': get_color(kpi.reduc_consumo_agua)
        })
        kpis.append({
            'question': 'Reducción Residuos',
            'value': kpi.reduc_residuos,
            'description': descriptions[4][round(kpi.reduc_residuos, 0)],
            'color': get_color(kpi.reduc_residuos)
        })
        kpis.append({
            'question': 'Análisis Impactos Ambientales',
            'value': kpi.impacto_ambiental,
            'description': descriptions[5][round(kpi.impacto_ambiental, 0)],
            'color': get_color(kpi.impacto_ambiental)
        })
        kpis.append({
            'question': 'Cumplimiento Aspectos Laborales',
            'value': kpi.asp_laborales,
            'description': descriptions[6][round(kpi.asp_laborales, 0)],
            'color': get_color(kpi.asp_laborales)
        })
        kpis.append({
            'question': 'Gestión Diversidad e Inclusión',
            'value': kpi.div_inc_ddhh,
            'description': descriptions[7][round(kpi.div_inc_ddhh, 0)],
            'color': get_color(kpi.div_inc_ddhh)
        })
        kpis.append({
            'question': 'Acciones Sociales',
            'value': kpi.acc_social,
            'description': descriptions[8][round(kpi.acc_social, 0)],
            'color': get_color(kpi.acc_social)
        })
        kpis.append({
            'question': 'Gestión Salud y Seguridad',
            'value': kpi.ssma,
            'description': descriptions[9][round(kpi.ssma, 0)],
            'color': get_color(kpi.ssma)
        })
        kpis.append({
            'question': 'Gestión Formación',
            'value': kpi.formacion,
            'description': descriptions[10][round(kpi.formacion, 0)],
            'color': get_color(kpi.formacion)
        })
        kpis.append({
            'question': 'Código de Conducta',
            'value': kpi.codigo_conducta,
            'description': descriptions[11][round(kpi.codigo_conducta, 0)],
            'color': get_color(kpi.codigo_conducta)
        })
        kpis.append({
            'question': 'Canal de Denuncias',
            'value': kpi.linea_etica,
            'description': descriptions[12][round(kpi.linea_etica, 0)],
            'color': get_color(kpi.linea_etica)
        })
        kpis.append({
            'question': 'Área de Compliance',
            'value': kpi.area_compliance,
            'description': descriptions[13][round(kpi.area_compliance, 0)],
            'color': get_color(kpi.area_compliance)
        })
        kpis.append({
            'question': 'Debida Diligencia',
            'value': kpi.due_dilligence,
            'description': descriptions[14][round(kpi.due_dilligence, 0)],
            'color': get_color(kpi.due_dilligence)
        })
        kpis.append({
            'question': 'Evaluación de Riesgos',
            'value': kpi.riesgos,
            'description': descriptions[15][round(kpi.riesgos, 0)],
            'color': get_color(kpi.riesgos)
        })
        kpis.append({
            'question': 'Huella de CO2',
            'value': kpi.huella_co2,
            'description': descriptions[16][round(kpi.huella_co2, 0)],
            'color': get_color(kpi.huella_co2)
        })

    return render_template('user.html', user=user, kpis=kpis)


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

""" @views.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('views.home'))
    try:
        print("Antes de la consulta de usuarios")
        query = text("SELECT cuit, organization_name FROM user WHERE is_admin = 0")
        print(f"Query ejecutada: {query}")
        result = db.session.execute(query)
        users = result.fetchall()
        print(f"Usuarios obtenidos: {users}")
        
        # Convertir los resultados en una lista de diccionarios para facilitar su uso
        users = [{"cuit": row[0], "organization_name": row[1]} for row in users]
        print(f"Lista de usuarios: {users}")

    except Exception as e:
        print(f"Error al obtener usuarios: {str(e)}")
        users = []

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
    return render_template('dashboard.html', users=users, kpi_averages=kpi_averages, descriptions=descriptions) """


from flask import jsonify, render_template
from flask_login import login_required, current_user
from .models import KPI, KPIDescription
from . import db


@views.route('/api/kpis/admin/latest')
@login_required
def get_admin_latest_kpis():
    if not current_user.is_admin:
        return jsonify({'error': 'Access Denied'}), 403

    # Obtener la última evaluación por cuit
    subquery = db.session.query(
        KPI.cuit, db.func.max(KPI.date).label('latest_date')
    ).group_by(KPI.cuit).subquery()

    # Obtener los promedios de los KPIs más recientes
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
    ).join(subquery, (KPI.cuit == subquery.c.cuit) & (KPI.date == subquery.c.latest_date)).one()

    descriptions = {desc.question_number: {} for desc in KPIDescription.query.all()}
    for desc in KPIDescription.query.all():
        descriptions[desc.question_number][desc.value] = desc.description

    users = User.query.all()  # Obtener todos los usuarios para el selector

    def get_color(value):
        if value >= 4:
            return "darkgreen"
        elif value >= 2:
            return "yellow"
        else:
            return "red"

    # Crear la lista de KPIs con las descripciones y colores
    kpis_data = {
        'reduc_consumo_electrico': kpis.reduc_consumo_electrico,
        'gestion_ambiental': kpis.gestion_ambiental,
        'reduc_consumo_agua': kpis.reduc_consumo_agua,
        'reduc_residuos': kpis.reduc_residuos,
        'impacto_ambiental': kpis.impacto_ambiental,
        'asp_laborales': kpis.asp_laborales,
        'div_inc_ddhh': kpis.div_inc_ddhh,
        'acc_social': kpis.acc_social,
        'ssma': kpis.ssma,
        'formacion': kpis.formacion,
        'codigo_conducta': kpis.codigo_conducta,
        'linea_etica': kpis.linea_etica,
        'area_compliance': kpis.area_compliance,
        'due_dilligence': kpis.due_dilligence,
        'riesgos': kpis.riesgos,
        'huella_co2': kpis.huella_co2
    }

    kpis_data_with_meta = [
        {
            'question': 'Reducción Consumo Eléctrico',
            'value': kpis_data['reduc_consumo_electrico'],
            'description': descriptions[1][round(kpis_data['reduc_consumo_electrico'], 0)],
            'color': get_color(kpis_data['reduc_consumo_electrico'])
        },
        {
            'question': 'Gestión Ambiental',
            'value': kpis_data['gestion_ambiental'],
            'description': descriptions[2][round(kpis_data['gestion_ambiental'], 0)],
            'color': get_color(kpis_data['gestion_ambiental'])
        },
        {
            'question': 'Reducción Consumo Agua',
            'value': kpis_data['reduc_consumo_agua'],
            'description': descriptions[3][round(kpis_data['reduc_consumo_agua'], 0)],
            'color': get_color(kpis_data['reduc_consumo_agua'])
        },
        {
            'question': 'Reducción Residuos',
            'value': kpis_data['reduc_residuos'],
            'description': descriptions[4][round(kpis_data['reduc_residuos'], 0)],
            'color': get_color(kpis_data['reduc_residuos'])
        },
        {
            'question': 'Análisis Impactos Ambientales',
            'value': kpis_data['impacto_ambiental'],
            'description': descriptions[5][round(kpis_data['impacto_ambiental'], 0)],
            'color': get_color(kpis_data['impacto_ambiental'])
        },
        {
            'question': 'Cumplimiento Aspectos Laborales',
            'value': kpis_data['asp_laborales'],
            'description': descriptions[6][round(kpis_data['asp_laborales'], 0)],
            'color': get_color(kpis_data['asp_laborales'])
        },
        {
            'question': 'Gestión Diversidad e Inclusión',
            'value': kpis_data['div_inc_ddhh'],
            'description': descriptions[7][round(kpis_data['div_inc_ddhh'], 0)],
            'color': get_color(kpis_data['div_inc_ddhh'])
        },
        {
            'question': 'Acciones Sociales',
            'value': kpis_data['acc_social'],
            'description': descriptions[8][round(kpis_data['acc_social'], 0)],
            'color': get_color(kpis_data['acc_social'])
        },
        {
            'question': 'Gestión Salud y Seguridad',
            'value': kpis_data['ssma'],
            'description': descriptions[9][round(kpis_data['ssma'], 0)],
            'color': get_color(kpis_data['ssma'])
        },
        {
            'question': 'Gestión Formación',
            'value': kpis_data['formacion'],
            'description': descriptions[10][round(kpis_data['formacion'], 0)],
            'color': get_color(kpis_data['formacion'])
        },
        {
            'question': 'Código de Conducta',
            'value': kpis_data['codigo_conducta'],
            'description': descriptions[11][round(kpis_data['codigo_conducta'], 0)],
            'color': get_color(kpis_data['codigo_conducta'])
        },
        {
            'question': 'Canal de Denuncias',
            'value': kpis_data['linea_etica'],
            'description': descriptions[12][round(kpis_data['linea_etica'], 0)],
            'color': get_color(kpis_data['linea_etica'])
        },
        {
            'question': 'Área de Compliance',
            'value': kpis_data['area_compliance'],
            'description': descriptions[13][round(kpis_data['area_compliance'], 0)],
            'color': get_color(kpis_data['area_compliance'])
        },
        {
            'question': 'Debida Diligencia',
            'value': kpis_data['due_dilligence'],
            'description': descriptions[14][round(kpis_data['due_dilligence'], 0)],
            'color': get_color(kpis_data['due_dilligence'])
        },
        {
            'question': 'Evaluación de Riesgos',
            'value': kpis_data['riesgos'],
            'description': descriptions[15][round(kpis_data['riesgos'], 0)],
            'color': get_color(kpis_data['riesgos'])
        },
        {
            'question': 'Huella de CO2',
            'value': kpis_data['huella_co2'],
            'description': descriptions[16][round(kpis_data['huella_co2'], 0)],
            'color': get_color(kpis_data['huella_co2'])
        }
    ]

    # Renderizar la plantilla del dashboard con los datos y el selector de usuarios
    return render_template('dashboard.html', kpi_averages=kpis_data, descriptions=descriptions, users=users)



@views.route('/api/kpis/admin/evolution')
@login_required
def get_admin_kpi_evolution():
    if not current_user.is_admin:
        return jsonify({'error': 'Access Denied'}), 403

    # Obtener la evolución de los KPIs, agrupados por CUIT y fecha
    kpi_evolution = db.session.query(
        KPI.cuit,
        KPI.date,
        KPI.reduc_consumo_electrico,
        KPI.gestion_ambiental,
        KPI.reduc_consumo_agua,
        KPI.reduc_residuos,
        KPI.impacto_ambiental,
        KPI.asp_laborales,
        KPI.div_inc_ddhh,
        KPI.acc_social,
        KPI.ssma,
        KPI.formacion,
        KPI.codigo_conducta,
        KPI.linea_etica,
        KPI.area_compliance,
        KPI.due_dilligence,
        KPI.riesgos,
        KPI.huella_co2
    ).order_by(KPI.cuit, KPI.date).all()

    # Organizar los datos por CUIT y fecha para ser enviados al front-end
    evolution_data = {}
    for kpi in kpi_evolution:
        if kpi.cuit not in evolution_data:
            evolution_data[kpi.cuit] = []
        evolution_data[kpi.cuit].append({
            'date': kpi.date,
            'reduc_consumo_electrico': kpi.reduc_consumo_electrico,
            'gestion_ambiental': kpi.gestion_ambiental,
            'reduc_consumo_agua': kpi.reduc_consumo_agua,
            'reduc_residuos': kpi.reduc_residuos,
            'impacto_ambiental': kpi.impacto_ambiental,
            'asp_laborales': kpi.asp_laborales,
            'div_inc_ddhh': kpi.div_inc_ddhh,
            'acc_social': kpi.acc_social,
            'ssma': kpi.ssma,
            'formacion': kpi.formacion,
            'codigo_conducta': kpi.codigo_conducta,
            'linea_etica': kpi.linea_etica,
            'area_compliance': kpi.area_compliance,
            'due_dilligence': kpi.due_dilligence,
            'riesgos': kpi.riesgos,
            'huella_co2': kpi.huella_co2
        })

    return jsonify({'evolution': evolution_data})



@views.route('/api/kpis/user/latest/<int:cuit>')
@login_required
def get_user_latest_kpis(cuit):
    if not current_user.is_admin and current_user.cuit != cuit:
        return jsonify({'error': 'Access Denied'}), 403

    # Obtener la última evaluación del usuario
    subquery = db.session.query(
        KPI.cuit, db.func.max(KPI.date).label('latest_date')
    ).filter(KPI.cuit == cuit).group_by(KPI.cuit).subquery()

    # Obtener los KPIs más recientes para este usuario
    kpi = db.session.query(
        KPI.reduc_consumo_electrico,
        KPI.gestion_ambiental,
        KPI.reduc_consumo_agua,
        KPI.reduc_residuos,
        KPI.impacto_ambiental,
        KPI.asp_laborales,
        KPI.div_inc_ddhh,
        KPI.acc_social,
        KPI.ssma,
        KPI.formacion,
        KPI.codigo_conducta,
        KPI.linea_etica,
        KPI.area_compliance,
        KPI.due_dilligence,
        KPI.riesgos,
        KPI.huella_co2
    ).join(subquery, (KPI.cuit == subquery.c.cuit) & (KPI.date == subquery.c.latest_date)).one()

    descriptions = {desc.question_number: {} for desc in KPIDescription.query.all()}
    for desc in KPIDescription.query.all():
        descriptions[desc.question_number][desc.value] = desc.description

    def get_color(value):
        if value >= 4:
            return "darkgreen"
        elif value >= 2:
            return "yellow"
        else:
            return "red"

    # Crear la lista de KPIs con las descripciones y colores
    kpis_data = [
        {
            'question': 'Reducción Consumo Eléctrico',
            'value': kpi.reduc_consumo_electrico,
            'description': descriptions[1][round(kpi.reduc_consumo_electrico, 0)],
            'color': get_color(kpi.reduc_consumo_electrico)
        },
        {
            'question': 'Gestión Ambiental',
            'value': kpi.gestion_ambiental,
            'description': descriptions[2][round(kpi.gestion_ambiental, 0)],
            'color': get_color(kpi.gestion_ambiental)
        },
        {
            'question': 'Reducción Consumo Agua',
            'value': kpi.reduc_consumo_agua,
            'description': descriptions[3][round(kpi.reduc_consumo_agua, 0)],
            'color': get_color(kpi.reduc_consumo_agua)
        },
        {
            'question': 'Reducción Residuos',
            'value': kpi.reduc_residuos,
            'description': descriptions[4][round(kpi.reduc_residuos, 0)],
            'color': get_color(kpi.reduc_residuos)
        },
        {
            'question': 'Análisis Impactos Ambientales',
            'value': kpi.impacto_ambiental,
            'description': descriptions[5][round(kpi.impacto_ambiental, 0)],
            'color': get_color(kpi.impacto_ambiental)
        },
        {
            'question': 'Cumplimiento Aspectos Laborales',
            'value': kpi.asp_laborales,
            'description': descriptions[6][round(kpi.asp_laborales, 0)],
            'color': get_color(kpi.asp_laborales)
        },
        {
            'question': 'Gestión Diversidad e Inclusión',
            'value': kpi.div_inc_ddhh,
            'description': descriptions[7][round(kpi.div_inc_ddhh, 0)],
            'color': get_color(kpi.div_inc_ddhh)
        },
        {
            'question': 'Acciones Sociales',
            'value': kpi.acc_social,
            'description': descriptions[8][round(kpi.acc_social, 0)],
            'color': get_color(kpi.acc_social)
        },
        {
            'question': 'Gestión Salud y Seguridad',
            'value': kpi.ssma,
            'description': descriptions[9][round(kpi.ssma, 0)],
            'color': get_color(kpi.ssma)
        },
        {
            'question': 'Gestión Formación',
            'value': kpi.formacion,
            'description': descriptions[10][round(kpi.formacion, 0)],
            'color': get_color(kpi.formacion)
        },
        {
            'question': 'Código de Conducta',
            'value': kpi.codigo_conducta,
            'description': descriptions[11][round(kpi.codigo_conducta, 0)],
            'color': get_color(kpi.codigo_conducta)
        },
        {
            'question': 'Canal de Denuncias',
            'value': kpi.linea_etica,
            'description': descriptions[12][round(kpi.linea_etica, 0)],
            'color': get_color(kpi.linea_etica)
        },
        {
            'question': 'Área de Compliance',
            'value': kpi.area_compliance,
            'description': descriptions[13][round(kpi.area_compliance, 0)],
            'color': get_color(kpi.area_compliance)
        },
        {
            'question': 'Debida Diligencia',
            'value': kpi.due_dilligence,
            'description': descriptions[14][round(kpi.due_dilligence, 0)],
            'color': get_color(kpi.due_dilligence)
        },
        {
            'question': 'Evaluación de Riesgos',
            'value': kpi.riesgos,
            'description': descriptions[15][round(kpi.riesgos, 0)],
            'color': get_color(kpi.riesgos)
        },
        {
            'question': 'Huella de CO2',
            'value': kpi.huella_co2,
            'description': descriptions[16][round(kpi.huella_co2, 0)],
            'color': get_color(kpi.huella_co2)
        }
    ]

    return jsonify({'kpis': kpis_data})


@views.route('/api/kpis/user/evolution/<int:cuit>')
@login_required
def get_user_kpi_evolution(cuit):
    if not current_user.is_admin and current_user.cuit != cuit:
        return jsonify({'error': 'Access Denied'}), 403

    # Obtener la evolución de los KPIs para un usuario específico, ordenado por fecha
    kpi_evolution = db.session.query(
        KPI.date,
        KPI.reduc_consumo_electrico,
        KPI.gestion_ambiental,
        KPI.reduc_consumo_agua,
        KPI.reduc_residuos,
        KPI.impacto_ambiental,
        KPI.asp_laborales,
        KPI.div_inc_ddhh,
        KPI.acc_social,
        KPI.ssma,
        KPI.formacion,
        KPI.codigo_conducta,
        KPI.linea_etica,
        KPI.area_compliance,
        KPI.due_dilligence,
        KPI.riesgos,
        KPI.huella_co2
    ).filter_by(cuit=cuit).order_by(KPI.date).all()

    # Organizar los datos por fecha para ser enviados al front-end
    evolution_data = []
    for kpi in kpi_evolution:
        evolution_data.append({
            'date': kpi.date,
            'reduc_consumo_electrico': kpi.reduc_consumo_electrico,
            'gestion_ambiental': kpi.gestion_ambiental,
            'reduc_consumo_agua': kpi.reduc_consumo_agua,
            'reduc_residuos': kpi.reduc_residuos,
            'impacto_ambiental': kpi.impacto_ambiental,
            'asp_laborales': kpi.asp_laborales,
            'div_inc_ddhh': kpi.div_inc_ddhh,
            'acc_social': kpi.acc_social,
            'ssma': kpi.ssma,
            'formacion': kpi.formacion,
            'codigo_conducta': kpi.codigo_conducta,
            'linea_etica': kpi.linea_etica,
            'area_compliance': kpi.area_compliance,
            'due_dilligence': kpi.due_dilligence,
            'riesgos': kpi.riesgos,
            'huella_co2': kpi.huella_co2
        })

    return jsonify({'evolution': evolution_data})



""" @views.route('/api/kpis/<cuit>')
@login_required
def get_kpis(cuit):
    if not current_user.is_admin:
        return jsonify({'error': 'Access Denied'}), 403

    descriptions = {desc.question_number: {} for desc in KPIDescription.query.all()}
    for desc in KPIDescription.query.all():
        descriptions[desc.question_number][desc.value] = desc.description

    def get_color(value):
        if value >= 4:
            return "darkgreen"
        elif value >= 2:
            return "yellow"
        else:
            return "red"

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
            {'question': 'Reducción Consumo Eléctrico', 'value': kpis.reduc_consumo_electrico, 'description': descriptions[1][round(kpis.reduc_consumo_electrico, 0)], 'color': get_color(kpis.reduc_consumo_electrico)},
            {'question': 'Gestión Ambiental', 'value': kpis.gestion_ambiental, 'description': descriptions[2][round(kpis.gestion_ambiental, 0)], 'color': get_color(kpis.gestion_ambiental)},
            {'question': 'Reducción Consumo Agua', 'value': kpis.reduc_consumo_agua, 'description': descriptions[3][round(kpis.reduc_consumo_agua, 0)], 'color': get_color(kpis.reduc_consumo_agua)},
            {'question': 'Reducción Residuos', 'value': kpis.reduc_residuos, 'description': descriptions[4][round(kpis.reduc_residuos, 0)], 'color': get_color(kpis.reduc_residuos)},
            {'question': 'Análisis Impactos Ambientales', 'value': kpis.impacto_ambiental, 'description': descriptions[5][round(kpis.impacto_ambiental, 0)], 'color': get_color(kpis.impacto_ambiental)},
            {'question': 'Cumplimiento Aspectos Laborales', 'value': kpis.asp_laborales, 'description': descriptions[6][round(kpis.asp_laborales, 0)], 'color': get_color(kpis.asp_laborales)},
            {'question': 'Gestión Diversidad e Inclusión', 'value': kpis.div_inc_ddhh, 'description': descriptions[7][round(kpis.div_inc_ddhh, 0)], 'color': get_color(kpis.div_inc_ddhh)},
            {'question': 'Acciones Sociales', 'value': kpis.acc_social, 'description': descriptions[8][round(kpis.acc_social, 0)], 'color': get_color(kpis.acc_social)},
            {'question': 'Gestión Salud y Seguridad', 'value': kpis.ssma, 'description': descriptions[9][round(kpis.ssma, 0)], 'color': get_color(kpis.ssma)},
            {'question': 'Gestión Formación', 'value': kpis.formacion, 'description': descriptions[10][round(kpis.formacion, 0)], 'color': get_color(kpis.formacion)},
            {'question': 'Código de Conducta', 'value': kpis.codigo_conducta, 'description': descriptions[11][round(kpis.codigo_conducta, 0)], 'color': get_color(kpis.codigo_conducta)},
            {'question': 'Canal de Denuncias', 'value': kpis.linea_etica, 'description': descriptions[12][round(kpis.linea_etica, 0)], 'color': get_color(kpis.linea_etica)},
            {'question': 'Área de Compliance', 'value': kpis.area_compliance, 'description': descriptions[13][round(kpis.area_compliance, 0)], 'color': get_color(kpis.area_compliance)},
            {'question': 'Debida Diligencia', 'value': kpis.due_dilligence, 'description': descriptions[14][round(kpis.due_dilligence, 0)], 'color': get_color(kpis.due_dilligence)},
            {'question': 'Evaluación de Riesgos', 'value': kpis.riesgos, 'description': descriptions[15][round(kpis.riesgos, 0)], 'color': get_color(kpis.riesgos)},
            {'question': 'Huella de CO2', 'value': kpis.huella_co2, 'description': descriptions[16][round(kpis.huella_co2, 0)], 'color': get_color(kpis.huella_co2)}
        ]
    else:
        kpis = KPI.query.filter_by(cuit=cuit).all()
        kpis = [
            {'question': 'Reducción Consumo Eléctrico', 'value': kpi.reduc_consumo_electrico, 'description': descriptions[1][round(kpi.reduc_consumo_electrico, 0)], 'color': get_color(kpi.reduc_consumo_electrico)} for kpi in kpis
        ] + [
            {'question': 'Gestión Ambiental', 'value': kpi.gestion_ambiental, 'description': descriptions[2][round(kpi.gestion_ambiental, 0)], 'color': get_color(kpi.gestion_ambiental)} for kpi in kpis
        ] + [
            {'question': 'Reducción Consumo Agua', 'value': kpi.reduc_consumo_agua, 'description': descriptions[3][round(kpi.reduc_consumo_agua, 0)], 'color': get_color(kpi.reduc_consumo_agua)} for kpi in kpis
        ] + [
            {'question': 'Reducción Residuos', 'value': kpi.reduc_residuos, 'description': descriptions[4][round(kpi.reduc_residuos, 0)], 'color': get_color(kpi.reduc_residuos)} for kpi in kpis
        ] + [
            {'question': 'Análisis Impactos Ambientales', 'value': kpi.impacto_ambiental, 'description': descriptions[5][round(kpi.impacto_ambiental, 0)], 'color': get_color(kpi.impacto_ambiental)} for kpi in kpis
        ] + [
            {'question': 'Cumplimiento Aspectos Laborales', 'value': kpi.asp_laborales, 'description': descriptions[6][round(kpi.asp_laborales, 0)], 'color': get_color(kpi.asp_laborales)} for kpi in kpis
        ] + [
            {'question': 'Gestión Diversidad e Inclusión', 'value': kpi.div_inc_ddhh, 'description': descriptions[7][round(kpi.div_inc_ddhh, 0)], 'color': get_color(kpi.div_inc_ddhh)} for kpi in kpis
        ] + [
            {'question': 'Acciones Sociales', 'value': kpi.acc_social, 'description': descriptions[8][round(kpi.acc_social, 0)], 'color': get_color(kpi.acc_social)} for kpi in kpis
        ] + [
            {'question': 'Gestión Salud y Seguridad', 'value': kpi.ssma, 'description': descriptions[9][round(kpi.ssma, 0)], 'color': get_color(kpi.ssma)} for kpi in kpis
        ] + [
            {'question': 'Gestión Formación', 'value': kpi.formacion, 'description': descriptions[10][round(kpi.formacion, 0)], 'color': get_color(kpi.formacion)} for kpi in kpis
        ] + [
            {'question': 'Código de Conducta', 'value': kpi.codigo_conducta, 'description': descriptions[11][round(kpi.codigo_conducta, 0)], 'color': get_color(kpi.codigo_conducta)} for kpi in kpis
        ] + [
            {'question': 'Canal de Denuncias', 'value': kpi.linea_etica, 'description': descriptions[12][round(kpi.linea_etica, 0)], 'color': get_color(kpi.linea_etica)} for kpi in kpis
        ] + [
            {'question': 'Área de Compliance', 'value': kpi.area_compliance, 'description': descriptions[13][round(kpi.area_compliance, 0)], 'color': get_color(kpi.area_compliance)} for kpi in kpis
        ] + [
            {'question': 'Debida Diligencia', 'value': kpi.due_dilligence, 'description': descriptions[14][round(kpi.due_dilligence, 0)], 'color': get_color(kpi.due_dilligence)} for kpi in kpis
        ] + [
            {'question': 'Evaluación de Riesgos', 'value': kpi.riesgos, 'description': descriptions[15][round(kpi.riesgos, 0)], 'color': get_color(kpi.riesgos)} for kpi in kpis
        ] + [
            {'question': 'Huella de CO2', 'value': kpi.huella_co2, 'description': descriptions[16][round(kpi.huella_co2, 0)], 'color': get_color(kpi.huella_co2)} for kpi in kpis
        ]

    return jsonify({'kpis': kpis}) """