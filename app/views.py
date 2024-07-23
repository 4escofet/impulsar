from flask import render_template, redirect, url_for, flash, request, current_app as app
from flask_login import login_user, login_required, logout_user, current_user
from . import db, bcrypt
from .models import User, KPI, KPIDescription
from .forms import RegistrationForm, LoginForm, EvaluationForm
from datetime import datetime

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return render_template('index.html')

@app.route('/recursos')
def recursos():
    app.logger.debug("Recursos route accessed")
    return render_template('recursos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.debug("Login route accessed")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            app.logger.debug("User found and password matched")
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.debug("Register route accessed")
    form = RegistrationForm()
    if form.validate_on_submit():
        app.logger.debug("Registration form submitted")
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
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/user/<int:cuit>')
@login_required
def user(cuit):
    user = User.query.get_or_404(cuit)
    kpis = KPI.query.filter_by(cuit=user.cuit).all()  # Ajuste aquí

    descriptions = {desc.question_number: {} for desc in KPIDescription.query.all()}
    for desc in KPIDescription.query.all():
        descriptions[desc.question_number][desc.value] = desc.description

    return render_template('user.html', user=user, kpis=kpis, descriptions=descriptions)


@app.route('/user/<cuit>/evaluate', methods=['GET', 'POST'])
@login_required
def evaluate(cuit):
    user = User.query.get_or_404(cuit)
    form = EvaluationForm()
    if form.validate_on_submit():
        kpi = KPI(
            user_cuit=user.cuit,
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
        return redirect(url_for('user', cuit=user.cuit))
    return render_template('evaluate.html', user=user, form=form)
