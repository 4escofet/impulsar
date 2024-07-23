from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    organization_name = StringField('Nombre de la Organización', validators=[DataRequired(), Length(min=2, max=150)])
    cuit = IntegerField('CUIT', validators=[DataRequired()])
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=150)])
    position = StringField('Cargo', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Teléfono', validators=[DataRequired()])
    importance = BooleanField('Importancia')
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email ya está en uso.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Login')

class EvaluationForm(FlaskForm):
    reduc_consumo_electrico = SelectField('1. ¿Su Organización realiza acciones relativas a la reducción del consumo eléctrico?', choices=[
        (0, 'No'),
        (1, 'La organización no realiza acciones'),
        (2, 'La organización realiza acciones esporádicas'),
        (3, 'La organización posee un plan de reducción del consumo eléctrico'),
        (4, 'La organización posee un programa de gestión ambiental en donde se contempla la reducción del consumo eléctrico y lo supervisa la más alta autoridad')
    ], validators=[DataRequired()])

    gestion_ambiental = SelectField('2. ¿Su organización posee un programa de gestión ambiental?', choices=[
        (0, 'No'),
        (1, 'No posee un programa de gestión ambiental'),
        (2, 'La organización posee un programa de gestión ambiental respetando la normativa ambiental'),
        (3, 'La organización posee un programa de gestión ambiental y posee certificaciones externas (ISO o similar)'),
        (4, 'La organización posee un programa de gestión ambiental y posee certificaciones externas (ISO o similar) y lo supervisa la más alta autoridad')
    ], validators=[DataRequired()])

    reduc_consumo_agua = SelectField('3. ¿Su Organización realiza acciones relativas a la reducción del consumo de agua?', choices=[
        (0, 'No'),
        (1, 'La organización no realiza acciones'),
        (2, 'La organización realiza acciones esporádicas'),
        (3, 'La organización posee un plan de reducción del consumo de agua'),
        (4, 'La organización posee un programa de gestión ambiental en donde se contempla la reducción del consumo de agua y lo supervisa la más alta autoridad')
    ], validators=[DataRequired()])

    reduc_residuos = SelectField('4. ¿Su Organización realiza acciones relativas a la reducción de residuos?', choices=[
        (0, 'No'),
        (1, 'La organización no realiza acciones'),
        (2, 'La organización realiza acciones esporádicas'),
        (3, 'La organización posee un plan de reducción de residuos'),
        (4, 'La organización posee un programa de gestión ambiental en donde se contempla la reducción de residuos y lo supervisa la más alta autoridad')
    ], validators=[DataRequired()])

    impacto_ambiental = SelectField('5. ¿Se ha realizado en su organización un análisis de los impactos ambientales de su actividad?', choices=[
        (0, 'No'),
        (1, 'No se dispone de una identificación ni de una definición de temas relevantes relacionados con aspectos ambientales para la actividad de la organización'),
        (2, 'Se ha llevado a cabo una identificación de los temas relevantes para la organización y las áreas de influencia en temas ambientales'),
        (3, 'Además de la identificación de asuntos relevantes, la organización establece planes y objetivos para gestionar los asuntos relevantes identificados'),
        (4, 'La gestión de los asuntos relevantes son una prioridad para la organización y lo supervisa la más alta autoridad')
    ], validators=[DataRequired()])

    asp_laborales = SelectField('6. ¿En qué medida si Organización cumple con los aspectos laborales?', choices=[
        (0, 'No'),
        (1, 'La organización incumple o cumple parcialmente aspectos básicos de la ley laboral'),
        (2, 'La organización cumple la regulación en materia laboral (Estatuto de los trabajadores, Convenio colectivo), Seguridad y Salud, Protección de datos, etc.'),
        (3, 'Además del cumplimiento regulatorio, la empresa establece planes y objetivos para mejorar la gestión de las condiciones laborales (como plan de cero accidentes)'),
        (4, 'Las cuestiones laborales y de desarrollo profesional forman parte de la estrategia de la organización y se supervisan por la máxima autoridad de la organización.')
    ], validators=[DataRequired()])

    div_inc_ddhh = SelectField('7. ¿Cómo gestiona su organización los aspectos relacionados con la diversidad, inclusión y derechos humanos?', choices=[
        (0, 'No'),
        (1, 'La organización incumple o cumple parcialmente regulación en materia de diversidad, inclusión, discriminación o derechos humanos'),
        (2, 'La organización cumple la regulación y normativa vigente en materia de diversidad e inclusión'),
        (3, 'La organización establece prácticas y objetivos para mejorar la gestión de la diversidad e inclusión que van más allá del cumplimiento regulatorio, estableciendo objetivos de integración de colectivos vulnerables'),
        (4, 'Los asuntos relacionados con diversidad, inclusión y derechos humanos forman parte de la estrategia de la organización y son supervisados por la más alta autoridad')
    ], validators=[DataRequired()])

    acc_social = SelectField('8. ¿En qué grado los colaboradores internos participan, brindan soporte y se involucran en las distintas acciones de sociales con la comunidad local o en donde está inmersa?', choices=[
        (0, 'No'),
        (1, 'La organización no aborda temas sociales con sus colaboradores internos'),
        (2, 'Los colaboradores internos están involucrados en temas relacionados a voluntarios u otras acciones comunitarias y sociales'),
        (3, 'La máxima autoridad de la Organización impulsa iniciativas de acciones sociales con la comunidad local'),
        (4, 'La organización se comunica de manera amplia con sus colaboradores en temas de sostenibilidad, posee programas estructurados de inversión social e indicadores a largo plazo')
    ], validators=[DataRequired()])

    ssma = SelectField('9. ¿Cómo gestiona su organización los aspectos relacionados con la salud y seguridad en el trabajo de sus colaboradores?', choices=[
        (0, 'No'),
        (1, 'La organización incumple la normativa vigente en el cuidado de la salud y seguridad de sus colaboradores'),
        (2, 'La organización cumple la normativa vigente en el cuidado de la salud y seguridad de sus colaboradores'),
        (3, 'La organización posee un sistema de gestión de la salud y la seguridad en el trabajo de sus colaboradores, evaluando riesgos e investigación de accidentes'),
        (4, 'La organización posee un sistema de gestión de la salud y la seguridad en el trabajo de sus colaboradores, evaluando riesgos e investigación de accidentes y posee una certificación externa en su sistema de gestión')
    ], validators=[DataRequired()])

    formacion = SelectField('10. ¿Cómo gestiona su organización los aspectos relacionados con la formación de sus colaboradores?', choices=[
        (0, 'No'),
        (1, 'La organización no posee un programa de capacitación para sus colaboradores'),
        (2, 'La organización realiza capacitaciones esporádicas a sus colaboradores'),
        (3, 'La organización posee un programa de capacitación para sus colaboradores destinado a mejorar sus aptitudes'),
        (4, 'La organización posee un programa de capacitación para sus colaboradores destinado a mejorar sus aptitudes y realiza evaluaciones periódicas de desempeño')
    ], validators=[DataRequired()])

    codigo_conducta = SelectField('11. ¿Su organización posee un Código de Ética/Conducta aprobado?', choices=[
        (0, 'No'),
        (1, 'La organización no posee código de ética'),
        (2, 'La organización se encuentra en un proceso de elaboración de su código de ética'),
        (3, 'La organización cuenta con un código de ética no aprobado por la más alta autoridad'),
        (4, 'La organización cuenta con un código de ética aprobado por la más alta autoridad.')
    ], validators=[DataRequired()])

    linea_etica = SelectField('12. ¿Tiene la organización un mecanismo de reporte como un canal de denuncia o línea ética?', choices=[
        (0, 'No'),
        (1, 'En la organización no existe un canal de denuncias ni línea de ética'),
        (2, 'La organización se encuentra en proceso de realización y se está desarrollando un protocolo de gestión'),
        (3, 'Existe un canal interno de denuncias, el cual es manejado por personal de la organización'),
        (4, 'Existe un canal de denuncias o línea de ética administrado por una entidad externa y un protocolo de gestión de las mismas. Se garantiza la confidencialidad de todos los comunicados que se realicen')
    ], validators=[DataRequired()])

    area_compliance = SelectField('13. ¿La organización tiene una área o encargado de Cumplimiento/Compliance/Ética?', choices=[
        (0, 'No'),
        (1, 'La organización no cuenta ni con un área ni encargado de Cumplimiento o de Compliance'),
        (2, 'En la organización se está diagramando el área y/o definiendo el responsable'),
        (3, 'La organización cuenta con una persona que se encarga de dichas cuestiones'),
        (4, 'La organización cuenta con un área específica, encargada de la gestión de un programa de Compliance')
    ], validators=[DataRequired()])

    due_dilligence = SelectField('14. ¿Realizan acciones de debida diligencia previo a la contratación de terceras partes?', choices=[
        (0, 'No'),
        (1, 'En la organización no existe un proceso de debida diligencia para conocer a los terceros con los que interactúa'),
        (2, 'La Organización se encuentra en elaboración de un proceso de debida diligencia'),
        (3, 'La organización realiza acciones de debida diligencia pero en forma posterior a la contratación de un tercero'),
        (4, 'La organización realiza un proceso de debida diligencia en forman anterior a la contratación de un tercero')
    ], validators=[DataRequired()])

    riesgos = SelectField('15. ¿La organización realizó una evaluación de sus riesgos particulares (fraude, corrupción, soborno, lavado de activos, etc.)?', choices=[
        (0, 'No'),
        (1, 'En la organización no se ha realizado una evaluación de riesgos'),
        (2, 'La organización se encuentra en proceso de realización de una evaluación de riesgos'),
        (3, 'La organización cuenta con una evaluación de riesgos pero la misma está incompleta'),
        (4, 'La organización cuenta con una evaluación de riesgos, mediante la cual se establecieron los posibles riesgos que tiene la Compañía al interactuar con distintos terceros')
    ], validators=[DataRequired()])

    huella_co2 = SelectField('16. ¿Su Organización posee Medición de Huella de Carbono?', choices=[
        (0, 'No'),
        (1, 'No posee Medición de Huella de Carbono'),
        (2, 'La organización posee Medición de Huella de Carbono alcance 1'),
        (3, 'La organización posee Medición de Huella de Carbono alcance 1 y cuenta con objetivo de reducción'),
        (4, 'La organización posee Medición de Huella de Carbono alcances 1, 2 y 3, cuenta con objetivo, plan de reducción, y, además, cuenta con disminución en su Huella de Carbono')
    ], validators=[DataRequired()])

    submit = SubmitField('Enviar')
